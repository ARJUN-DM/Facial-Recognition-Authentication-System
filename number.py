import os
from twilio.rest import Client
import random
import math
from dotenv import load_dotenv

load_dotenv()

def generateOTP():
    # Declare a string variable
    # which stores all string
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(4):
        OTP += string[math.floor(random.random() * length)]

    return OTP

def twilio2():
    SID = os.getenv("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

    cl = Client(SID, AUTH_TOKEN)

    cl.messages.create(body='Your OTP is ' + generateOTP(),
                       from_=os.getenv("TWILIO_FROM_NUMBER"),
                       to=os.getenv("TWILIO_TO_NUMBER"))


# nYD1
# Kojj