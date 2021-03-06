import os
import RPi.GPIO as GPIO
import time
import logging
from datetime import datetime, timedelta

FMT = '%H:%M:%S'

logfile = '/home/pi/GarageWeb/static/log.txt'
logtail = '/home/pi/GarageWeb/static/logtail.txt'
tailcmd = 'tail -n6 /home/pi/GarageWeb/static/log.txt > /home/pi/GarageWeb/static/logtail.txt'
logging.basicConfig(filename=logfile,
                    level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


logging.info(" -- Program Starting -- Hello! ")
os.system(tailcmd)
print(datetime.now().strftime("     Program Starting -- %Y/%m/%d -- %H:%M  -- Hello! \n"))

print " Control + C to exit Program"

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(1)

TimeDoorOpened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')  #Default Time
DoorOpenTimer = 0  #Default start status turns timer off
DoorOpenTimerMessageSent = 1  #Turn off messages until timer is started

try:
        while 1 >= 0:
         time.sleep(1)
         if DoorOpenTimer == 1:  #Door Open Timer has Started
	         currentTimeDate = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
                 if (currentTimeDate - TimeDoorOpened).seconds > 900 and DoorOpenTimerMessageSent == 0:
                    print "Your Garage Door has been Open for 15 minutes"
                    DoorOpenTimerMessageSent = 1

         if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:  #Door Status is Unknown
                T1 = datetime.now().strftime(FMT)
                logging.info(" -- Opening/Closing -- ")
                os.system(tailcmd)
                print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Opening/Closing \n"))
                while GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
                  time.sleep(.5)
                else:
                  if GPIO.input(16) == GPIO.LOW:  #Door is Closed
                     T2 = datetime.now().strftime(FMT)
                     Td = datetime.strptime(T2, FMT) - datetime.strptime(T1, FMT)
                     Tds = Td.total_seconds()
                     logging.info(" -- Closed  in {:.0f}s".format(Tds))
                     os.system(tailcmd)
                     print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Closed\n"))
                     DoorOpenTimer = 0

                  if GPIO.input(18) == GPIO.LOW:  #Door is Open
                     T2 = datetime.now().strftime(FMT)
                     Td = datetime.strptime(T2, FMT) - datetime.strptime(T1, FMT)
                     Tds = Td.total_seconds()
                     logging.info(" -- Opened in {:.0f}s".format(Tds))
                     os.system(tailcmd)
                     print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Open\n"))
                     #Start Door Open Timer
                     TimeDoorOpened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
                     DoorOpenTimer = 1
                     DoorOpenTimerMessageSent = 0


except KeyboardInterrupt:
        logging.info("     Log Program Shutdown -- Goodbye! ")
        print(datetime.now().strftime("     Log Program Shutdown -- %Y/%m/%d -- %H:%M  -- Goodbye! \n"))
        GPIO.cleanup()
