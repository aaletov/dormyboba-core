from typing import Callable, List, Any
import random
from concurrent import futures
import logging
from datetime import datetime
import grpc
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete, and_, or_
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
    
    def __init__(self, session: Session, worksheet: Worksheet):
        self.session = session        
        self.worksheet = worksheet

    def GenerateVerificationCode(
            self,
            request: apiv1.GenerateVerificationCodeRequest,
            context: grpc.ServicerContext,
    ):
        code = random.randint(1000, 9999)
        stmt = select(DormybobaRole.role_id).where(DormybobaRole.role_name == request.role_name)
        role_id: int = self.session.execute(stmt).first()[0]
        stmt = insert(VerificationCode).values(
            code=code,
            role_id=role_id,
        )
        self.session.execute(stmt)
        self.session.commit()

        return apiv1.GenerateVerificationCodeResponse(verification_code=code)
    
    def GetRoleByVerificationCode(
        self,
        request: apiv1.GetRoleByVerificationCodeRequest,
        context: grpc.ServicerContext,
    ):
        stmt = select(VerificationCode).where(VerificationCode.code == request.verification_code)
        res = self.session.execute(stmt).first()
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
        stmt = select(VerificationCode).where(VerificationCode.code == request.verification_code)
        res = self.session.execute(stmt).first()
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
        self.session.execute(stmt)
        self.session.commit()

    def GetUserById(
        self,
        request: apiv1.GetUserByIdRequest,
        context: grpc.ServicerContext,
    ):
        stmt = select(DormybobaUser).where(DormybobaUser.user_id == request.user_id)
        res = self.session.execute(stmt).first()

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
        stmt = select(Institute)
        institutes = self.session.execute(stmt).all()
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
        stmt = select(Institute).where(Institute.institute_name == request.institute_name)
        res = self.session.execute(stmt).first()
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
        stmt = select(AcademicType).where(AcademicType.type_name == request.type_name)
        res = self.session.execute(stmt).first()
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
        stmt = insert(Mailing).values(
            institute_id=request.institute_id,
            academic_type_id=request.academic_type_id,
            year=request.year,
            at=request.at,
            theme=request.theme,
            mailing_text=request.mailing_text,
        )
        self.session.execute(stmt)
        self.session.commit()

    def CreateQueue(
        self,
        request: apiv1.CreateQueueRequest,
        context: grpc.ServicerContext,
    ):
        stmt = insert(Queue).values(
            title=request.title,
            description=request.description,
            open=request.open,
            close=request.close,
        )
        self.session.execute(stmt)
        self.session.commit()
    
    def AddPersonToQueue(
        self,
        request: apiv1.AddPersonToQueueRequest,
        context: grpc.ServicerContext,
    ):
        stmt = select(Queue).where(Queue.queue_id == request.queue_id)
        res = self.session.execute(stmt).first()

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

        self.session.execute(stmt)
        self.session.commit()
        return apiv1.AddPersonToQueueResponse(is_active=is_active)
    
    def RemovePersonFromQueue(
        self,
        request: apiv1.RemovePersonFromQueueRequest,
        context: grpc.ServicerContext,
    ):
        # just throw if user already left queue
        stmt = delete(QueueToUser).where(
            and_(
                QueueToUser.user_id == request.user_id,
                QueueToUser.queue_id == request.queue_id,
            )
        )
        self.session.execute(stmt)
        self.session.commit()
    
    def PersonCompleteQueue(
        self,
        request: apiv1.PersonCompleteQueueRequest,
        context: grpc.ServicerContext,
    ):
        stmt = delete(QueueToUser).where(
            and_(
                QueueToUser.user_id == request.user_id,
                QueueToUser.queue_id == request.queue_id,
            )
        )
        self.session.execute(stmt)

        stmt = select(Queue).where(Queue.queue_id == request.queue_id)
        queue: Queue = self.session.execute(stmt).first()[0]

        key: Callable[[QueueToUser], datetime] = lambda qtu: qtu.joined
        sorted_qtu = sorted(queue.queue_to_user, key=key)

        is_queue_empty = (len(sorted_qtu) == 0)
        active_user_id = None if is_queue_empty else sorted_qtu[0].user_id

        stmt = update(Queue).where(Queue.queue_id == request.queue_id).values(
            active_user_id=active_user_id,
        )

        self.session.execute(stmt)
        self.session.commit()

        return apiv1.PersonCompleteQueueResponse(
            is_queue_empty=is_queue_empty,
            active_user_id=active_user_id,
        )
    
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
            request.defect.user_id,
            request.defect.defect_type,
            request.defect.description,
            request.defect.defect_status
        )
        for cell, value in zip(irange, values):
            cell.value = value

        self.worksheet.update_cells(irange)

    DEFECT_TYPE_MAP = {
        "Электрика": apiv1.ELECTRICITY,
        "Сантехника": apiv1.PLUMB,
        "Общее": apiv1.COMMON,
    }

    DEFECT_STATUS_MAP = {
        "Добавлено": apiv1.CREATED,
        "Принято": apiv1.ACCEPTED,
        "Решено": apiv1.RESOLVED,
    }

    def GetDefectById(
        self,
        request: apiv1.GetDefectByIdRequest,
        context: grpc.ServicerContext,
    ):
        column = self.worksheet.col_values(1)
        if request.defect.defect_id not in column:
            return apiv1.GetDefectByIdResponse()

        i = column.index(request.defect.defect_id) + 1
        irange: List[Cell] = self.worksheet.range(i, 2, i+4, 5)
        return apiv1.GetDefectByIdResponse(
            defect=apiv1.Defect(
                defect_id=irange[0].value,
                user_id=irange[1].value,
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
            request.defect.defect_type,
            request.defect.description,
            request.defect.defect_status
        )

        for cell, value in zip(irange, values):
            cell.value = value

        self.worksheet.update_cells(irange)
    
    def AssignDefect(
        self,
        request: apiv1.AssignDefectRequest,
        context: grpc.ServicerContext,
    ):
        stmt = (
            select(DormybobaUser)
            .join(DormybobaRole, DormybobaUser.role_id == DormybobaRole.role_id)
            .where(DormybobaRole.role_name == "admin")
        )
        res = self.session.execute(stmt).first()

        if res is None:
            return context.abort_with_status(grpc.StatusCode.INTERNAL)

        admin_user: DormybobaUser = res[0]

        return apiv1.AssignDefectResponse(assigned_user_id=admin_user.user_id)

    def _build_api_mailing_event(
        self,
        mailing: Mailing,
        users: List[DormybobaUser],
    ) -> apiv1.MailingEvent:
        api_mailing = apiv1.Mailing(
            theme=mailing.theme,
            mailing_text=mailing.mailing_text,
            at=mailing.at,
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

    def MailingEvent(
        self,
        request: Any,
        context: grpc.ServicerContext,
    ):
        events = []
        try:
            stmt = select(Mailing).where(
                or_(
                    Mailing.at == None,
                    datetime.now() > Mailing.at
                )
            )
            mailings = self.session.execute(stmt).all()
            # Only registered
            stmt = select(DormybobaUser).where(
                and_(
                    DormybobaUser.institute_id != None,
                    DormybobaUser.academic_type_id != None,
                    DormybobaUser.year != None,
                )
            )
            res = self.session.execute(stmt).all()
            users = list([row[0] for row in res])
            for row in mailings:
                mailing: Mailing = row[0]
                event = self._build_api_mailing_event(mailing, users)
                events.append(event)

                stmt = delete(Mailing).where(Mailing.mailing_id == mailing.mailing_id)
                self.session.execute(stmt)
                self.session.commit()
        except Exception as exc:
            print(exc)
        yield apiv1.MailingEventResponse(events=events)
        

    def _build_api_queue_event(
        self,
        queue: Queue,
        users: List[DormybobaUser],
    ) -> apiv1.QueueEvent:
        api_queue = apiv1.Queue(
            queue_id=queue.queue_id,
            title=queue.title,
            descritpion=queue.description,
            open=queue.open,
            close=queue.close,
        )

        api_users = []
        for row in users:
            user: DormybobaUser = row[0]
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

    def QueueEvent(
        self,
        request: Any,
        context: grpc.ServicerContext,
    ):
        events = []
        try:
            stmt = select(Queue).where(
                and_(
                    datetime.now() > Queue.open,
                    Queue.is_opened == False,
                )
            )
            queues = self.session.execute(stmt).all()
            stmt = select(DormybobaUser)
            res = self.session.execute(stmt).all()
            users = list([row[0] for row in res])

            for row in queues:
                queue: Queue = row[0]
                event = self._build_api_queue_event(queue, users)
                events.append(event)

                stmt = update(Queue).where(Queue.queue_id == queue.queue_id).values(
                    is_opened = True,
                )
                self.session.execute(stmt)
                self.session.commit()

        except Exception as exc:
            print(exc)
        yield apiv1.QueueEventResponse(events=events)

def serve(session: Session, worksheet: Worksheet):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    apiv1grpc.add_DormybobaCoreServicer_to_server(
        DormybobaCoreServicer(session, worksheet), server
    )
    logging.info("Starting server...")
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()