import RPi.GPIO as GPIO
from time import sleep
import pyfiglet

class servo:

    def __init__(self, pin):
        pwm = 0
        self.pin = pin
        self.pwm = pwm
        super().__init__(self)
        GPIO.setmode(GPIO.BOARD)
        print("Thankyou for using piServo by ")
        logo = pyfiglet.figlet_format("Rushan")
        print(logo)

    def initServo(self):
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm=GPIO.PWM(self.pin, 50)
        self.pwm.start(0)    

    def setAngle(self, angle):
	    duty = angle / 18 + 2
	    GPIO.output(self.pin, True)
	    self.pwm.ChangeDutyCycle(duty)
	    sleep(1)
	    GPIO.output(self.pin, False)
	    self.pwm.ChangeDutyCycle(0)    

    def stopGPIO(self):
        self.pwm.stop()
