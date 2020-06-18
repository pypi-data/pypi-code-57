import paho.mqtt.client as mqtt
import uuid


class MQTTConnectHelper:
    def __init__(self, host, port, username, password, keepalive=60):
        self.connect_callback = None
        clientid_uuid = "client-" + str(uuid.uuid1())
        self.client = mqtt.Client(clientid_uuid)
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect_callback
        self.client.connect(host, port, keepalive)

    def on_connect_callback(self, client, userdata, flags, rc):
        ret = ""
        if rc == 0:
            ret += "连接成功"
        elif rc == 1:
            ret += "连接拒绝(无效的版本或协议)"
        elif rc == 2:
            ret += "连接无效(无效的clientID和identifier标识符)"
        elif rc == 3:
            ret += "连接拒绝(主机不可用)"
        elif rc == 4:
            ret += "连接拒绝(无效的用户名或密码)"
        elif rc == 5:
            ret += "连接拒绝(无效认证)"
        else:
            ret += "其它"
        if self.connect_callback:
            self.connect_callback(client, userdata, flags, rc)
        print(ret)

    def on_connect(self, func):
        self.connect_callback = func

    def on_message(self, func):
        self.client.on_message = func

    def on_disconnect(self, func):
        self.client.on_disconnect = func

    def subscribe(self, topic):
        self.client.subscribe(topic=topic)

    def publish(self, topic, msg):
        self.client.publish(topic, msg)

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def loo(self):
        self.client.loop_forever()
if __name__ == "__main__":
    import time
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    # 连接EMQX服务器，host,port,username,password
    mqttHelper = MQTTConnectHelper("xx", 111, "xx", "xx")
    # 连接回调函数
    mqttHelper.on_connect(None)
    # 消息接收函数
    mqttHelper.on_message(on_message)
    # 订阅主题client/1
    mqttHelper.subscribe("client/1")
    # 向主题上client/1发送消息123
    mqttHelper.publish("client/1", "123")
    # 开始运行
    mqttHelper.start()
    time.sleep(5)
    # 停止运行
    mqttHelper.stop()