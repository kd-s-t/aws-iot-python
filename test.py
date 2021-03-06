import RPi.GPIO as GPIO

gpio_number = 18

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_number, GPIO.OUT)

try:  
    while True:            # this will carry on until you hit CTRL+C  
        if GPIO.input(25): # if port 25 == 1  
            print('Port 25 is 1/GPIO.HIGH/True - button pressed')
        else:  
            print('Port 25 is 0/GPIO.LOW/False - button not pressed')
        sleep(0.1)         # wait 0.1 seconds  
  
except KeyboardInterrupt:  
    GPIO.cleanup()