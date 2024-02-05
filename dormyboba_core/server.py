import random
from concurrent import futures
import logging
import grpc
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
import dormyboba_api as apiv1
from .model.generated import DormybobaUser, DormybobaRole, VerificationCode

class DormybobaCoreServicer(apiv1.DormybobaCoreServicer):
    """Provides methods that implement functionality of dormyboba-core server."""
    
    def __init__(self, session: Session):
        self.session = session        

    def GenerateVerificationCode(
            self,
            request: apiv1.GenerateVerificationCodeRequest,
            context,
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

        response = apiv1.GenerateVerificationCodeResponse()
        response.verification_code = code
        return response
    
    def GetRoleByVerificationCode(self, request, context):
        return super().GetRoleByVerificationCode(request, context)
    
    def CreateUser(self, request, context):
        return super().CreateUser(request, context)
    
    def GetAllInstitutes(self, request, context):
        return super().GetAllInstitutes(request, context)

    def GetInstituteByName(self, request, context):
        return super().GetInstituteByName(request, context)
    
    def GetAcademicTypeByName(self, request, context):
        return super().GetAcademicTypeByName(request, context)
    
    def CreateMailing(self, request, context):
        return super().CreateMailing(request, context)

    def CreateQueue(self, request, context):
        return super().CreateQueue(request, context)
    
    def AddPersonToQueue(self, request, context):
        return super().AddPersonToQueue(request, context)
    
    def RemovePersonFromQueue(self, request, context):
        return super().RemovePersonFromQueue(request, context)
    
    def PersonCompleteQueue(self, request, context):
        return super().PersonCompleteQueue(request, context)
    
    def AssignDefect(self, request, context):
        return super().AssignDefect(request, context)
    
def serve(session: Session):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    apiv1.add_DormybobaCoreServicer_to_server(
        DormybobaCoreServicer(session), server
    )
    logging.info("Starting server...")
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()