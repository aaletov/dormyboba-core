from behave import use_fixture
import behave.runner as behave_runner
import grpc
import sqlalchemy
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
import dormyboba_core.model as model

TEST_CORE_ADDR = "localhost:50051"
TEST_DB_ADDR = f"postgresql+psycopg2://postgres:123456@localhost:5432/dormyboba"

def before_all(context: behave_runner.Context):
    channel = grpc.aio.insecure_channel(TEST_CORE_ADDR)
    stub = apiv1grpc.DormybobaCoreStub(channel)
    context.stub = stub

    context.engine = sqlalchemy.create_engine(TEST_DB_ADDR, connect_args={"connect_timeout": 30})

def before_scenario(context: behave_runner.Context, scenario):
    model.Base.metadata.create_all(context.engine)

def after_scenario(context: behave_runner.Context, scenario):
    model.Base.metadata.drop_all(context.engine)
