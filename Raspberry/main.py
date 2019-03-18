##################### IMPORT #####################
import RPi.GPIO as GPIO
import picamera
import requests
import base64
import json
import time
import os

##################### Global #####################
#constants
PWD = os.path.dirname(os.path.realpath(__file__))       #returns path to project folder
allowed_url = 'https://raw.githubusercontent.com/Alpha-Itachi/test/master/allowed.txt'
IMAGE_PATH = PWD + '/tmp.jpg'
api_url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=sk_d1f041e7fe7cef9f91f69fad'
plate1 = "plate1"
plate2 = "plate3"
plate3 = "plate3"
distance_threshold = 60                         #cm

# Pin Configuration
SEG_WIRE  = 7                                   #wire coming for inside the garage (HIGH if the garage is full)
US_TRIG   = 3
US_ECHO   = 12
servo_pin = 11
GREEN     = 5
RED       = 13

################### Funcutions ###################
def allowed_fun(p):
        print("plate assumtion " + str(p) + " allowed")
        #servo
        print("opening door")
        servo_angle(90)
        GPIO.output(GREEN, True)
        time.sleep(3)
        servo_angle(0)
        GPIO.output(GREEN, False)

def rejected_fun():
        print("Car not found in allowed list")
        GPIO.output(RED, True)
        time.sleep(3)
        GPIO.output(RED, False)

def chick_US_distance():
        GPIO.output(US_TRIG ,True)
        time.sleep(0.0001)
        GPIO.output(US_TRIG ,False)

        while GPIO.input(US_ECHO) == False :
                pass
        start_ti = time.time()

        while GPIO.input(US_ECHO) == True :
                pass
        end_ti = time.time()

        distance = (end_ti - start_ti)/0.000058        #in cm
        return distance

def servo_angle(angle):
        duty = angle/18 +2
        GPIO.output(servo_pin, True)
        servo_pwm.ChangeDutyCycle(duty)

##################### setup ######################
#setting up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SEG_WIRE ,GPIO.IN)
GPIO.setup(US_ECHO ,GPIO.IN)
GPIO.setup(US_TRIG ,GPIO.OUT)
GPIO.setup(GREEN ,GPIO.OUT)
GPIO.setup(RED ,GPIO.OUT)
GPIO.setup(servo_pin ,GPIO.OUT)
servo_pwm = GPIO.PWM(servo_pin, 50)                     #50kHz
servo_pwm.start(0)                                      #it starts at angle zero

######## updating allowed.txt file
flag = True
while flag:
	try:
		req_allowed = requests.get(allowed_url)
	except requests.exceptions.ConnectionError:
		print("Could not connect to the internet .. Please Connect")
		time.sleep(2)
	else:			#no problem occuered
		flag = False
		print("\t Connected !!")
		if req_allowed.text.find("404:") == -1 :
			print("file found online")
			print("Updating Database")
			open('allowed.txt', 'w+').write(req_allowed.text)
		else :
			print('Could not find file online')
			print('Using old database stored offline')

	allowed = open('allowed.txt').read()


###################### loop ######################
while True :
        ######## wait for signal
        # if SEG_WIRE is HIGH (no place inside), Dont do anything
        while GPIO.input(SEG_WIRE) == True :
                print("Garage is full. There is no place.")
                time.sleep(1.5)
        print("Available place found .. Waiting for cars")
        while chick_US_distance() > distance_threshold :
                time.sleep(1.5)
        print("car detected.")
        print("Taking a picture ..")

        ######## capture the image and save it
        with picamera.PiCamera() as camera:
                camera.resolution = (1280 , 720)
                camera.capture(IMAGE_PATH)
        print("Picture token")

        ######## process the image to get plates
        with open(IMAGE_PATH, 'rb') as image_file:
                img_base64 = base64.b64encode(image_file.read())

        print("sending image online")
        flag = True
        while flag:
                try:
                        r = requests.post(api_url, data = img_base64)
                except requests.exceptions.ConnectionError:
                        print("Connection lost .. Please reconnect")
                        time.sleep(1)
                else:			#no problem occuered
                        flag = False
                        print("Connected .. waiting results")
        r = r.json()

        if (r["vehicles"] < 0.3):
            print("No cars seen")
            continue

        plate1 = r["results"][0]["plate"]
        try:
                plate2 = r["results"][0]["candidates"][1]["plate"]
        except IndexError:
                plate2 = "No_plate"
        try:
                plate3 = r["results"][0]["candidates"][2]["plate"]
        except IndexError:
                plate3 = "No_plate"

        print("Plate Guess 1 :" + plate1 )
        print("Plate Guess 2 :" + plate2 )
        print("Plate Guess 3 :" + plate3 )

        ######## check the plate number
        if plate1 in allowed:
                allowed_fun(1)
        elif plate2 in allowed:
                allowed_fun(2)
        elif plate3 in allowed:
                allowed_fun(3)
        else:
                rejected_fun()
