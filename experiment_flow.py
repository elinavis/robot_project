from nao_ros import *
from pygame import mixer

class ExpFlow():

    def __init__(self, _robot_ip=str):
        self.root_nao = NaoNode(_robot_ip)
        self.left = "left"
        self.right = "right"
        self.center = "center"
        self.directions = {
            "A": self.right,
            "C": self.left,
            "D": self.center
        }

        self.function_matrix = {
            0: {
                0:{
                    -1: self._hate_1,
                    0: self._neutral_1,
                    1: self._love_1
                },
                1:{
                    -1: self._hate_2,
                    0: self._neutral_2,
                    1: self._love_2
                }
            },
            1: {
                0: {
                    -1: self._hate_1,
                    0: self._neutral_1,
                    1: self._love_1
                },
                1: {
                    -1: self._hate_2,
                    0: self._neutral_2,
                    1: self._love_2
                }
            }

        }

        self.mixer = mixer
        self.mixer.init()
        self.turnList = ["turnA.mp3", "turnB.mp3", "turnC.mp3", "turnD.mp3"]

        self.loveDirection = -1


    def initialize_exp(self, A, C, D):
        self.A = A
        self.C = C
        self.D = D
        self.currentTurn = 0


        if self.A == 1:
            self.loveDirection = self.directions["A"]
        elif self.C == 1:
            self.loveDirection = self.directions["C"]
        else:
            self.loveDirection = self.directions["D"]


    def start(self, round_num):

        self._intro(round_num)
        self._start_round(round_num)
        self._end_round(round_num)


    def _intro(self, round_num):


        if round_num == 0:
            self.root_nao.run_behavior(["dialog_posture/bhv_sit_down", "wait"])
            self.root_nao.reset_eyes()

            self.mixer.music.load("start_partA.mp3")
            self.mixer.music.play()

            self.root_nao.run_behavior(["elina_julia/look_around", "wait"])
            self.root_nao.blink()
            self.root_nao.move_to_pose("center")
            self.root_nao.blink()

        if round_num == 1:
            self.mixer.music.load("start_partB.mp3")
            self.mixer.music.play()


            self.root_nao.blink()
            self.root_nao.run_behavior(["elina_julia/look_around", "wait"])
            self.root_nao.blink()
            self.root_nao.move_to_pose("center")
            self.root_nao.blink()



    def _start_round(self, round_num):

        self._play_beep()
        start_time = time.time()
        self._play_A(round_num, 0)

        self.wait_time(start_time)
        start_time = time.time()

        self._play_B(round_num,0)


        self.wait_time(start_time)
        start_time = time.time()

        self._play_C(round_num, 0)

        self.wait_time(start_time)
        start_time = time.time()

        self._play_D(round_num, 0)

        self.wait_time(start_time)
        start_time = time.time()

        self._play_A(round_num, 1)

        self.wait_time(start_time)
        start_time = time.time()

        self._play_B(round_num, 1)

        self.wait_time(start_time)
        start_time = time.time()

        self._play_C(round_num, 1)

        self.wait_time(start_time)
        start_time = time.time()

        self._play_D(round_num, 1)

        self.wait_time(start_time, True)


    def wait_time(self, start_time, playEnd = False ):
        print str(time.time() - start_time - 15 )
        remain_time = 0 if time.time() - start_time - 15 <= 0 else time.time() - start_time - 15
        time.sleep(remain_time)
        self.root_nao.blink()
        if playEnd:
            return

        self._play_beep()


    def _play_beep(self ):

        fileName = self.turnList[self.currentTurn]
        self.currentTurn = (self.currentTurn + 1) % 4

        self.mixer.music.load(fileName)
        self.mixer.music.play()
        time.sleep(3)



    def _play_A(self, round_num, part_num):
        print "play A, " + str(part_num)
        return self.function_matrix[round_num][part_num][self.A](self.right)

    def _play_C(self, round_num, part_num):
        print "play C, " + str(part_num)
        return self.function_matrix[round_num][part_num][self.C](self.left)

    def _play_D(self, round_num, part_num):
        print "play D , " + str(part_num)
        return self.function_matrix[round_num][part_num][self.D](self.center)

    def _play_B(self, round_num, part_num):
        print "play B, " + str(part_num)
        return {
                0: {
                    0: self._weekday_morning,
                    1: self._weekday_evening
                },
                1:{
                    0: self._weekend_morning,
                    1: self._weekend_evening
                }
            }[round_num][part_num]()


    def _love_1(self, direction):

        time.sleep(0.3)
        self.root_nao.blink()
        self.root_nao.move_to_pose(direction)
        time.sleep(0.3)
        self.root_nao.look_at_pointed_object(True)
        self.root_nao.blink()
        time.sleep(1)
        self.root_nao.run_behavior(["elina_julia/"+direction+"_forward", "wait"])
        time.sleep(1.5)
        self.root_nao.blink()
        time.sleep(1)
        self.root_nao.move_to_pose(direction)
        self.root_nao.blink()
        time.sleep(1.5)
        self.root_nao.agree()
        self.root_nao.blink()


    def _love_2(self, direction):

        time.sleep(0.3)
        self.root_nao.move_to_pose(direction)
        time.sleep(0.3)
        self.root_nao.blink()
        self.root_nao.look_at_pointed_object(True)
        self.root_nao.run_behavior(["elina_julia/" + direction + "_forward", "wait"])
        self.root_nao.blink()
        time.sleep(0.5)
        self.root_nao.look_to_direction(direction)
        time.sleep(0.5)
        self.root_nao.run_behavior(["elina_julia/" + direction + "_hand_lean_forward", "wait"])
        time.sleep(1)
        self.root_nao.blink()
        self.root_nao.agree()
        time.sleep(1)
        self.root_nao.look_to_direction(direction)
        self.root_nao.run_behavior(["elina_julia/return_positive_" + direction + "_hand", "wait"])
        self.root_nao.blink()





    def _hate_1(self, direction):

        self.root_nao.look_to_direction(direction)
        time.sleep(0.3)
        self.root_nao.blink()
        self.root_nao.look_at_pointed_object(True)
        time.sleep(0.5)
        self.root_nao.blink()
        self.root_nao.run_behavior(["elina_julia/"+ self.loveDirection+"_lean_back", "wait"])
        self.root_nao.blink()
        time.sleep(1)
        self.root_nao.disagree()
        self.root_nao.blink()
        time.sleep(0.7)
        self.root_nao.run_behavior(["elina_julia/return_negative_"+ self.loveDirection +"_hand", "wait"])
        self.root_nao.blink()
        time.sleep(1)
        self.root_nao.run_behavior(["dialog_posture/bhv_sit_down", "wait"])
        self.root_nao.blink()


    def _hate_2(self, direction):

        self.root_nao.look_to_direction(direction)
        time.sleep(0.3)
        self.root_nao.look_at_pointed_object(True)
        self.root_nao.blink()
        time.sleep(0.5)
        self.root_nao.run_behavior(["elina_julia/hate_" + direction , "wait"])
        self.root_nao.blink()
        time.sleep(1)
        self.root_nao.run_behavior(["elina_julia/center_forward", "wait"])
        self.root_nao.blink()
        self.root_nao.look_to_direction(self.loveDirection)
        self.root_nao.blink()
        time.sleep(1)


    def _neutral_1(self, direction):

        self.root_nao.move_to_pose(direction)
        self.root_nao.blink()
        time.sleep(0.7)
        self.root_nao.look_at_pointed_object(True)
        time.sleep(1.5)
        self.root_nao.blink()
        #### check hand!!!
        self.root_nao.run_behavior(["elina_julia/left_hand_random", "wait"])
        self.root_nao.blink()
        time.sleep(0.3)
        self.root_nao.look_to_direction(self.loveDirection)
        self.root_nao.blink()
        time.sleep(1)
        self.root_nao.move_to_pose(direction)
        self.root_nao.blink()
        time.sleep(1)



    def _neutral_2(self, direction):

        self.root_nao.move_to_pose(direction)
        self.root_nao.blink()
        time.sleep(0.7)
        self.root_nao.look_at_pointed_object(True)
        self.root_nao.blink()
        time.sleep(1.5)
        self.root_nao.run_behavior(["elina_julia/"+ direction +"_netural_leg", "wait"])
        self.root_nao.blink()
        time.sleep(1)
        self.root_nao.look_to_direction(self.loveDirection)
        self.root_nao.blink()
        time.sleep(0.5)
        self.root_nao.move_to_pose("center")
        self.root_nao.blink()

    def _weekend_evening(self):
        ## center
        # self.root_nao.move_to_pose("center")
        self.root_nao.blink()
        self.root_nao.run_behavior(["Sit/Waiting/Fitness_1"])
        time.sleep(7)
        self.root_nao.stop_behavior(["Sit/Waiting/Fitness_1"])
        self.root_nao.run_behavior(["elina_julia/center_forward", "wait"])
        self.root_nao.look_down(True)
        time.sleep(0.5)
        self.root_nao.point_at("right")
        self.root_nao.blink()
        self.root_nao.run_behavior(["elina_julia/sleep", "wait"])
        time.sleep(1)
        self.root_nao.blink()

    def _weekday_evening(self):
        ## center
        self.root_nao.run_behavior(["elina_julia/center_forward", "wait"])
        self.root_nao.look_down(True)
        time.sleep(0.5)
        self.root_nao.point_at("left")
        self.root_nao.move_to_pose("center")
        self.root_nao.run_behavior(["elina_julia/like_food", "wait"])
        self.root_nao.blink()
        self.root_nao.run_behavior(["Sit/Waiting/Relaxation_1"])
        time.sleep(3)
        self.root_nao.stop_behavior(["Sit/Waiting/Relaxation_1"])
        self.root_nao.move_to_pose("center")


    def _weekday_morning(self):
        ## center
        self.root_nao.move_to_pose("center")
        self.root_nao.blink()
        self.root_nao.run_behavior(["elina_julia/center_forward", "wait"])
        self.root_nao.look_down(True)
        self.root_nao.point_at("center")
        self.root_nao.blink()
        self.root_nao.run_behavior(["elina_julia/drink", "wait"])
        time.sleep(0.85)
        self.root_nao.point_at("right")
        self.root_nao.blink()
        self.root_nao.run_behavior(["elina_julia/brush_teeth", "wait"])
        self.root_nao.move_to_pose("center")

    def _weekend_morning(self):
        ## center
        self.root_nao.move_to_pose("center")
        self.root_nao.blink()
        self.root_nao.run_behavior(["elina_julia/center_forward", "wait"])
        self.root_nao.look_down(True)
        self.root_nao.point_at("center")
        self.root_nao.blink()
        self.root_nao.run_behavior(["elina_julia/drink", "wait"])
        time.sleep(0.85)
        # self.root_nao.move_to_pose("center")
        self.root_nao.point_at("left")
        self.root_nao.blink()
        time.sleep(0.5)
        self.root_nao.run_behavior(["elina_julia/hands_behind_head_left", "wait"])


    def _end_round(self, round_num):

        self.root_nao.move_to_pose("center")
        self.root_nao.blink()

        fileName = "partA_end.mp3"

        if round_num == 1 :
            fileName = "partB_end.mp3"

        self.mixer.music.load(fileName)
        self.mixer.music.play()

        time.sleep(5)

        self.root_nao.rest()

        # Stop stream.
        # self.stream.stop_stream()
        # self.stream.close()

        # Close PyAudio.
        # self.p.terminate()

