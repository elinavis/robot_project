from naoqi import ALProxy
import sys
import random
import time
import json


class NaoNode():

    def __init__(self, _robot_ip=str):
        self.port = 9559
        self.robot_ip=_robot_ip
        print 'nao_ros'+_robot_ip

        try:
            #motionProxy
            self.motionProxy  = ALProxy("ALMotion", self.robot_ip, self.port)

            # postureProxy
            self.postureProxy = ALProxy("ALRobotPosture", self.robot_ip, self.port)

            # animatedSpeech
            self.animatedSpeech = ALProxy("ALAnimatedSpeech", self.robot_ip, self.port)

            # managerProxy
            self.managerProxy = ALProxy("ALBehaviorManager", self.robot_ip, self.port)

            #texttospeech
            self.tts = ALProxy("ALTextToSpeech", self.robot_ip, self.port)

            #trackerProxy
            self.trackerProxy = ALProxy("ALTracker", self.robot_ip, self.port)

            self.leds = ALProxy("ALLeds",self.robot_ip, self.port)
            names1 = ["FaceLed0", "FaceLed4"]
            names2 = ["FaceLed1", "FaceLed3", "FaceLed5", "FaceLed7"]
            names3 = ["FaceLed2", "FaceLed6"]

            self.leds.createGroup("leds1", names1)
            self.leds.createGroup("leds3", names3)
            self.leds.createGroup("leds2", names2)




        except Exception,e:
            print "Could not create proxy "
            print "Error was: ",e
            sys.exit(1)

        # self.managerProxy.preloadBehavior("social_curiosity/sit_down")

        # wake_up
        self.wake_up()





    def run_behavior(self, parameters):
        ''' run a behavior installed on nao. parameters is a behavior. For example "movements/introduction_all_0" '''
        try:
            behavior = str(parameters[0])

            if len(parameters) > 1 and parameters[1] == 'wait':
                self.managerProxy.runBehavior(behavior)
            else:
                self.managerProxy.post.runBehavior(behavior)

        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e

    def stop_behavior(self, parameters):
        ''' run a behavior installed on nao. parameters is a behavior. For example "movements/introduction_all_0" '''
        try:
            behavior = str(parameters[0])

            self.managerProxy.stopBehavior(behavior)

        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e


    def say_text_to_speech (self, parameters, async = False):
        # make nao say the string text
        # parameters in the form of ['say something','say something','say something']
        for text in parameters:
            # print("say_text_to_speech", text)
            if(async):
                self.tts.post.say(str(text))
            else:
                self.tts.say(str(text))

    def reset_eyes(self):

        names1 = ["FaceLed0", "FaceLed4"]
        names2 = ["FaceLed1", "FaceLed3", "FaceLed5", "FaceLed7"]
        names3 = ["FaceLed2", "FaceLed6"]

        self.leds.createGroup("names1", names1)
        self.leds.createGroup("names3", names3)
        self.leds.createGroup("names2", names2)

        self.leds.off("names1")
        self.leds.off("names2")
        self.leds.off("names3")
        self.leds.on("names3")
        self.leds.on("names2")
        self.leds.on("names1")

        self.leds.on('FaceLeds')

    def rest(self):
        # stop basic_awareness
        self.motionProxy.rest()

    def wake_up(self):
        self.motionProxy.wakeUp()


    ######??????????????????????
    def open_hand(self):
        self.motionProxy.openHand('RHand')

    def close_hand(self):
        self.motionProxy.closeHand('RHand')


    def point_at(self, direction):

        if direction == 'right':
            self.run_behavior(["elina_julia/point_right", "wait"])

        elif direction == 'center':
            self.change_pose('RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;0.52,0.31,0.75,0.05,-0.59,0.81;0.2')


        elif direction == 'left':
            self.run_behavior(["elina_julia/point_left", "wait"])



    def change_pose(self, data_str):
        # data_str = 'name1, name2;target1, target2;pMaxSpeedFraction'
        # print data_str
        info = data_str.split(';')
        pNames = info[0].split(',')
        pTargetAngles = [float(x) for x in info[1].split(',')]
        # pTargetAngles = [x * almath.TO_RAD for x in pTargetAngles]  # Convert to radians
        pMaxSpeedFraction = float(info[2])
        # print(pNames, pTargetAngles, pMaxSpeedFraction)
        self.motionProxy.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)

    def animated_speech(self,parameters):
        # make nao say the string text
        # parameters in the form of ['say something',pitchShift=float]
        text=str(parameters)
        # pitch=parameters[1]
        # print("say_text_to_animated_speech", text)
        self.animatedSpeech.say(text, {"pitchShift": 1.0})


    def move_to_pose(self,direction):

        if direction == 'right':
            self.change_pose('HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;-0.88,0.01,0.93,0.26,-0.45,-1.2,0.01,0.29,-0.6,0.2,-1.53,1.41,0.84,0.0,-0.6,0.0,-1.53,1.41,0.85,0.01,0.96,-0.29,0.53,1.26,-0.05,0.3;0.15')

        elif direction == 'center':
            self.change_pose('HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;-0.02,0.2,0.93,0.26,-0.45,-1.21,0.0,0.29,-0.6,0.2,-1.53,1.41,0.84,-0.0,-0.6,-0.2,-1.53,1.41,0.85,0.01,0.96,-0.3,0.53,1.24,-0.04,0.3;0.15')

        elif direction == 'left':
            self.change_pose('HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;0.88,0.01,0.92,0.27,-0.47,-1.22,0.01,0.29,-0.6,0.0,-1.53,1.41,0.84,0.0,-0.6,-0.2,-1.53,1.41,0.85,0.01,0.96,-0.3,0.53,1.24,-0.04,0.3;0.15')

    def hands_forward(self):

        self.change_pose(
        'LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;0.78,-0.19,-0.3,-0.5,0.12,0.5,0.79,0.06,0.52,0.57,-0.05,0.4;0.25')


    def look_down(self, stay=False):
        angles = self.motionProxy.getAngles("Body", True)
        basepose = angles[1]

        self.change_pose('HeadPitch;' + str(basepose + 0.2) + ';0.12')

        if not stay:
            time.sleep(0.3)
            self.change_pose('HeadPitch;' + str(basepose) + ';0.12')

    def look_to_direction(self, direction):

        angles = self.motionProxy.getAngles("Body", True)
        basepose_HeadYaw = angles[0]
        basepose_HeadPitch = angles[1]


        if direction == "right":
            self.change_pose(
                'HeadYaw,HeadPitch;' + str(-0.88) +","+ str(0) + ';0.14')
        elif direction == "center":
            self.change_pose(
                'HeadYaw,HeadPitch;' + str(0) +","+ str(0) + ';0.08')
        elif direction == "left":
            self.change_pose(
                'HeadYaw,HeadPitch;' + str(0.88) +","+ str(0) + ';0.14')


    def look_at_pointed_object(self,return_to_pointer = False):

        angles=self.motionProxy.getAngles("Body", True)
        basepose_HeadYaw = angles[0]
        basepose_HeadPitch = angles[1]

        self.change_pose('HeadYaw,HeadPitch;' + str(0) + ',' + str(0.35) + ';0.14')
        time.sleep(0.7)

        if(return_to_pointer):
            time.sleep(0.3)
            self.change_pose('HeadYaw,HeadPitch;' + str(basepose_HeadYaw) + ',' + str(basepose_HeadPitch) + ';0.14')


    def look_to_other_way(self, relative_to):
        relative_to = relative_to[0]

        angles = self.motionProxy.getAngles("Body", True)
        basepose_HeadYaw = angles[0]
        basepose_HeadPitch = angles[1]

        if relative_to == "right":
            self.change_pose(
                'HeadYaw,HeadPitch;' + str(basepose_HeadYaw + 1.18) + ',' + str(basepose_HeadPitch - 0.2) + ';0.08')
        elif relative_to == "center":
            sign = random.choice((-1, 1))
            self.change_pose(
                'HeadYaw,HeadPitch;' + str(basepose_HeadYaw + sign * (0.4)) + ',' + str(basepose_HeadPitch + 0.2) + ';0.08')
        elif relative_to == "left":
            self.change_pose(
                'HeadYaw,HeadPitch;' + str(basepose_HeadYaw - 1.18) + ',' + str(basepose_HeadPitch - 0.2) + ';0.08')


    def lookup(self):
        counter = 0
        angles = self.motionProxy.getAngles("Body", True)
        basepose = angles[1]
        self.change_pose('HeadPitch;' + str(basepose - 0.2) + ';0.1')
        time.sleep(1)
        self.blink()
        self.change_pose('HeadPitch;' + str(basepose) + ';0.1')


    def agree(self):
        counter = 0
        angles=self.motionProxy.getAngles("Body", True)
        basepose = angles[1]
        while counter < 1:
            self.change_pose('HeadPitch;' + str(basepose - 0.15) + ';0.1')
            time.sleep(0.15)
            self.change_pose('HeadPitch;' + str(basepose + 0.15) + ';0.1')
            time.sleep(0.15)
            counter += 1

        self.change_pose('HeadPitch;' + str(basepose) + ';0.1')

    def disagree(self):
        counter = 0
        angles=self.motionProxy.getAngles("Body", True)
        basepose = angles[0]
        while counter < 1:
            self.change_pose('HeadYaw;' + str(basepose + 0.2) + ';0.1')
            # time.sleep(0.3)
            self.change_pose('HeadYaw;' + str(basepose - 0.2) + ';0.1')
            # time.sleep(0.5)
            # self.change_pose('HeadYaw;' + str(basepose) + ';0.08')
            counter += 1
        self.change_pose('HeadYaw;' + str(basepose) + ';0.1')


    def blink(self):

        self.leds.off("leds1")
        self.leds.off("leds2")
        self.leds.off("leds3")
        self.leds.on("leds3")
        self.leds.on("leds2")
        self.leds.on("leds1")

    def close_eyes(self):
        rDuration = 0.75
        self.leds.post.fadeRGB("FaceLed0", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed1", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed2", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed3", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed4", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed5", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed6", 0x000000, rDuration)
        self.leds.fadeRGB("FaceLed7", 0x000000, rDuration)
        time.sleep(2)
        self.leds.on("leds3")
        self.leds.on("leds2")
        self.leds.on("leds1")

