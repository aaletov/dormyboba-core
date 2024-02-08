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
from .model.generated import (
    DormybobaUser,
    DormybobaRole,
    VerificationCode,
    Institute,
    AcademicType,
    Mailing,
    Queue,
    QueueToUser,
)

class DormybobaCoreServicer(apiv1grpc.DormybobaCoreServicer):
    """Provides methods that implement functionality of dormyboba-core server."""
    
    def __init__(self, engine: Engine, worksheet: Worksheet):
        self.engine = engine
        self.worksheet = worksheet

    @staticmethod
    def nullifier(message: Any, field_name: str) -> Optional[Any]:
        return None if not(message.HasField(field_name)) else getattr(message, field_name)

    def GenerateVerificationCode(
            self,
            request: apiv1.GenerateVerificationCodeRequest,
            context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        code = random.randint(1000, 9999)
        stmt = select(DormybobaRole.role_id).where(DormybobaRole.role_name == request.role_name)
        role_id: int = session.execute(stmt).first()[0]
        stmt = insert(VerificationCode).values(
            code=code,
            role_id=role_id,
        )
        session.execute(stmt)
        session.commit()

        return apiv1.GenerateVerificationCodeResponse(verification_code=code)
    
    def GetRoleByVerificationCode(
        self,
        request: apiv1.GetRoleByVerificationCodeRequest,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        stmt = select(VerificationCode).where(VerificationCode.code == request.verification_code)
        res = session.execute(stmt).first()
        if res in None:
            return context.abort_with_status(grpc.StatusCode.INVALID_ARGUMENT)
        role: DormybobaRole = res[0]
        api_role = apiv1.DormybobaRole(
            role_id=role.role_id,
            role_name=role.role_name,
        )
        return apiv1.GetRoleByVerificationCodeResponse(role=api_role)

    def CreateUser(
        self,
        request: apiv1.CreateUserRequest,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        stmt = select(VerificationCode).where(VerificationCode.code == request.verification_code)
        res = session.execute(stmt).first()
        if res in None:
            return context.abort_with_status(grpc.StatusCode.INVALID_ARGUMENT)
        
        stmt = insert(DormybobaUser).values(
            user_id=request.user_id,
            institute_id=request.institute_id,
            role_id=request.role_id,
            academic_type_id=request.academic_type_id,
            year=request.year,
            group=request.group,
        )
        session.execute(stmt)
        session.commit()
        return Empty()

    def GetUserById(
        self,
        request: apiv1.GetUserByIdRequest,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        stmt = select(DormybobaUser).where(DormybobaUser.user_id == request.user_id)
        res = session.execute(stmt).first()

        if res is None:
            return apiv1.GetUserByIdResponse()
        
        user: DormybobaUser = res[0]

        return apiv1.GetUserByIdResponse(
            user=apiv1.DormybobaUser(
                user_id=user.user_id,
                institute=apiv1.Institute(
                    institute_id=user.institute.institute_id,
                    institute_name=user.institute.institute_name,
                ),
                role=apiv1.DormybobaRole(
                    role_id=user.role.role_id,
                    role_name=user.role.role_name,
                ),
                academic_type=apiv1.AcademicType(
                    type_id=user.academic_type.type_id,
                    type_name=user.academic_type.type_name,
                ),
                year=user.year,
                group=user.group,
            ),
        )


    def GetAllInstitutes(
        self,
        request: None,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        stmt = select(Institute)
        institutes = session.execute(stmt).all()
        api_institutes = []
        for row in institutes:
            institute: Institute = row[0]
            api_institute = apiv1.Institute(
                institute_id=institute.institute_id,
                institute_name=institute.institute_name,
            )
            api_institutes.append(api_institute)
        return apiv1.GetAllInstitutesResponse(institutes=api_institutes)

    def GetInstituteByName(
        self,
        request: apiv1.GetInstituteByNameRequest,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        stmt = select(Institute).where(Institute.institute_name == request.institute_name)
        res = session.execute(stmt).first()
        if res is None:
            return context.abort_with_status(grpc.StatusCode.INVALID_ARGUMENT)
        institute: Institute = res[0]
        api_institute = apiv1.Institute(
            institute_id=institute.institute_id,
            institute_name=institute.institute_name,
        )
        return apiv1.GetInstituteByNameResponse(institute=api_institute)
    
    def GetAcademicTypeByName(
        self,
        request: apiv1.GetAcademicTypeByNameRequest,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        stmt = select(AcademicType).where(AcademicType.type_name == request.type_name)
        res = session.execute(stmt).first()
        if res is None:
            return context.abort_with_status(grpc.StatusCode.INVALID_ARGUMENT)
        academic_type: AcademicType = res[0]
        api_academic_type = apiv1.AcademicType(
            type_id=academic_type.type_id,
            type_name=academic_type.type_name,
        )
        return apiv1.GetAcademicTypeByNameResponse(academic_type=api_academic_type)
    
    def CreateMailing(
        self,
        request: apiv1.CreateMailingRequest,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        at = None if request.HasField("at") else request.at.ToDatetime()
        stmt = insert(Mailing).values(
            institute_id=self.nullifier(request, "institute_id"),
            academic_type_id=self.nullifier(request, "academic_type_id"),
            year=self.nullifier(request, "year"),
            at=at,
            theme=self.nullifier(request, "theme"),
            mailing_text=request.mailing_text,
        )
        session.execute(stmt)
        session.commit()
        return Empty()

    def CreateQueue(
        self,
        request: apiv1.CreateQueueRequest,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        open = None if request.HasField("open") else request.open.ToDatetime()
        close = None if request.HasField("open") else request.close.ToDatetime()
        stmt = insert(Queue).values(
            title=request.title,
            description=self.nullifier(request, "description"),
            open=open,
            close=close,
        )
        session.execute(stmt)
        session.commit()
        return Empty()
    
    def AddPersonToQueue(
        self,
        request: apiv1.AddPersonToQueueRequest,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        stmt = select(Queue).where(Queue.queue_id == request.queue_id)
        res = session.execute(stmt).first()

        if res is None:
            return context.abort_with_status(grpc.StatusCode.INVALID_ARGUMENT)

        queue: Queue = res[0]
        stmt = None
        is_active = False
        if queue.active_user == None:
            stmt = update(Queue).where(Queue.queue_id == request.queue_id).values(
                active_user_id=request.user_id
            )
        else:
            # just throw if user already joined queue
            stmt = insert(QueueToUser).values(
                user_id=request.user_id,
                queue_id=request.queue_id,
                joined=datetime.now(),
            )
            is_active = True

        session.execute(stmt)
        session.commit()
        return apiv1.AddPersonToQueueResponse(is_active=is_active)
    
    def RemovePersonFromQueue(
        self,
        request: apiv1.RemovePersonFromQueueRequest,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        # just throw if user already left queue
        stmt = delete(QueueToUser).where(
            and_(
                QueueToUser.user_id == request.user_id,
                QueueToUser.queue_id == request.queue_id,
            )
        )
        session.execute(stmt)
        session.commit()
        return Empty()
    
    def PersonCompleteQueue(
        self,
        request: apiv1.PersonCompleteQueueRequest,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        stmt = delete(QueueToUser).where(
            and_(
                QueueToUser.user_id == request.user_id,
                QueueToUser.queue_id == request.queue_id,
            )
        )
        session.execute(stmt)

        stmt = select(Queue).where(Queue.queue_id == request.queue_id)
        queue: Queue = session.execute(stmt).first()[0]

        key: Callable[[QueueToUser], datetime] = lambda qtu: qtu.joined
        sorted_qtu = sorted(queue.queue_to_user, key=key)

        is_queue_empty = (len(sorted_qtu) == 0)
        active_user_id = None if is_queue_empty else sorted_qtu[0].user_id

        stmt = update(Queue).where(Queue.queue_id == request.queue_id).values(
            active_user_id=active_user_id,
        )

        session.execute(stmt)
        session.commit()

        return apiv1.PersonCompleteQueueResponse(
            is_queue_empty=is_queue_empty,
            active_user_id=active_user_id,
        )
    
    DEFECT_TYPE_MAP = {
        "Электрика": apiv1.ELECTRICITY,
        "Сантехника": apiv1.PLUMB,
        "Общее": apiv1.COMMON,
    }

    REV_DEFECT_TYPE_MAP = {v: k for k, v in DEFECT_TYPE_MAP.items()}

    DEFECT_STATUS_MAP = {
        "Добавлено": apiv1.CREATED,
        "Принято": apiv1.ACCEPTED,
        "Решено": apiv1.RESOLVED,
    }

    REV_DEFECT_STATUS_MAP = {v: k for k, v in DEFECT_STATUS_MAP.items()}
    
    def CreateDefect(
        self,
        request: apiv1.CreateDefectRequest,
        context: grpc.ServicerContext,
    ):
        column = self.worksheet.col_values(1)
        i = len(column) + 1
        if None in column:
            i = column.index(None) + 1
        irange: List[Cell] = self.worksheet.range(i, 1, i+4, 5)
        defect_id = "DD" + str(random.randint(1000, 9999))
        values = (
            defect_id,
            request.user_id,
            self.REV_DEFECT_TYPE_MAP[request.defect_type],
            request.description,
            self.REV_DEFECT_STATUS_MAP[request.defect_status],
        )
        for cell, value in zip(irange, values):
            cell.value = value

        self.worksheet.update_cells(irange)

        return apiv1.CreateDefectResponse(
            defect=apiv1.Defect(
                defect_id=defect_id,
                user_id=request.user_id,
                defect_type=request.defect_type,
                description=request.description,
                defect_status=request.defect_status,
            ),
        )

    def GetDefectById(
        self,
        request: apiv1.GetDefectByIdRequest,
        context: grpc.ServicerContext,
    ):
        column = self.worksheet.col_values(1)
        if request.defect_id not in column:
            return apiv1.GetDefectByIdResponse()

        i = column.index(request.defect_id) + 1
        irange: List[Cell] = self.worksheet.range(i, 1, i+4, 5)
        return apiv1.GetDefectByIdResponse(
            defect=apiv1.Defect(
                defect_id=irange[0].value,
                user_id=int(irange[1].value),
                defect_type=self.DEFECT_TYPE_MAP[irange[2].value],
                description=irange[3].value,
                defect_status=self.DEFECT_STATUS_MAP[irange[4].value],
            ),
        )

    def UpdateDefect(
        self,
        request: apiv1.UpdateDefectRequest,
        context: grpc.ServicerContext,
    ):
        column = self.worksheet.col_values(1)
        if request.defect.defect_id not in column:
            return context.abort_with_status(grpc.StatusCode.INVALID_ARGUMENT)

        i = column.index(request.defect.defect_id) + 1
        irange: List[Cell] = self.worksheet.range(i, 2, i+4, 5)

        values = (
            request.defect.user_id,
            self.REV_DEFECT_TYPE_MAP[request.defect.defect_type],
            request.defect.description,
            self.REV_DEFECT_STATUS_MAP[request.defect.defect_status],
        )

        for cell, value in zip(irange, values):
            cell.value = value

        self.worksheet.update_cells(irange)
        return Empty()
    
    def AssignDefect(
        self,
        request: apiv1.AssignDefectRequest,
        context: grpc.ServicerContext,
    ):
        session = Session(self.engine)
        stmt = (
            select(DormybobaUser)
            .join(DormybobaRole, DormybobaUser.role_id == DormybobaRole.role_id)
            .where(DormybobaRole.role_name == "admin")
        )
        res = session.execute(stmt).first()

        if res is None:
            return context.abort_with_status(grpc.StatusCode.INTERNAL)

        admin_user: DormybobaUser = res[0]

        return apiv1.AssignDefectResponse(assigned_user_id=admin_user.user_id)

    def _build_api_mailing_event(
        self,
        mailing: Mailing,
        users: List[DormybobaUser],
    ) -> apiv1.MailingEvent:
        at = None if mailing.at is None else Timestamp().FromDatetime(mailing.at)
        api_mailing = apiv1.Mailing(
            theme=mailing.theme,
            mailing_text=mailing.mailing_text,
            at=at,
            institute_id=mailing.institute_id,
            academic_type_id=mailing.academic_type_id,
            year=mailing.year,
        )
        api_users = []
        for user in users:
            condition = (
                ((mailing.academic_type_id is None) or
                    (mailing.academic_type_id == user.academic_type_id)) and
                ((mailing.institute_id is None) or
                    (mailing.institute_id == user.institute_id)) and
                ((mailing.year is None) or
                    (mailing.year == user.year))
            )
            if condition:
                api_institute = apiv1.Institute(
                    institute_id=user.institute.institute_id,
                    institute_name=user.institute.institute_name,
                )
                api_academic_type = apiv1.AcademicType(
                    type_id=user.academic_type.type_id,
                    type_name=user.academic_type.type_name,
                )
                api_users.append(apiv1.DormybobaUser(
                    user_id=user.user_id,
                    institute=api_institute,
                    academic_type=api_academic_type,
                    year=user.year,
                    group=user.group,
                ))
        return apiv1.MailingEvent(
            mailing=api_mailing,
            users=api_users,
        )

    async def MailingEvent(
        self,
        request: Any,
        context: grpc.ServicerContext,
    ):
        while True:
            logging.debug("Checking mailing events...")
            try:
                session = Session(self.engine)
                stmt = select(Mailing).where(
                    and_(
                        or_(
                            Mailing.at == None,
                            datetime.now() > Mailing.at,
                        ),
                        Mailing.is_event_generated == False,
                    )
                )
                row = session.execute(stmt).first()

                if row is None:
                    await asyncio.sleep(15)
                    continue
                
                mailing: Mailing = row[0]
                # Only registered
                stmt = select(DormybobaUser).where(
                    and_(
                        DormybobaUser.institute_id != None,
                        DormybobaUser.academic_type_id != None,
                        DormybobaUser.year != None,
                    )
                )
                rows = session.execute(stmt).all()
                users = list([row[0] for row in rows])
    
                event = self._build_api_mailing_event(mailing, users)

                stmt = update(Mailing).where(Mailing.mailing_id == mailing.mailing_id).values(
                    is_event_generated=True,
                )
                session.execute(stmt)
                session.commit()

                yield apiv1.MailingEventResponse(event=event)
            except Exception as exc:
                logging.exception(exc)

    def _build_api_queue_event(
        self,
        queue: Queue,
        users: List[DormybobaUser],
    ) -> apiv1.QueueEvent:
        open = None if queue.open is None else Timestamp().FromDatetime(queue.open)
        close = None if queue.close is None else Timestamp().FromDatetime(queue.close)
        
        api_queue = apiv1.Queue(
            queue_id=queue.queue_id,
            title=queue.title,
            description=queue.description,
            open=open,
            close=close,
        )

        api_users = []
        for user in users:
            api_institute = apiv1.Institute(
                institute_id=user.institute.institute_id,
                institute_name=user.institute.institute_name,
            )
            api_academic_type = apiv1.AcademicType(
                type_id=user.academic_type.type_id,
                type_name=user.academic_type.type_name,
            )
            api_users.append(apiv1.DormybobaUser(
                user_id=user.user_id,
                institute=api_institute,
                academic_type=api_academic_type,
                year=user.year,
                group=user.group,
            ))

        return apiv1.QueueEvent(
            queue=api_queue,
            users=api_users,
        )

    async def QueueEvent(
        self,
        request: Any,
        context: grpc.ServicerContext,
    ):
        while True:
            logging.debug("Checking queue events...")
            try:
                session = Session(self.engine)
                stmt = select(Queue).where(
                    and_(
                        datetime.now() > Queue.open,
                        Queue.is_event_generated == False,
                    )
                )
                row = session.execute(stmt).first()
                if row is None:
                    await asyncio.sleep(15)
                    continue
                queue: Queue = row[0]
                stmt = select(DormybobaUser)
                res = session.execute(stmt).all()
                users = list([row[0] for row in res])

                event = self._build_api_queue_event(queue, users)

                stmt = update(Queue).where(Queue.queue_id == queue.queue_id).values(
                    is_event_generated=True,
                )
                session.execute(stmt)
                session.commit()
    
                yield apiv1.QueueEventResponse(event=event)
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