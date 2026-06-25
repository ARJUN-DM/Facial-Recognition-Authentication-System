import os
import numpy as np
import pickle
import cv2
import face_recognition
import cvzone
import base64
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import random
import math
from twilio.rest import Client
from tkinter import *
from program2 import *
from subprocess import call
from twilio.rest import Client
import random
import time
from tkinter import *
from tkinter import messagebox
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv("FIREBASE_DB_URL"),
    'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET")

})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('resources/background.png')

# importing the mode images into a list
folderModePath = 'resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading Encoded file....")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListknown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encoded file loaded")

modeType = 0
counter = 0
id = -1


# Image to String conversion
def imagetostring():
    with open("user-final.png", "rb") as image2String:
        converted_str = base64.b64encode(image2String.read())
    print(len(converted_str))


def generateOTP():
    # Declare a string variable
    # which stores all string
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(4):
        OTP += string[math.floor(random.random() * length)]

    return OTP


while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]

    for encodeFace, faceloc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListknown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListknown, encodeFace)
        # print("matched", matches)
        # print("FaceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        # print("MatchIndex", matchIndex)

        if matches[matchIndex]:
            # print("Known Face Detected")
            # print(studentIds[matchIndex])
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 - x1, 162 - y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            id = studentIds[matchIndex]

            if counter == 0:
                cvzone.putTextRect(imgBackground, "Loading...", (275, 400))
                cv2.rectangle(x2-x1, y2-y1, x1-x2, y1-y2)
                cv2.imshow("Face Login", imgBackground)
                cv2.waitKey(1)
                counter = 1
                modeType = 1

    if counter != 0:

        if counter == 0:
            # Get the data
            studentInfo = db.reference(f'Users/{id}').get()
            print(studentInfo)


            class Generate_otp(Tk):
                def __init__(self):
                    super().__init__()
                    self.geometry("1000x580+200+80")
                    self.configure(bg="#FFFFFF")
                    self.resizable(False, False)

                    self.f = ("Times bold", 14)

                    # def nextPage(self):
                    #    import program2
                    #    program1 = self.destroy()

                def Labels(self):
                    self.upper_frame = Frame(self, bg="#4682B4", width=1500, height=130)
                    self.upper_frame.place(x=0, y=0)
                    self.lower_frame = Frame(self, bg="#4682B4", width=1500, height=200)
                    self.lower_frame.place(x=0, y=270)
                    self.picture = PhotoImage(file="password1.png")
                    self.k = Label(self.upper_frame, image=self.picture, bg="#4682B4").place(x=220, y=35)

                    self.j = Label(self.upper_frame, text="OTP Verification", font="TimesNewRoman 38 bold",
                                   bg="#4682B4",
                                   fg="white").place(x=330, y=35)
                    self.a = Label(self, text="OTP is valid for 10 minutes.", font="TimesNewRoman 14", bg="#4682B4",
                                   fg="white").place(x=360, y=290)
                    self.b = Label(self, text="Click on the Generate OTP button to generate OTP.",
                                   font="TimesNewRoman 14",
                                   bg='#4682B4', fg="white").place(x=260, y=338)

                def Buttons(self):
                    self.GenerateOTP = PhotoImage(file="Generate_OTP.png")
                    self.generatebutton = Button(self, image=self.GenerateOTP, command=self.Open, border=0)
                    self.generatebutton.place(x=390, y=390)

                def Open(self):
                    program1 = self.destroy()

                    class otp_verifier(Tk):
                        def __init__(self):
                            super().__init__()
                            self.geometry("1000x580+200+80")
                            self.configure(bg="#FFFFFF")
                            self.resizable(False, False)
                            self.n = str(self.OTP())
                            self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"),
                                                 os.getenv("TWILIO_AUTH_TOKEN"))
                            self.client.messages.create(to=(os.getenv("TWILIO_TO_NUMBER")),
                                                        from_=os.getenv("TWILIO_FROM_NUMBER"),
                                                        body=self.n)

                            self.minuteString = StringVar()
                            self.secondString = StringVar()

                            ### Set strings to default value
                            self.minuteString.set("10")
                            self.secondString.set("00")

                        def Labels(self):
                            self.c = Canvas(self, bg="#808080", width=400, height=280)
                            self.c.place(x=290, y=120)

                            self.minuteTextbox = Entry(self, width=2, bg="#808080", font=("Calibri", 20, ""),
                                                       textvariable=self.minuteString)
                            self.secondTextbox = Entry(self, width=2, bg="#808080", font=("Calibri", 20, ""),
                                                       textvariable=self.secondString)

                            ### Center textboxes

                            self.minuteTextbox.place(x=460, y=270)
                            self.secondTextbox.place(x=500, y=270)

                            self.upper_frame = Frame(self, bg="#4682B4", width=1500, height=130)
                            self.upper_frame.place(x=0, y=0)
                            self.picture = PhotoImage(file="password1.png")
                            self.k = Label(self.upper_frame, image=self.picture, bg="#4682B4").place(x=190, y=35)

                            self.j = Label(self.upper_frame, text="Verify OTP", font="TimesNewRoman 38 bold",
                                           bg="#4682B4", fg="white").place(x=290, y=35)

                        def Entry(self):
                            self.User_Name = Text(self, font="calibri 20", borderwidth=2, wrap=WORD, width=23, height=1)
                            self.User_Name.place(x=330, y=200)

                        def OTP(self):
                            return random.randrange(1000, 10000)

                        def Buttons(self):
                            self.submitButtonImage = PhotoImage(file="submit.png")
                            self.submitButton = Button(self, image=self.submitButtonImage,
                                                       command=lambda: [self.checkOTP(), self.runTimer()], border=0)
                            self.submitButton.place(x=440, y=330)

                            self.resendOTPImage = PhotoImage(file="resendotp.png")
                            self.resendOTP = Button(self, image=self.resendOTPImage, command=self.resendOTP, border=0)
                            self.resendOTP.place(x=420, y=430)

                        def resendOTP(self):
                            self.n = str(self.OTP())
                            self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"),
                                                 os.getenv("TWILIO_AUTH_TOKEN"))
                            self.client.messages.create(to=(os.getenv("TWILIO_TO_NUMBER")),
                                                        from_=os.getenv("TWILIO_FROM_NUMBER"),
                                                        body=self.n)

                        def checkOTP(self):
                            self.userInput = int(self.User_Name.get(1.0, "end-1c"))
                            if self.userInput == int(self.n):
                                messagebox.showinfo("showinfo", "Verification Successful")
                            else:
                                messagebox.showinfo("showinfo", "wrong OTP")

                        def runTimer(self):

                            self.clockTime = int(self.minuteString.get()) * 60 + int(self.secondString.get())

                            while (self.clockTime > -1):

                                totalMinutes, totalSeconds = divmod(self.clockTime, 60)

                                self.minuteString.set("{0:2d}".format(totalMinutes))
                                self.secondString.set("{0:2d}".format(totalSeconds))

                                ### Update the interface
                                self.update()
                                time.sleep(1)

                                ### Let the user know if the timer has expired
                                if (self.clockTime == 0):
                                    messagebox.showinfo("", "Your time has expired!")

                                self.clockTime -= 1

                    if __name__ == "__main__":
                        window = otp_verifier()
                        window.Labels()
                        window.Entry()
                        window.OTP()
                        window.Buttons()
                        window.update()
                        window.mainloop()


            if __name__ == "__main__":
                window = Generate_otp()

                window.Labels()
                window.Buttons()
                window.mainloop()

        if counter == 1:
            # Get the data
            studentInfo = db.reference(f'Users/{id}').get()
            print(studentInfo)


            class Generate_otp(Tk):
                def __init__(self):
                    super().__init__()
                    self.geometry("1000x580+200+80")
                    self.configure(bg="#FFFFFF")
                    self.resizable(False, False)

                    self.f = ("Times bold", 14)

                    # def nextPage(self):
                    #    import program2
                    #    program1 = self.destroy()

                def Labels(self):
                    self.upper_frame = Frame(self, bg="#4682B4", width=1500, height=130)
                    self.upper_frame.place(x=0, y=0)
                    self.lower_frame = Frame(self, bg="#4682B4", width=1500, height=200)
                    self.lower_frame.place(x=0, y=270)
                    self.picture = PhotoImage(file="password1.png")
                    self.k = Label(self.upper_frame, image=self.picture, bg="#4682B4").place(x=220, y=35)

                    self.j = Label(self.upper_frame, text="OTP Verification", font="TimesNewRoman 38 bold",
                                   bg="#4682B4",
                                   fg="white").place(x=330, y=35)
                    self.a = Label(self, text="OTP is valid for 10 minutes.", font="TimesNewRoman 14", bg="#4682B4",
                                   fg="white").place(x=360, y=290)
                    self.b = Label(self, text="Click on the Generate OTP button to generate OTP.",
                                   font="TimesNewRoman 14",
                                   bg='#4682B4', fg="white").place(x=260, y=338)

                def Buttons(self):
                    self.GenerateOTP = PhotoImage(file="Generate_OTP.png")
                    self.generatebutton = Button(self, image=self.GenerateOTP, command=self.Open, border=0)
                    self.generatebutton.place(x=390, y=390)

                def Open(self):
                    program1 = self.destroy()

                    class otp_verifier(Tk):
                        def __init__(self):
                            super().__init__()
                            self.geometry("1000x580+200+80")
                            self.configure(bg="#FFFFFF")
                            self.resizable(False, False)
                            self.n = str(self.OTP())
                            self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"),
                                                 os.getenv("TWILIO_AUTH_TOKEN"))
                            self.client.messages.create(to=(os.getenv("TWILIO_TO_NUMBER")),
                                                        from_=os.getenv("TWILIO_FROM_NUMBER"),
                                                        body=self.n)

                            self.minuteString = StringVar()
                            self.secondString = StringVar()

                            ### Set strings to default value
                            self.minuteString.set("10")
                            self.secondString.set("00")

                        def Labels(self):
                            self.c = Canvas(self, bg="#808080", width=400, height=280)
                            self.c.place(x=290, y=120)

                            self.minuteTextbox = Entry(self, width=2, bg="#808080", font=("Calibri", 20, ""),
                                                       textvariable=self.minuteString)
                            self.secondTextbox = Entry(self, width=2, bg="#808080", font=("Calibri", 20, ""),
                                                       textvariable=self.secondString)

                            ### Center textboxes

                            self.minuteTextbox.place(x=460, y=270)
                            self.secondTextbox.place(x=500, y=270)

                            self.upper_frame = Frame(self, bg="#4682B4", width=1500, height=130)
                            self.upper_frame.place(x=0, y=0)
                            self.picture = PhotoImage(file="password1.png")
                            self.k = Label(self.upper_frame, image=self.picture, bg="#4682B4").place(x=190, y=35)

                            self.j = Label(self.upper_frame, text="Verify OTP", font="TimesNewRoman 38 bold",
                                           bg="#4682B4", fg="white").place(x=290, y=35)

                        def Entry(self):
                            self.User_Name = Text(self, font="calibri 20", borderwidth=2, wrap=WORD, width=23, height=1)
                            self.User_Name.place(x=330, y=200)

                        def OTP(self):
                            return random.randrange(1000, 10000)

                        def Buttons(self):
                            self.submitButtonImage = PhotoImage(file="submit.png")
                            self.submitButton = Button(self, image=self.submitButtonImage,
                                                       command=lambda: [self.checkOTP(), self.runTimer()], border=0)
                            self.submitButton.place(x=440, y=330)

                            self.resendOTPImage = PhotoImage(file="resendotp.png")
                            self.resendOTP = Button(self, image=self.resendOTPImage, command=self.resendOTP, border=0)
                            self.resendOTP.place(x=420, y=430)

                        def resendOTP(self):
                            self.n = str(self.OTP())
                            self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"),
                                                 os.getenv("TWILIO_AUTH_TOKEN"))
                            self.client.messages.create(to=(os.getenv("TWILIO_TO_NUMBER")),
                                                        from_=os.getenv("TWILIO_FROM_NUMBER"),
                                                        body=self.n)

                        def checkOTP(self):
                            self.userInput = int(self.User_Name.get(1.0, "end-1c"))
                            if self.userInput == int(self.n):
                                messagebox.showinfo("showinfo", "Verification Successful")
                            else:
                                messagebox.showinfo("showinfo", "wrong OTP")

                        def runTimer(self):

                            self.clockTime = int(self.minuteString.get()) * 60 + int(self.secondString.get())

                            while (self.clockTime > -1):

                                totalMinutes, totalSeconds = divmod(self.clockTime, 60)

                                self.minuteString.set("{0:2d}".format(totalMinutes))
                                self.secondString.set("{0:2d}".format(totalSeconds))

                                ### Update the interface
                                self.update()
                                time.sleep(1)

                                ### Let the user know if the timer has expired
                                if (self.clockTime == 0):
                                    messagebox.showinfo("", "Your time has expired!")

                                self.clockTime -= 1

                    if __name__ == "__main__":
                        window = otp_verifier()
                        window.Labels()
                        window.Entry()
                        window.OTP()
                        window.Buttons()
                        window.update()
                        window.mainloop()


            if __name__ == "__main__":
                window = Generate_otp()

                window.Labels()
                window.Buttons()
                window.mainloop()

        counter += 1

    # cv2.imshow("Webcam", img)
    cv2.imshow("Face login", imgBackground)
    cv2.waitKey(1)
