import behave.runner as behave_runner
import grpc
import sqlalchemy
import dormyboba_api.v1api_pb2_grpc as apiv1grpc

TEST_CORE_ADDR = "dormyboba_core:50051"
TEST_DB_ADDR = f"postgresql+psycopg2://postgres:123456@postgresql/dormyboba"

def before_all(context: behave_runner.Context):
    channel = grpc.aio.insecure_channel(TEST_CORE_ADDR)
    stub = apiv1grpc.DormybobaCoreStub(channel)
    context.stub = stub

    context.engine = sqlalchemy.create_engine(TEST_DB_ADDR)
