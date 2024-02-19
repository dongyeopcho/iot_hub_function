import azure.functions as func
import json
import logging

from azure.iot.device import IoTHubDeviceClient

app = func.FunctionApp()

# Learn more at aka.ms/pythonprogrammingmodel

# Get started by running the following code to create a function using a HTTP trigger.

@app.function_name(name="reservation_http_trigger")
@app.route(route="reservation_http_trigger")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    CONNECTION_STRING = req_body.get("CONNECTION_STRING")
    DEVICE_ID = req_body.get("DEVICE_ID")
    RESERVATION_METHOD = req_body.get("RESERVATION_METHOD")

    # 메시지를 전송할 디바이스 클라이언트 생성
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # 연결
    device_client.connect()

    # 메시지 생성
    json_message = {
        "reserve_user_id" : "1",
        "reserve_device_id" : DEVICE_ID,
        "reservation_method" : RESERVATION_METHOD, # KIOSK, VIEW, WEB, APP 
        "reservation_datetime" : "reservation_datetime_string",
        "reservation_participants" : 3,
        "current_datetime" : "current_datetime_str"
    }
    
    str_message = json.dumps(json_message)
    print("Message sent: {}".format(str_message))
    
    # 연결 종료9
    device_client.disconnect()
    logging.info('Python http trigger function executed.')

    # 메시지 전송
    device_client.send_message(str_message)

    return func.HttpResponse(f"Hello, {DEVICE_ID}. This HTTP triggered function executed successfully.")