from typing import Any, Optional
import random
import logging
import asyncio
import datetime
import grpc
from google.protobuf.empty_pb2 import Empty
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
from .. import entity
from ..repository import (
    SqlAlchemyDormybobaUserRepository,
    SqlAlchemyDormybobaRoleRepository,
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
        user_repository: SqlAlchemyDormybobaUserRepository,
        role_repository: SqlAlchemyDormybobaRoleRepository,
        institute_repository: SqlAlchemyInstituteRepository,
        academic_type_repository: SqlAlchemyAcademicTypeRepository,
        sheet_repository: GsheetDefectRepository,
        mailing_repository: SqlAlchemyMailingRepository,
        queue_repository: SqlAlchemyQueueRepository,
        token_converter: entity.TokenConverter,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.institute_repository = institute_repository
        self.academic_type_repository = academic_type_repository
        self.sheet_repository = sheet_repository
        self.mailing_repository = mailing_repository
        self.queue_repository = queue_repository
        self.token_converter = token_converter

    @staticmethod
    def nullifier(message: Any, field_name: str) -> Optional[Any]:
        return None if not(message.HasField(field_name)) else getattr(message, field_name)

    def GenerateToken(
        self,
        request: apiv1.GenerateTokenRequest,
        context: grpc.aio.ServicerContext,
    ):
        role = self.role_repository.getByName(request.role_name)
        if role == None:
            return context.abort(
                code=grpc.StatusCode.INVALID_ARGUMENT,
                details="No such role",
            )

        token = entity.Token.generate(request.role_name)
        return apiv1.GenerateTokenResponse(
            token=self.token_converter.encode(token),
        )

    def UpdateUser(
        self,
        request: apiv1.UpdateUserRequest,
        context: grpc.aio.ServicerContext,
    ):
        user = entity.DormybobaUser.from_api(request.user)
        if self.user_repository.getById(user.user_id) == None:
            return context.abort(
                code=grpc.StatusCode.INVALID_ARGUMENT,
                details="No such user",
            )

        user = self.user_repository.update(user)
        return apiv1.UpdateUserResponse(
            user=user.to_api(),
        )

    def GetUserById(
        self,
        request: apiv1.GetUserByIdRequest,
        context: grpc.aio.ServicerContext,
    ):
        user = self.user_repository.getById(request.user_id)

        if user is None:
            # Incorrect! Delete after acceptance
            return context.abort(
                code=grpc.StatusCode.INVALID_ARGUMENT,
                details="No such user",
            )
            # Correct
            return apiv1.GetUserByIdResponse()

        return apiv1.GetUserByIdResponse(
            user=user.to_api(),
        )

    def GetAllInstitutes(
        self,
        request: None,
        context: grpc.aio.ServicerContext,
    ):
        entity_institutes = self.institute_repository.list()
        return apiv1.GetAllInstitutesResponse(
            institutes=list([i.to_api() for i in entity_institutes]),
        )

    def GetInstituteByName(
        self,
        request: apiv1.GetInstituteByNameRequest,
        context: grpc.aio.ServicerContext,
    ):
        institute = self.institute_repository.getByName(request.institute_name)
        if institute is None:
            return context.abort(
                code=grpc.StatusCode.INVALID_ARGUMENT,
                details="No such instutute",
            )
        return apiv1.GetInstituteByNameResponse(
            institute=institute.to_api(),
        )

    def GetAllAcademicTypes(
        self,
        request: None,
        context: grpc.aio.ServicerContext,
    ):
        academic_types = self.academic_type_repository.list()
        return apiv1.GetAllAcademicTypesResponse(
            academic_types=list([t.to_api() for t in academic_types])
        )

    def GetAcademicTypeByName(
        self,
        request: apiv1.GetAcademicTypeByNameRequest,
        context: grpc.aio.ServicerContext,
    ):
        academic_type = self.academic_type_repository.getByName(request.type_name)
        return apiv1.GetAcademicTypeByNameResponse(
            academic_type=academic_type.to_api(),
        )

    def CreateMailing(
        self,
        request: apiv1.CreateMailingRequest,
        context: grpc.aio.ServicerContext,
    ):
        mailing = entity.Mailing.from_api(request.mailing)
        if (mailing.at is not None) and (mailing.at < datetime.datetime.now()):
            return context.abort(
                code=grpc.StatusCode.INVALID_ARGUMENT,
                details="\"at\" cannot be less than current datetime",
            )
        mailing = self.mailing_repository.add(
            mailing,
        )
        return apiv1.CreateMailingResponse(
            mailing=mailing.to_api(),
        )

    def CreateQueue(
        self,
        request: apiv1.CreateQueueRequest,
        context: grpc.aio.ServicerContext,
    ):
        queue = self.queue_repository.add(entity.Queue.from_api(request.queue))
        return apiv1.CreateQueueResponse(queue=queue.to_api())

    def AddPersonToQueue(
        self,
        request: apiv1.AddPersonToQueueRequest,
        context: grpc.aio.ServicerContext,
    ):
        queue = self.queue_repository.addUser(request.queue_id, request.user_id)
        is_active = queue.active_user.user_id == request.user_id
        return apiv1.AddPersonToQueueResponse(is_active=is_active)

    def RemovePersonFromQueue(
        self,
        request: apiv1.RemovePersonFromQueueRequest,
        context: grpc.aio.ServicerContext,
    ):
        queue = self.queue_repository.getById(request.queue_id)
        user = self.user_repository.getById(request.user_id)
        self.queue_repository.deleteUser(queue, user)
        return Empty()

    def PersonCompleteQueue(
        self,
        request: apiv1.PersonCompleteQueueRequest,
        context: grpc.aio.ServicerContext,
    ):
        queue = self.queue_repository.getById(request.queue_id)
        queue = self.queue_repository.moveQueue(queue)

        is_queue_empty = queue.active_user is None
        active_user_id = None if is_queue_empty else queue.active_user.user_id

        return apiv1.PersonCompleteQueueResponse(
            is_queue_empty=is_queue_empty,
            active_user_id=active_user_id,
        )

    def CreateDefect(
        self,
        request: apiv1.CreateDefectRequest,
        context: grpc.aio.ServicerContext,
    ):
        defect = entity.Defect.from_api(request.defect)
        defect.defect_id = "DD" + str(random.randint(1000, 9999))
        self.sheet_repository.add(defect)

        return apiv1.CreateDefectResponse(
            defect=defect.to_api(),
        )

    def GetDefectById(
        self,
        request: apiv1.GetDefectByIdRequest,
        context: grpc.aio.ServicerContext,
    ):
        defect = self.sheet_repository.getById(request.defect_id)

        return apiv1.GetDefectByIdResponse(
            defect=defect.to_api(),
        )

    def UpdateDefect(
        self,
        request: apiv1.UpdateDefectRequest,
        context: grpc.aio.ServicerContext,
    ):
        defect = entity.Defect.from_api(request.defect)
        self.sheet_repository.update(defect)
        return Empty()

    def AssignDefect(
        self,
        request: apiv1.AssignDefectRequest,
        context: grpc.aio.ServicerContext,
    ):
        role = self.role_repository.getByName("admin")
        user = self.user_repository.listByRole(role)[0]
        return apiv1.AssignDefectResponse(assigned_user_id=user.user_id)

    async def MailingEvent(
        self,
        request: Any,
        context: grpc.aio.ServicerContext,
    ):
        logger = logging.getLogger('dormyboba')
        while True:
            logger.debug("Checking mailing events...")
            try:
                event = self.mailing_repository.getEvent()

                if event is None:
                    await asyncio.sleep(15)
                    continue

                yield apiv1.MailingEventResponse(event=event.to_api())
            except Exception as exc:
                logger.exception(exc)

    async def QueueEvent(
        self,
        request: Any,
        context: grpc.aio.ServicerContext,
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