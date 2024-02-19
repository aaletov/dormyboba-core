import logging
from concurrent import futures
import grpc
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
from .service import DormybobaCoreServicer

class DormybobaServer:
    def __init__(self, dormyboba_service: DormybobaCoreServicer):
        self.logger = logging.getLogger('dormyboba')
        self.dormyboba_servicer = dormyboba_service

    async def run(self) -> None:
        server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
        apiv1grpc.add_DormybobaCoreServicer_to_server(self.dormyboba_servicer, server)

        self.logger.info("Starting server...")
        server.add_insecure_port("[::]:50051")
        await server.start()
        await server.wait_for_termination()
