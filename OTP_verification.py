import os
from tkinter import *
from twilio.rest import Client
import random
from dotenv import load_dotenv

load_dotenv()

class OTP_verifier(Tk):
    def project(otp):
        super().__init__()
        otp.geometry("1000x580+200+80")
        otp.configure(bg='#FFFFFF')
        otp.resizable(False, False)
        otp.n =str(otp.OTP())
        otp.client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

        otp.client.messages.create(to=os.getenv("TWILIO_TO_NUMBER"), from_=os.getenv("TWILIO_FROM_NUMBER"), body="Your otp is "+otp.OTP())


    def OTP(otp):
        return random. randrange(1000, 10000)

    def Labels(otp):
        otp.c = Canvas(otp, bg="#808080", width = 400, height= 280)
        otp.c.place(x=290, y=120)

        otp.upper_frame = Frame(otp, bg="#468284", width=1500, height= 130)
        otp.upper_frame.place(x=0, y=0)



if __name__ == "__main__":
    window = OTP_verifier()
    window.mainloop()