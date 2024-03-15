from typing import Any, Callable, Awaitable
import logging
import behave.runner as behave_runner
import grpc
import google.protobuf.json_format as gpjson

async def do_rpc(
    context: behave_runner.Context,
    rpc: Callable[[Any, Any], Awaitable[Any]],
    *args,
    **kwargs,
):
    try:
        context.response = await rpc(*args, **kwargs)
        context.json_response = gpjson.MessageToJson(context.response)
        context.status = grpc.StatusCode.OK
    except grpc.RpcError as exc:
        context.response = None
        context.json_response = ""
        context.status = exc.code()

    logging.info(f"Response is {context.json_response}")
    logging.info(f"Response status is {context.status}")
