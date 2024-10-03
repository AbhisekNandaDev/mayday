# models.py
from enum import unique
from operator import index
from pickle import TUPLE

from sqlalchemy import Column, Integer, String,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class ServiceProvider(Base):
    __tablename__ = "service_provider"

    service_provioder_id = Column(Integer, primary_key=True,unique=True, index=True)
    service_provider_name = Column(String, index=True)
    service = Column(String, index=True)
    service_provider_status = Column(Integer,index=True) # 0 if free 1 if in enquery 2 if busy
    service_provider_phone_no = Column(Integer,index=True)
    service_provider_vechil_no = Column(Integer, index=True)
    service_provider_location_lat = Column(Integer,index=True)
    service_provider_location_long = Column(Integer,index=True)

class UserRequest(Base):
    __tablename__ = "user_request"
    request_id=Column(Integer, primary_key=True,unique=True, index=True)
    request=Column(String,index=True)
    request_service=Column(String,index=True)
    request_phone_no=Column(Integer,index=True)
    location=Column(String,index=True)
    long = Column(Integer,index=True)
    lat= Column(Integer,index=True)

class LiveService(Base):
    __tablename__ = "live_service"

    live_service_id = Column(Integer,primary_key=True,unique=True, index=True)
    service_provioder_id = Column(Integer, ForeignKey("service_provider.service_provioder_id"), unique=True, index=True)
    user_phone_no = Column(Integer,index=True)


class SendRequestServiceProvider(Base):
    __tablename__ = "send_request_service_provider"

    id = Column(Integer, primary_key=True,unique=True, index=True)
    service_provioder_id = Column(Integer, ForeignKey("service_provider.service_provioder_id"), unique=True, index=True)
    user_phone_no = Column(Integer,index=True)
    send_sms_to_service = Column(Integer,index=True)
    accept_reject = Column(Integer,index=True) #0 send request 1 accpet request
