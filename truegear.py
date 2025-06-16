from websocket import create_connection # pip install websocket,websocket_client
from threading import Lock, Thread
import websocket
import socket
import json
import time
import base64
import sys

class TruegearPlayerClient:
    _effectSeek = {}
    _url = "ws://127.0.0.1:18233/v1/tact/"

    def __init__(self, _appId, _apiKey):
        self.appId = _appId
        self.apiKey = _apiKey
        self._ws_lock = Lock()
        self._ws = None

        self._worker_thread = None
        self._active = False  # 开启启动websocket的开关。
        self._cur = 1

    def _Create_RegisteApp(self):
        base64_bytes = base64.b64encode((self.appId + ";" + self.apiKey).encode())
        base64_string = base64_bytes.decode("ascii")
        msg = {
                "Method" : "register_app",
                "ReqId": self._cur,
                "Body" : base64_string
            }
        self._cur += 1
        print(msg)
        return json.dumps(msg)

    def _Create_SeekEffectObject_byUUid(self,  uuid):
        base64_bytes = base64.b64encode((self.appId + ";" + uuid).encode())
        base64_string = base64_bytes.decode("ascii")
        msg = {
            "Method" : "seek_by_uuid",
            "ReqId": self._cur,
            "Body" : base64_string
        }
        self._cur += 1
        print(msg)
        return json.dumps(msg)

    def _Create_PlayEffectByUuid(self,  uuid):
        base64_bytes = base64.b64encode((self.appId + ";" + uuid).encode())
        base64_string = base64_bytes.decode("ascii")
        msg = {
            "Method" : "play_effect_by_uuid",
            "ReqId": self._cur,
            "Body" : base64_string 
        }
        self._cur += 1
        print(msg)
        return json.dumps(msg)

    def _Create_PlayEffectByEffectObject(self, effectObject):
        base64_bytes = base64.b64encode(json.dumps(effectObject).encode())
        base64_string = base64_bytes.decode("ascii")
        msg = {
            "Method" : "play_effect_by_content",
            "ReqId": self.cur,
            "Body" : base64_string
        }
        self._cur += 1
        print(msg)
        return json.dumps(msg)

    def start(self):
        self._active = True
        self._worker_thread = Thread(target=self._run)
        self._worker_thread.start()
        print("start")

    def send_play(self, uuid):
        obj = self._Create_PlayEffectByUuid( uuid)
        self._send_msg(obj)

    def send_play_effect_by_content(self, eff_obj):
        obj = self._Create_PlayEffectByEffectObject( eff_obj)
        self._send_msg(obj)

    def send_seek_effect(self, uuid):
        obj = self._Create_SeekEffectObject_byUUid( uuid)
        self._send_msg(obj)

    def pre_seek_effect(self, uuid):
        self._effectSeek[uuid] = True

    def find_effect_by_uuid(self, uuid):
        return self._effectSeek.get(uuid, None)

    def _send_msg(self, text):
        ws = self._ws
        if ws:
            ws.send(text)

    def get_status(self):
        return True if self._ws is not None else False

    def close(self):
        self._active = False
        if self._ws_lock.locked():
            self._ws_lock.release()
        #self._worker_thread.join()
        self._disconnect()

    def _ensure_connection(self, try_num):
        if try_num > 3 and self._ws is None:
            self.close()
            return

        triggered = False
        with self._ws_lock:
            if self._ws is None:
                self._ws = create_connection(self._url)
                triggered = True

        if triggered:
            self.on_open()

    def _disconnect(self):
        triggered = False
        with self._ws_lock:
            if self._ws:
                ws: websocket.WebSocket = self._ws
                self._ws = None
                triggered = True
        if triggered:
            ws.close()
            self.on_close()

    def _run(self):
        try_num = 0
        try:
            while self._active:
                try:
                    try_num += 1
                    self._ensure_connection(try_num)
                    ws = self._ws
                    if ws:
                        text = ws.recv()
                        if not text:
                            self._disconnect()
                            continue
                        self.on_msg(text)
                    else:
                        time.sleep(2)
 
                except (websocket.WebSocketConnectionClosedException, socket.error):
                    self._disconnect()
                except:
                    et, ev, tb = sys.exc_info()
                    self.on_error(et, ev, tb)
                    self._disconnect()  #
        except:
            et, ev, tb = sys.exc_info()
            self.on_error(et, ev, tb)

        self._disconnect()
    
    def on_close(self):
        print("on close")

    def on_open(self):
        print("on open")
        obj = self._Create_RegisteApp()
        self._send_msg(obj)

    def on_msg(self, data: str):
        print("on msg")
        data = json.loads(data)
        print(data)
        body = base64.b64decode(data["Result"])
        if data["Method"] == "register_app":
            self._register_app()

        if body is not None and len(body) > 0:
            if data["Method"] == "seek_by_uuid":
                self._seek_by_uuid(body)

    def on_error(self, exception_type, exception_value: Exception, tb):
        return sys.excepthook(exception_type, exception_value, tb)
    
    def _register_app(self):
        for line in self._effectSeek.keys():
            obj = self.send_seek_effect(line)
            self._send_msg(obj)

    def _seek_by_uuid(self, body):
        print  ("seek by uuid", body)
        obj = json.loads(body)
        self._effectSeek[obj["uuid"]] = obj

if __name__ == "__main__":
    test_ws = TruegearPlayerClient(_appId = "1540210", _apiKey = "test")
    test_ws.pre_seek_effect("DefaultDamage")
    test_ws.start()
    time.sleep(5)
    test_ws.send_seek_effect("DefaultDamage")
    time.sleep(5)
    test_ws.send_play("DefaultDamage")
    time.sleep(5)
    t = test_ws.find_effect_by_uuid("DefaultDamage")
    print(t)
    test_ws.send_play_effect_by_content(t)