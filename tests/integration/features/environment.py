import grpc
import dormyboba_api.v1api_pb2_grpc as apiv1grpc

TEST_CORE_ADDR = "dormyboba_core:50051"

def before_all(context):
    channel = grpc.aio.insecure_channel(TEST_CORE_ADDR)
    stub = apiv1grpc.DormybobaCoreStub(channel)
    context.stub = stub