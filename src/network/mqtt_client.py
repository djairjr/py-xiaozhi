import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(
        self,
        server,
        port,
        username,
        password,
        subscribe_topic,
        publish_topic=None,
        client_id="PythonClient",
        on_connect=None,
        on_message=None,
        on_publish=None,
        on_disconnect=None,
    ):
        """Initialize the MqttClient instance.

        :param server: MQTT server address
        :param port: MQTT server port
        :param username: login username
        :param password: login password
        :param subscribe_topic: the topic to subscribe to
        :param publish_topic: published topic
        :param client_id: client ID, default is"PythonClient":param on_connect: Customized connection callback function
        :param on_message: Custom message receiving callback function
        :param on_publish: Custom message publishing callback function
        :param on_disconnect: Customized disconnect callback function"""
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic
        self.client_id = client_id

        # Create an MQTT client instance, using the latest API version
        self.client = mqtt.Client(client_id=self.client_id, protocol=mqtt.MQTTv5)

        # Set username and password
        self.client.username_pw_set(self.username, self.password)

        # Set the callback function. If a custom callback function is provided, use the custom one, otherwise use the default one.
        if on_connect:
            self.client.on_connect = on_connect
        else:
            self.client.on_connect = self._on_connect

        self.client.on_message = on_message if on_message else self._on_message
        self.client.on_publish = on_publish if on_publish else self._on_publish

        if on_disconnect:
            self.client.on_disconnect = on_disconnect
        else:
            self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        """The default connection callback function."""
        if rc == 0:
            print("✅ Successfully connected to MQTT server")
            # After successful connection, automatically subscribe to the topic
            client.subscribe(self.subscribe_topic)
            print(f"📥 Subscribed topic: {self.subscribe_topic}")
        else:
            print(f"❌ Connection failed, error code: {rc}")

    def _on_message(self, client, userdata, msg):
        """The default message receiving callback function."""
        topic = msg.topic
        content = msg.payload.decode()
        print(f"📩 Received message - Topic: {topic}, Content: {content}")

    def _on_publish(self, client, userdata, mid, properties=None):
        """The default message publishing callback function."""
        print(f"📤 The message has been published, message ID: {mid}")

    def _on_disconnect(self, client, userdata, rc, properties=None):
        """Default disconnect callback function."""
        print("🔌 The connection to the MQTT server has been lost")

    def connect(self):
        """Connect to MQTT server."""
        try:
            self.client.connect(self.server, self.port, 60)
            print(f"🔗 Connecting to server {self.server}:{self.port}")
        except Exception as e:
            print(f"❌ Connection failed, error: {e}")

    def start(self):
        """Start the client and start network looping."""
        self.client.loop_start()

    def publish(self, message):
        """Publish a message to the specified topic."""
        result = self.client.publish(self.publish_topic, message)
        status = result.rc
        if status == 0:
            print(f"✅ Successfully published to topic `{self.publish_topic}`")
        else:
            print(f"❌ Publish failed, error code: {status}")

    def stop(self):
        """Stop the network loop and disconnect."""
        self.client.loop_stop()
        self.client.disconnect()
        print("🛑 The client has stopped connecting")


if __name__ == "__main__":
    pass
    # Custom callback function
    # def custom_on_connect(client, userdata, flags, rc, properties=None):
    #     if rc == 0:
    # print("🎉 Custom callback: Successfully connected to MQTT server")ssfully connected to MQTT server")
    #         topic_data = userdata['subscribe_topic']
    #         client.subscribe(topic_data)
    # print(f"📥 Custom callback: Subscribed to topic: {topic_data}")d topic: {topic_data}")
    #     else:
    # print(f"❌ Custom callback: Connection failed, error code: {rc}")ection failed, error code: {rc}")
    #
    # def custom_on_message(client, userdata, msg):
    #     topic = msg.topic
    #     content = msg.payload.decode()
    # print(f"📩 Custom callback: Message received - topic: {topic}, content: {content}")c: {topic}, content: {content}")
    #
    # def custom_on_publish(client, userdata, mid, properties=None):
    # print(f"📤 Custom callback: message has been published, message ID: {mid}")has been published, message ID: {mid}")
    #
    # def custom_on_disconnect(client, userdata, rc, properties=None):
    # print("🔌 Custom callback: The connection to the MQTT server has been disconnected")ion to MQTT server disconnected")
    #
    # #Create an MqttClient instance and pass in the custom callback function
    # mqtt_client = MqttClient(
    #     server="8.130.181.98",
    #     port=1883,
    #     username="admin",
    #     password="dtwin@123",
    #     subscribe_topic="sensors/temperature/request",
    #     publish_topic="sensors/temperature/device_001/state",
    #     client_id="CustomClient",
    #     on_connect=custom_on_connect,
    #     on_message=custom_on_message,
    #     on_publish=custom_on_publish,
    #     on_disconnect=custom_on_disconnect
    # )
    #
    # # Pass subscription topic information as user data to the callback function
    # mqtt_client.client.user_data_set(
    #     {'subscribe_topic': mqtt_client.subscribe_topic}
    # )
    #
    # # Connect to MQTT server
    # mqtt_client.connect()
    #
    # # Start the client
    # mqtt_client.start()
    #
    # try:
    #     while True:
    # # Post a message
    # message = input("Enter the message to be published:")essage you want to publish:")
    #         mqtt_client.publish(message)
    # except KeyboardInterrupt:
    # print("\n⛔️ The program has stopped")gram has stopped")
    # finally:
    # # Stop and disconnect
    #     mqtt_client.stop()
