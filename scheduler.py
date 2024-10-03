# #from kafka import KafkaProducer
# from apscheduler.schedulers.background import BackgroundScheduler
# from fastapi import BackgroundTasks
# import json
# import math 


# #connect kafka
# # producer = KafkaProducer(
# #     bootstrap_servers='127.0.0.1:9092',  # Replace with your Kafka server
# #     value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize to JSON
# # )

# provider_location = (20.301989663023086, 85.89449949653775)  # Starting point of the service provider
# user_location = (20.302151644569957, 85.89460877672701)    # Destination point (user location)
# step_size = 0.1  # How much the provider moves towards the user in each step
# user_phone_no="+917735319358"

# kafka_topic = 'location_updates'

# def move_towards(start, end, step_size):
#     x1, y1 = start
#     x2, y2 = end

#     distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

#     if distance == 0:
#         return start  # Already at the destination
#     step_ratio = step_size / distance

#     new_x = x1 + (x2 - x1) * step_ratio
#     new_y = y1 + (y2 - y1) * step_ratio

#     return new_x, new_y

# # Scheduler task to update location
# def update_location():
#     global provider_location

#     provider_location = move_towards(provider_location, user_location, step_size)
#     location_data = {
#         "provider_id": 1,
#         "location": provider_location,
#         "status": "moving"
#     }
#     print(location_data)

#     # Send data to Kafka
#     #producer.send(kafka_topic, location_data)
#     #print(f"Pushed to Kafka: {location_data}")

#     if provider_location == user_location:
#         print("Provider reached the user.")
#         scheduler.shutdown()

# def send_msg():
#     global provider_location
#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         from_='+12074779603',
#         body=provider_location,
#         to=user_phone_no
#     )

#     return f"message send to {user_phone_no}"

# scheduler = BackgroundScheduler()

# # Function to start the background scheduler task
# def start_scheduler():
#     scheduler.add_job(update_location, 'interval', seconds=1)
#     scheduler.add_job(send_msg, 'interval', seconds=10)
#     scheduler.start()
#     print()

# def start_simulation():
#     # Add the start_scheduler function as a background task
#     BackgroundTasks.add_task(start_scheduler)
#     return {"message": "Simulation started, moving towards user..."}

# print(start_scheduler())


import time
import math
from sms import send_msg
from location import get_distance


# Function to calculate next step towards user
def move_towards(start, end, step_size):
    x1, y1 = start
    x2, y2 = end
    
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    if distance == 0:
        return start  # Service provider already at user location
    
    # Calculate ratio of movement towards the user
    step_ratio = step_size / distance
    new_x = x1 + (x2 - x1) * step_ratio
    new_y = y1 + (y2 - y1) * step_ratio
    
    return [new_x, new_y]


# Simulation function
def simulate_movement(provider_location, user_location, step_size,user_number):
    seconds_passed = 0

    while provider_location != user_location:
        # Move the service provider towards the user
        provider_location = move_towards(provider_location, user_location, step_size)
        
        # Print the current location every second
        print(f"Service provider location: {provider_location}")
        s=f"Service provider location: {provider_location}"
        # Every 30 seconds, send a message to the user
        if seconds_passed % 10 == 0 and seconds_passed > 0:
            msg=f"Your Service provider is {get_distance(coord1=provider_location,coord2=user_location)} km away from you"
            send_msg(number="+"+str(user_number),msg=msg)
        
        # Increment seconds and sleep for 1 second
        time.sleep(1)
        seconds_passed += 1
        
        # Stop if the service provider reaches the user
        if provider_location == user_location:
            print("Service provider has reached the user.")
            break

# # Start the simulation
# if __name__ == "__main__":
#     # Get initial locations from user input
#     provider_location, user_location = get_locations()
    
#     # Define step size (how much the provider moves every second)
#     step_size = 0.1  # Change this if necessary for faster or slower movement
    
#     # Start the simulation
#     simulate_movement(provider_location, user_location, step_size,"+917735319358")
