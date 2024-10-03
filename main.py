from fastapi import FastAPI,Request,Depends
from sqlalchemy.orm import Session
import json
from service_prov import clean_string,list_num,create_service_provider,add_user_request,get_all_service_provider,get_shortest_service_provider,send_service_request,accept_service_request
from sms import send_msg
from database import engine
from models import Base
from location import get_address
import database
from pydantic import BaseModel
#from kafka import KafkaProducer
from apscheduler.schedulers.background import BackgroundScheduler
import requests



# Create an instance of FastAPI
app = FastAPI()


# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define a simple route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Define another route that accepts a path parameter
@app.post("/sms")
async def read_item(request: Request,db: Session = Depends(get_db)):
    form_data = await request.form()
    from_number = form_data.get("From")
    body = form_data.get("Body")

    if "mayday401" in body:
        #if "yes" in body or "Yes" in body:
        print(accept_service_request(db=db,service_provider_no=from_number))
        # else:
        #     pass

    else:

        api_key="OPENAI_API_KEY"
        endpoint = 'https://api.openai.com/v1/chat/completions'

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        functions = [
            {
                "name": "emergency_response",
                "description": "Responds to emergency situations with service assignment, precautionary steps, and visual representation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service": {
                            "type": "string",
                            "description": "Category of the helper (Ambulance, Police, etc.)"
                        },
                        "precautionary_steps": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Safety instructions to follow while waiting for help ."
                        },
                        "longitude": {
                            "type": "number",
                            "description": "Extracted longitude or null."
                        },
                        "latitude": {
                            "type": "number",
                            "description": "Extracted latitude or null."
                        },
                        "location": {
                            "type": "string",
                            "description": "Extracted general location or null."
                        }
                    },
                    "required": ["service", "precautionary_steps", "longitude", "latitude", "location"]
                }
            }
        ]


        user_query = body  # Example user query

        data = {
            'model': 'gpt-4o-mini',  # Use the appropriate model
            'messages': [
                {'role': 'user', 'content': user_query}
            ],
            'functions': functions,
            'function_call': {"name": "emergency_response"}  # Specify the function to call
        }

        response = requests.post(endpoint, headers=headers, json=data)

        # Get the JSON response
        json_response = response.json()

        # Print the JSON output
        service =json.loads(json_response["choices"][0]["message"]["function_call"]["arguments"])
        print(service)
        print(type(service))
        #service = json.loads(chat_completion.choices[0].message.content)
        print(service)

        msg = f'''
        Hey we rechived your message we are sending {service["service"]} as soon as possiable.
        before we send the {service["service"]} please follow this steps
        {list_num(service["precautionary_steps"])}

        Thank You'''
        x=""
        #add request to database
        print("request added ",add_user_request(db=db,request=body,request_service=service["service"],request_phone_no=from_number,location=service["location"],long=service["longitude"],lat=service["latitude"]))
        if clean_string(service["service"]) == "police":

            print(send_msg(number=from_number,msg=msg))
            service_provider = get_shortest_service_provider(db=db,user_lat=service["latitude"],user_lon=service["longitude"],service_type="police")
            if service_provider != "":
                print(service_provider)
                if service["location"] != "null":
                    user_location = get_address(lat=service["latitude"],long=service["longitude"])
                    print(send_service_request(db=db,service_provider_id=service_provider.service_provioder_id,user_location=user_location,user_phone=from_number))
                else:
                    print(send_service_request(service_provider_id=service_provider.service_provioder_id,user_location=service["location"],user_phone=from_number,db=db))

        if clean_string(service["service"]) == "ambulance":
            print(send_msg(number=from_number,msg=msg))
            service_provider = get_shortest_service_provider(db=db,user_lat=service["latitude"],user_lon=service["longitude"],service_type="ambulance")
            if service_provider != "":
                print(service_provider)
                if service["location"] != "null":
                    user_location = get_address(lat=service["latitude"],long=service["longitude"])
                    print(send_service_request(db=db,service_provider_id=service_provider.service_provioder_id,user_location=user_location,user_phone=from_number))
                else:
                    print(send_service_request(service_provider_id=service_provider.service_provioder_id,user_location=service["location"],user_phone=from_number,db=db))

        if clean_string(service["service"]) == "disastermanagementteam":
            print(send_msg(number=from_number,msg=msg))
            service_provider = get_shortest_service_provider(db=db,user_lat=service["latitude"],user_lon=service["longitude"],service_type="disastermanagementteam")
            if service_provider != "":
                print(service_provider)
                if service["location"] != "null":
                    user_location = get_address(lat=service["latitude"],long=service["longitude"])
                    print(send_service_request(db=db,service_provider_id=service_provider.service_provioder_id,user_location=user_location,user_phone=from_number))
                else:
                    print(send_service_request(service_provider_id=service_provider.service_provioder_id,user_location=service["location"],user_phone=from_number,db=db))
        if clean_string(service["service"]) == "firepolice":
            print(send_msg(number=from_number,msg=msg))
            service_provider = get_shortest_service_provider(db=db,user_lat=service["latitude"],user_lon=service["longitude"],service_type="disastermanagementteam")
            if service_provider != "":
                print(service_provider)
                if service["location"] != "null":
                    user_location = get_address(lat=service["latitude"],long=service["longitude"])
                    print(send_service_request(db=db,service_provider_id=service_provider.service_provioder_id,user_location=user_location,user_phone=from_number))
                else:
                    print(send_service_request(service_provider_id=service_provider.service_provioder_id,user_location=service["location"],user_phone=from_number,db=db))



        # Log or process the message received


        # Respond back to the sender (optional)
        # response = MessagingResponse()
        # response.message(f"Thanks for your message, {from_number}!")

        return {"data":x}


@app.get("/add_service")
def addservice(db: Session = Depends(get_db)):
    create_service_provider(db=db,service_provider_name="Satyasuman",service="police",service_provider_status=0,service_provider_phone_no="+916371744525",service_provider_vechil_no="ODO7 4567",service_provider_location_lat=20.298756072801243,service_provider_location_long=85.8933521540178)

@app.get("/allserviceprovider")
def getalluser(db: Session = Depends(get_db)):
    return get_all_service_provider(db)