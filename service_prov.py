import string

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import threading

import models
from models import ServiceProvider,SendRequestServiceProvider,LiveService,UserRequest
from sms import send_msg
from scheduler import simulate_movement
from fastapi import BackgroundTasks


def clean_string(input_string):
    # Remove punctuation
    cleaned_string = input_string.translate(str.maketrans('', '', string.punctuation))
    # Remove spaces and convert to lowercase
    cleaned_string = cleaned_string.replace(" ", "").lower()
    return cleaned_string

def book_service(service,user,service_prov):

    return "x"

def create_service_provider(db: Session, service_provider_name: str, service: str,service_provider_status: str,service_provider_phone_no: str,service_provider_vechil_no: str,service_provider_location_lat: int,service_provider_location_long: int):
    new_user = models.ServiceProvider(service_provider_name=service_provider_name, service=service,service_provider_status=service_provider_status,service_provider_phone_no=service_provider_phone_no,service_provider_vechil_no=service_provider_vechil_no,service_provider_location_lat=service_provider_location_lat,service_provider_location_long=service_provider_location_long)

    # Add the new user to the database session
    db.add(new_user)

    # Commit the changes to the database
    db.commit()

    # Refresh the instance with the data from the database
    db.refresh(new_user)

    # Return the newly created user
    return new_user

def get_all_service_provider(db: Session):
    return db.query(ServiceProvider).all()

def get_shortest_service_provider(db: Session,user_lat,user_lon,service_type):
    user_lat = user_lat  # Replace with the user's latitude
    user_lon = user_lon  # Replace with the user's longitude

    # Query to find the closest service provider including service type
    haversine_query = (
        db.query(
            ServiceProvider.service_provioder_id,
            ServiceProvider.service_provider_name,
            ServiceProvider.service,
            (
                    6371000 *  # Radius of the Earth in meters
                    func.acos(
                        func.sin(func.radians(user_lat)) * func.sin(func.radians(ServiceProvider.service_provider_location_lat)) +
                        func.cos(func.radians(user_lat)) * func.cos(func.radians(ServiceProvider.service_provider_location_lat)) *
                        func.cos(func.radians(ServiceProvider.service_provider_location_long) - func.radians(user_lon))
                    )
            ).label('distance')
        )
        .filter(
            # Filter for a distance within a certain range (e.g., 10 km)
            6371000 * func.acos(
                func.sin(func.radians(user_lat)) * func.sin(func.radians(ServiceProvider.service_provider_location_lat)) +
                func.cos(func.radians(user_lat)) * func.cos(func.radians(ServiceProvider.service_provider_location_lat)) *
                func.cos(func.radians(ServiceProvider.service_provider_location_long) - func.radians(user_lon))
            ) < 10000  # 10 km
        )
        .order_by('distance')
        .limit(1)
        .one_or_none()
    )

    if haversine_query:
        return haversine_query
    else:
        return ""

def send_service_request(db: Session,service_provider_id,user_phone,user_location):
    #extract no from id
    service_provider = db.query(ServiceProvider).filter(ServiceProvider.service_provioder_id == service_provider_id).first()
    msg=f"""
    There is a emergency in """+user_location+""" get ready for the service user phone no :- """+user_phone+"""user_location:- """+user_location

    send_msg("+"+str(service_provider.service_provider_phone_no),msg)
    service_provider.service_provider_status = 1
    db.commit()  # Save the changes to the database
    db.refresh(service_provider)
    try:
        send_request=models.SendRequestServiceProvider(service_provioder_id=service_provider_id,user_phone_no=user_phone,send_sms_to_service=1,accept_reject=0)
        db.add(send_request)
        db.commit()
        db.refresh(send_request)
    except:
        pass

    return "Message already send successfully."

# def start_simulator(user,service,user_number,step_size=1):
#     back_ground_task=BackgroundTasks()
#     #simulate_movement(user_location=[user_long,user_lat],provider_location=[service_prov_lat,service_prov_long],step_size=step_size)
#     back_ground_task.add_task(simulate_movement, user, service, step_size,user_number)

back_ground_task=BackgroundTasks()
def accept_service_request(db: Session,service_provider_no):

    #get service provider details
    service_provider = db.query(ServiceProvider).filter(ServiceProvider.service_provider_phone_no == service_provider_no).first()
    user_phone_number = db.query(SendRequestServiceProvider).filter(SendRequestServiceProvider.service_provioder_id == service_provider.service_provioder_id).first().user_phone_no
    
    msg=f"""
    We are sending {service_provider.service_provider_name} with Vechile No. {service_provider.service_provider_vechil_no} to you soon
    """
    live_request = models.LiveService(service_provioder_id=service_provider.service_provioder_id,user_phone_no=user_phone_number)
    
    send_msg(number="+"+str(user_phone_number),msg=msg)
    
    user=db.query(UserRequest).filter(UserRequest.request_phone_no==user_phone_number).first()
    user_location=[user.lat,user.long]
    print("user",user_location)
    user_number=user_phone_number
    service_prov_location = [service_provider.service_provider_location_lat,service_provider.service_provider_location_long]
    print("service",service_prov_location)
    #start_simulator(user=user_location,service=service_prov_location,step_size=1,user_number=user_phone_number)
    #back_ground_task.add_task(simulate_movement,[user.lat,user.long], service_prov_location, 1,user_number)
    thread = threading.Thread(target=simulate_movement, args=([user.lat,user.long], service_prov_location, 0.1,user_number))
    thread.start()
    return "Message send to user"

def list_num(lst):
    count=1
    x=""
    for i in lst:
        x = x +"\n"+str(count)+"."+i
        count=count+1
    
    return x

def add_user_request(db: Session, request,request_service,request_phone_no,location,lat,long):
    new_request = models.UserRequest(request=request, request_service=request_service,request_phone_no=request_phone_no,location=location,lat=lat,long=long)

    # Add the new user to the database session
    db.add(new_request)

    # Commit the changes to the database
    db.commit()

    # Refresh the instance with the data from the database
    db.refresh(new_request)

    # Return the newly created user
    return new_request




