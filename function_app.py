import azure.functions as func
import datetime
import json
import logging
import time
from azure.iot.device import IoTHubDeviceClient, Message

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def TimerTrigger(myTimer: func.TimerRequest) -> None:

    # Azure IoT Hub 연결 문자열
    CONNECTION_STRING = ""

    # 메시지를 전송할 디바이스 클라이언트 생성
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # 연결
    device_client.connect()

    try:
        # 전송할 메시지 생성
        message = Message("Hello from Python!")

        # 메시지 속성 설정 (옵션)
        message.custom_properties["temperature"] = "27.3"
        message.custom_properties["humidity"] = "60.5"


        # 메시지 전송
        device_client.send_message(message)
        print("Message sent: {}".format(message))

        # 일정 간격으로 메시지 전송을 반복하려면 sleep을 사용할 수 있습니다.
        time.sleep(5)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")

    # 연결 종료
    device_client.disconnect()

    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')