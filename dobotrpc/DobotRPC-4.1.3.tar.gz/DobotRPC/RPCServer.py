import json
import demjson
import websockets
import asyncio
from websockets import WebSocketServerProtocol
from .Utils import loggers
from MessageCenter import message_center as mc
from typing import Any, NoReturn
from .NetworkError import NetworkError


LOGGER_NAME = "RPCServer"


class RPCServer(object):
    def __init__(self,
                 loop: asyncio.BaseEventLoop,
                 ip="0.0.0.0",
                 port=9091,
                 on_disconnected=None):
        self.__on_disconnected = on_disconnected
        self.__loop: asyncio.BaseEventLoop = loop
        self.__server_name = "DobotRPC-WSServer"

        self.__ban_list = (
            # "192.168.53.103",
            # "192.168.53.100"
        )
        self.__ws_client = None

        self.__rpc_id = 0
        self.__coroutines = {}
        self.__tasks = []
        self.__server = None

        async def init_worker() -> Any:
            nonlocal ip, port
            self.__server = await websockets.serve(
                self.__on_new_onnection,
                ip,
                port)

        self.__loop.run_until_complete(init_worker())

    def __del__(self):
        if self.__server:
            self.__server.close()
            self.__server.wait_closed()
            del self.__server

        self.__coroutines.clear()

    async def __call_worker(self, websocket, rpc_id, method, **params) -> None:
        try:
            rpc_result = await mc.call(method, **params)
            feedback = self.__pack_rpc(rpc_id, rpc_result)
        except Exception as e:
            feedback = self.__pack_rpc(rpc_id, e)

        loggers.get(LOGGER_NAME).debug(f"rpc server >>>> {feedback}")
        await websocket.send(feedback)

    async def __on_new_onnection(self, websocket: WebSocketServerProtocol,
                                 _) -> NoReturn:
        ip, port = websocket.remote_address
        if ip in self.__ban_list:
            loggers.get(LOGGER_NAME).warning(f"{ip} had been baned.")
            send_str = "You had been baned."
            loggers.get(LOGGER_NAME).debug(f"rpc server >>>> {send_str}")
            await websocket.send(send_str)
            return

        if self.__ws_client:
            loggers.get(LOGGER_NAME).warning(
                f"Client({ip}:{port}) try to connect. \
But refused by server.")
            send_str = f"{self.__server_name} has occupied"
            loggers.get(LOGGER_NAME).debug(f"rpc server >>>> {send_str}")
            await websocket.send(send_str)
            return

        loggers.get(LOGGER_NAME).info(f"Client({ip}:{port}) connected.")
        self.__ws_client = websocket

        while True:
            try:
                message = await websocket.recv()
                loggers.get(LOGGER_NAME).debug(f"rpc server <<<< {message}")
            except Exception as e:
                loggers.get(LOGGER_NAME).error(e, exc_info=True)
                break

            try:
                # result和error字段暂时不使用
                # 因为作为服务端不主动调用客户端
                rpc_id, method, params, _, _ = self.__unpack_rpc(
                    message)

                if "dobotlink" not in method:
                    # dobotlink的数据尽管透传
                    method = self.__convert_lower_case_name(method)
                    params = self.__convert_lower_case_params(params)

                self.__loop.create_task(
                    self.__call_worker(websocket, rpc_id, method, **params))
            except Exception as e:
                loggers.get(LOGGER_NAME).error(e, exc_info=True)
                loggers.get(LOGGER_NAME).debug(f"rpc server >>>> {e}")
                await websocket.send(str(e))
                continue

        loggers.get(LOGGER_NAME).warning("GUI had disconnected!!!!!!!!")
        self.__ws_client = None

        if self.__on_disconnected:
            await self.__on_disconnected()

    def __unpack_rpc(self, message: str) -> (int, str, str, str, Exception):
        try:
            data = json.loads(message)
        except Exception as e:
            raise NetworkError.InvaildJsonMsg(e)

        rpc_id = data.get("id", None)
        if type(rpc_id) is not int:
            raise NetworkError.RpcIdInvaild()

        rpc_verison = data.get("jsonrpc", None)
        if rpc_verison != "2.0":
            raise NetworkError.RpcVersionInvaild()

        method = data.get("method", None)
        params = data.get("params", None)
        result = data.get("result", None)
        error = data.get("error", None)
        if error:
            error = Exception(error)

        return rpc_id, method, params, result, error

    def __pack_rpc(self, rpc_id: int, rpc_playload: Any,
                   method: str = None) -> str:
        if rpc_id is None:
            data = {"jsonrpc": "2.0"}
        else:
            data = {"id": rpc_id, "jsonrpc": "2.0"}

        if method:
            data["method"] = method
            data["params"] = rpc_playload
        else:
            if isinstance(rpc_playload, Exception):
                # TODO: 所有异常捕捉并处理
                error_str = str(rpc_playload)
                if "code" in error_str:
                    rpc_playload = demjson.decode(error_str)
                else:
                    rpc_playload = {
                        "code": -32000,
                        "message": f"VM >> {error_str}"
                    }
                loggers.get(LOGGER_NAME).error(rpc_playload, exc_info=True)
                data["error"] = rpc_playload
            else:
                data["result"] = rpc_playload

        rpc_packet = json.dumps(data)
        return rpc_packet

    def __convert_lower_case_name(self, name):
        lst = []
        last_char_flag = False
        for char in name:
            if last_char_flag and char.isupper():
                lst.append("_")
            lst.append(char)

            if char == ".":
                last_char_flag = False
            else:
                last_char_flag = True

        return "".join(lst).lower()

    def __convert_lower_case_params(self, params):
        params = {} if params is None else params
        new_params = {}
        for key, value in params.items():
            key = self.__convert_lower_case_name(key)
            new_params[key] = value

        return new_params

    @property
    def is_connected(self) -> bool:
        return self.__ws_client is not None

    async def notify(self, method: str, data: Any) -> Any:
        if self.__ws_client is None:
            raise Exception("Had not connected!")

        rpc_packet = self.__pack_rpc(None, data, method)
        loggers.get(LOGGER_NAME).debug(f"rpc server >>>> {rpc_packet}")
        await self.__ws_client.send(rpc_packet)
