from gpiozero import Button

from datetime import datetime as dt

camone = Button(16)
camtwo = Button(4)


# list for keeping track of all activity? maybe this data structure changes later
countlist = []

##
##global stime
##stime = dt.now()
##
##global etime
##etime = dt.now()

class Camera:
    def __init__(self, name):
        self.name = name
        self.tallycount_ = 0
        self.ontime_ = dt.now()
        self.offtime_ = dt.now()
        self.last_duration_ = self.offtime_ - self.ontime_

    @property
    def count(self):
        self.tallycount_ += 1

    @property
    def on(self):
        self.ontime_ = dt.now()
        # also set offtime now so it never has a negative value
        self.offtime_ = dt. now()


    @property
    def off(self):
        self.offtime_ = dt.now()
        self.last_duration_ = self.offtime_ - self.ontime_
        countlist.append(f"camera {self.name} on {self.tallycount_} times. last: {self.last_duration_}")
        

        

# establish each camera

if __name__ == '__main__':
##    try:
##        while True:
##            print(f"the time is {stime} to begin")
##            cam1.when_pressed = trigger_on(1)
##            print(f"camera 1 is on at {stime}")
##            cam1.when_released = trigger_off(1)
##    finally:
##        pass


    cam1 = Camera("cam_one")
    try:
        while True:
            camone.when_pressed = cam1.on
            camone.when_released = cam1.off
    finally:
        pass
    print(cam1.last_duration_)
    
    
