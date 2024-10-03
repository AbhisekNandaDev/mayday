from twilio.rest import Client

account_sid = 'ACac93b7aaef7c708ff0250974d0fbb367'
auth_token = '442bcadf4a9191a28ce1ad448ea91998'
client = Client(account_sid, auth_token)
#
# message = client.messages.create(
#   from_='+447480569331',
#   body='welcome onboard',
#   to='+917735319358'
# )
#
# print(message.sid)
#
def send_msg(number,msg):
  client = Client(account_sid, auth_token)

  message = client.messages.create(
    from_='+12074779603',
    body=msg,
    to=number
  )

  return f"message send to {number}"

# Download the helper library from https://www.twilio.com/docs/python/install
# import os
# from twilio.rest import Client
#
# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure
# account_sid = 'ACac93b7aaef7c708ff0250974d0fbb367'
# auth_token = '442bcadf4a9191a28ce1ad448ea91998'
# client = Client(account_sid, auth_token)
#
# message = client.messages.create(
#     messaging_service_sid="MGd9345da3e226081a28d6456ac2553fff",
#     to="+15558675310",
#     body="This will be the body of the new message!",
# )
#
# print(message.body)