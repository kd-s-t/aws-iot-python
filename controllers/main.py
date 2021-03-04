from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import RPi.GPIO as GPIO
import json

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a2b0xwckvjuafw-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "test6"
PATH_TO_CERT = "certs/06f142bc14-certificate.pem.crt"
PATH_TO_KEY = "certs/06f142bc14-private.pem.key"
PATH_TO_ROOT = "certs/AmazonRootCA1.pem"

pin = 17
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)

class Main:

    def subscribe(self):
        def response(self, params, packet):
            status = ''
            print('Received message from AWS IoT Core')
            print('Topic: '+packet.topic)
            print(packet.payload)
            data = json.loads(packet.payload)
            print('Payload: ', data['switch'])
            if data['switch'] == 1:
                status = 'close'
                GPIO.setup(pin, GPIO.LOW)
                print("low")
            if data['switch'] == 0:
                status = 'open'
                GPIO.setup(pin, GPIO.HIGH)
                print("high")
            print("done")

        def online(self, params, packet):
            print('Received message from React Native')
            print('Topic: '+packet.topic)
            print(packet.payload)
            myMQTTClient.publish(
                topic="smartbank/connection",
                QoS=0,
                payload='{"message":"Yes"}'
            )

        # For certificate based connection
        myMQTTClient = AWSIoTMQTTClient(CLIENT_ID)
        # For TLS mutual authentication
        myMQTTClient.configureEndpoint(ENDPOINT, 8883) #Provide your AWS IoT Core endpoint (Example: "abcdef12345-ats.iot.us-east-1.amazonaws.com")
        myMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT) #Set path for Root CA and provisioning claim credentials
        myMQTTClient.configureOfflinePublishQueueing(-1)
        myMQTTClient.configureDrainingFrequency(2)
        myMQTTClient.configureConnectDisconnectTimeout(10)
        myMQTTClient.configureMQTTOperationTimeout(5)
        GPIO.setup(pin, GPIO.HIGH)
        
        print('Connecting...')
        myMQTTClient.connect()
        print('Connected.')
        print('Listening...')
        myMQTTClient.subscribe('smartbank/check', 1, online)
        myMQTTClient.subscribe('smartbank/switch', 1, response)

    def publish(self):
        print('Publishing...')
        myMQTTClient.publish(
            topic="smartbank/switch",
            QoS=1,
            payload='{"Message":"nothing"}'
        )