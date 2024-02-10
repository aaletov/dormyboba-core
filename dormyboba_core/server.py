from typing import Callable, List, Any, Optional
import random
from concurrent import futures
import logging
import asyncio
from datetime import datetime
import grpc
from google.protobuf.empty_pb2 import Empty
from google.protobuf.timestamp_pb2 import Timestamp
from sqlalchemy.orm import Session
from sqlalchemy import (
    Engine,
    insert,
    select,
    update,
    delete,
    and_,
    or_,
)
from gspread import Cell, Worksheet
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
from . import entity
from .repository import (
    SqlAlchemyDormybobaUserRepository,
    SqlAlchemyVerificationCodeRepository,
    SqlAlchemyInstituteRepository,
    SqlAlchemyAcademicTypeRepository,
    GsheetDefectRepository,
    SqlAlchemyMailingRepository,
    SqlAlchemyQueueRepository,
)

class DormybobaCoreServicer(apiv1grpc.DormybobaCoreServicer):
    """Provides methods that implement functionality of dormyboba-core server."""
    
    def __init__(
        self,
        engine: Engine,
        worksheet: Worksheet,
        user_repository: SqlAlchemyDormybobaUserRepository,
        code_repository: SqlAlchemyVerificationCodeRepository,
        institute_repository: SqlAlchemyInstituteRepository,
        academic_type_repository: SqlAlchemyAcademicTypeRepository,
        sheet_repository: GsheetDefectRepository,
        mailing_repository: SqlAlchemyMailingRepository,
        queue_repository: SqlAlchemyQueueRepository,
    ):
        self.engine = engine
        self.worksheet = worksheet
        self.user_repository = user_repository
        self.code_repository = code_repository
        self.institute_repository = institute_repository
        self.academic_type_repository = academic_type_repository
        self.sheet_repository = sheet_repository
        self.mailing_repository = mailing_repository
        self.queue_repository = queue_repository

    @staticmethod
    def nullifier(message: Any, field_name: str) -> Optional[Any]:
        return None if not(message.HasField(field_name)) else getattr(message, field_name)

    def GenerateVerificationCode(
            self,
            request: apiv1.GenerateVerificationCodeRequest,
            context: grpc.ServicerContext,
    ):
        code = entity.VerificationCode(
            verification_code=random.randint(1000, 9999),
            role=entity.DormybobaRole(role_name=request.role_name),
        )
        self.code_repository.add(code)

        return apiv1.GenerateVerificationCodeResponse(
            verification_code=code.verification_code,
        )
    
    def GetRoleByVerificationCode(
        self,
        request: apiv1.GetRoleByVerificationCodeRequest,
        context: grpc.ServicerContext,
    ):
        code = self.code_repository.getByCode(request.verification_code)
        if code is None:
            return context.abort_with_status(grpc.StatusCode.INVALID_ARGUMENT)
        
        api_role = code.role.to_api()
        return apiv1.GetRoleByVerificationCodeResponse(role=api_role)

    def CreateUser(
        self,
        request: apiv1.CreateUserRequest,
        context: grpc.ServicerContext,
    ):
        code = self.code_repository.getByCode(request.verification_code)
        if code is None:
            return context.abort_with_status(grpc.StatusCode.INVALID_ARGUMENT)

        user=entity.DormybobaUser(
            user_id=request.user_id,
            role=entity.DormybobaRole(role_id=request.role_id),
            institute=entity.Institute(institute_id=request.institute_id),
            academic_type=entity.AcademicType(type_id=request.academic_type_id),
            year=request.year,
            group=request.group,
        )

        self.user_repository.add(user)        
        return Empty()

    def GetUserById(
        self,
        request: apiv1.GetUserByIdRequest,
        context: grpc.ServicerContext,
    ):
        user = self.user_repository.getById(request.user_id)

        if user is None:
            return apiv1.GetUserByIdResponse()
        
        return apiv1.GetUserByIdResponse(
            user=user.to_api(),
        )

    def GetAllInstitutes(
        self,
        request: None,
        context: grpc.ServicerContext,
    ):
        entity_institutes = self.institute_repository.list()
        return apiv1.GetAllInstitutesResponse(
            institutes=list([i.to_api() for i in entity_institutes]),
        )

    def GetInstituteByName(
        self,
        request: apiv1.GetInstituteByNameRequest,
        context: grpc.ServicerContext,
    ):
        institute = self.institute_repository.getByName(request.institute_name)
        if institute is None:
            return context.abort_with_status(grpc.StatusCode.INVALID_ARGUMENT)
        return apiv1.GetInstituteByNameResponse(
            institute=institute.to_api(),
        )
    
    def GetAcademicTypeByName(
        self,
        request: apiv1.GetAcademicTypeByNameRequest,
        context: grpc.ServicerContext,
    ):
        academic_type = self.academic_type_repository.getByName(request.type_name)
        return apiv1.GetAcademicTypeByNameResponse(
            academic_type=academic_type.to_api(),
        )
    
    def CreateMailing(
        self,
        request: apiv1.CreateMailingRequest,
        context: grpc.ServicerContext,
    ):
        mailing = self.mailing_repository.add(
            entity.Mailing.from_api(request.mailing),
        )
        return apiv1.CreateMailingResponse(
            mailing=mailing.to_api(),
        )

    def CreateQueue(
        self,
        request: apiv1.CreateQueueRequest,
        context: grpc.ServicerContext,
    ):
        queue = self.queue_repository.add(entity.Queue.from_api(request.queue))
        return apiv1.CreateQueueResponse(queue=queue.to_api())
    
    def AddPersonToQueue(
        self,
        request: apiv1.AddPersonToQueueRequest,
        context: grpc.ServicerContext,
    ):
        queue = self.queue_repository.getById(request.queue_id)
        user = self.user_repository.getById(request.user_id)
        queue = self.queue_repository.addUser(queue, user)

        is_active = queue.active_user.user_id == user.user_id

        return apiv1.AddPersonToQueueResponse(is_active=is_active)
    
    def RemovePersonFromQueue(
        self,
        request: apiv1.RemovePersonFromQueueRequest,
        context: grpc.ServicerContext,
    ):
        queue = self.queue_repository.getById(request.queue_id)
        user = self.user_repository.getById(request.user_id)
        self.queue_repository.deleteUser(queue, user)
        return Empty()
    
    def PersonCompleteQueue(
        self,
        request: apiv1.PersonCompleteQueueRequest,
        context: grpc.ServicerContext,
    ):
        queue = self.queue_repository.getById(request.queue_id)
        queue = self.queue_repository.moveQueue(queue)

        is_queue_empty = queue.active_user is None
        active_user_id = queue.active_user.user_id

        return apiv1.PersonCompleteQueueResponse(
            is_queue_empty=is_queue_empty,
            active_user_id=active_user_id,
        )
    
    def CreateDefect(
        self,
        request: apiv1.CreateDefectRequest,
        context: grpc.ServicerContext,
    ):
        defect = entity.Defect.from_api(request.defect)
        self.sheet_repository.add(defect)

        return apiv1.CreateDefectResponse(
            defect=defect.to_api(),
        )

    def GetDefectById(
        self,
        request: apiv1.GetDefectByIdRequest,
        context: grpc.ServicerContext,
    ):
        defect = self.sheet_repository.getById(request.defect_id)

        return apiv1.GetDefectByIdResponse(
            defect=defect.to_api(),
        )

    def UpdateDefect(
        self,
        request: apiv1.UpdateDefectRequest,
        context: grpc.ServicerContext,
    ):
        defect = entity.Defect.from_api(request.defect)
        self.sheet_repository.update(defect)
        return Empty()
    
    def AssignDefect(
        self,
        request: apiv1.AssignDefectRequest,
        context: grpc.ServicerContext,
    ):
        user = self.user_repository.listByRole("admin")[0]
        return apiv1.AssignDefectResponse(assigned_user_id=user.user_id)

    async def MailingEvent(
        self,
        request: Any,
        context: grpc.ServicerContext,
    ):
        while True:
            logging.debug("Checking mailing events...")
            try:
                event = self.mailing_repository.getEvent()

                if event is None:
                    await asyncio.sleep(15)
                    continue

                yield apiv1.MailingEventResponse(event=event.to_api())
            except Exception as exc:
                logging.exception(exc)

    async def QueueEvent(
        self,
        request: Any,
        context: grpc.ServicerContext,
    ):
        while True:
            logging.debug("Checking queue events...")
            try:
                event = self.queue_repository.getEvent()

                if event is None:
                    await asyncio.sleep(15)
                    continue
                
                yield apiv1.QueueEventResponse(event=event.to_api())
            except Exception as exc:
                logging.exception(exc)

async def serve(engine: Engine, worksheet: Worksheet):
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    apiv1grpc.add_DormybobaCoreServicer_to_server(
        DormybobaCoreServicer(engine, worksheet), server
    )
    logging.info("Starting server...")
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(serve())