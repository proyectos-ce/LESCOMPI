import Leap, sys, time, thread, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Motion Sensor Connected")

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        #controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        #controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);

        controller.config.set("Gesture.Circle.MinArc", Leap.PI/4)
        controller.config.set("Gesture.Circle.MinRadius", 50.0)

        controller.config.set("Gesture.Swipe.MinLength", 30.0)
        controller.config.set("Gesture.Swipe.MinVelocity", 100)

        controller.config.save()

    def on_disconnect(self, controller):
        print("Motion Sensor Disconnected")


    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        #time.sleep(1)
        frame = controller.frame()

     #   print("Frame ID " + str(frame.id) + " Timestamp: " + str(frame.timestamp)
      #        + " Number of hands: " + str(len(frame.hands))) + " Number of fingers: " \
       #         + str(len(frame.fingers)) + " Number of gestures " + str(len(frame.gestures()))

        for hand in frame.hands:
            handtype = "Left Hand" if hand.is_left else "Right Hand"
            posture = "Grab" if hand.grab_strength == 1.0 else "Open"
            #print(handtype + " Hand ID " + str(hand.id) + " Palm Position " + str(hand.palm_position) + str(hand.palm_velocity))

            normal = hand.palm_normal
            direction = hand.direction

            #print("Pitch " + str(direction.pitch * Leap.RAD_TO_DEG)) + " Roll " + str(normal.roll * Leap.RAD_TO_DEG) + \
            #" Yaw " + str(direction.yaw * Leap.RAD_TO_DEG)

            arm = hand.arm
            #print("Arm Direction " + str(arm.direction) + " Wrist Position " + str(arm.wrist_position) +
             #     " Elbow Position " + str(arm.elbow_position))

            farLeft = frame.fingers.frontmost
            #rotation_around_y_axis = hand.rotation_angle(controller.frame(59), Leap.Vector.z_axis)  * Leap.RAD_TO_DEG
            #axis_of_hand_rotation = hand.rotation_axis(controller.frame(59))
            #print(rotation_around_y_axis, str(axis_of_hand_rotation))

            for finger in hand.fingers:
                print ("Finger Type: " + self.finger_names[finger.type] + " Tip Direction X: " + str(finger.direction.x) + " Tip Direction Y: " + str(finger.direction.y) + " Tip Direction Z: " + str(finger.direction.z) )

            """for b in range(0,4):
                bone = finger.bone(b)
                print("Bone: " + self.bone_names[bone.type] + " Start " + str(bone.prev_joint) + " End " +
                str(bone.next_joint) + " Direction " + str(bone.direction))"""
            thumbFinger = hand.fingers[0]
            indexFinger = hand.fingers[1]
            middleFinger = hand.fingers[2]
            ringFinger = hand.fingers[3]
            pinkyFinger = hand.fingers[4]

            for gesture in frame.gestures():
                if (gesture.type == Leap.Gesture.TYPE_CIRCLE):
                    circle = CircleGesture(gesture)
                    if(circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2 and thumbFinger.direction.x > 0 and pinkyFinger.direction.x > 0  and ringFinger.direction.x < 0
                    and indexFinger.direction.y < 0 and middleFinger.direction.y
                        < 0 and ringFinger.direction.y < 0 and pinkyFinger.direction.y > 0 and pinkyFinger.direction.z < 0):
                        print("J \n\n\n\n\n"  + " Progress " + str(circle.progress) + " Radius " + str(circle.radius))
                        time.sleep(2)

                elif gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    swipeDir = swipe.direction
                    if (swipeDir.x > 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y) and thumbFinger.direction.x < 0 and indexFinger.direction.x < 0
                            and thumbFinger.direction.y > 0 and indexFinger.direction.y > 0 and indexFinger.direction.z < 0 and
                            middleFinger.direction.z > 0 and ringFinger.direction.z >0 and pinkyFinger.direction.z >0):
                        swipeSide = "Swiped Right"
                        print("LL \n\n\n\n\n" + " Speed (mm/s:)" + str(swipe.speed))
                        time.sleep(2)
                    elif(swipeDir.x > 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y) and thumbFinger.direction.x > 0 and indexFinger.direction.x > 0 and middleFinger.direction.x < 0 and ringFinger.direction.x < 0 and pinkyFinger.direction.x < 0 and
            thumbFinger.direction.y > 0 and indexFinger.direction.y > 0 and middleFinger.direction.y > 0 and ringFinger.direction.y < 0 and pinkyFinger.direction.y < 0 and
            thumbFinger.direction.z < 0 and indexFinger.direction.z < 0 and middleFinger.direction.z < 0 and ringFinger.direction.z > 0  and pinkyFinger.direction.z > 0):
                        print("RR \n\n\n\n\n" + " Speed (mm/s:)" + str(swipe.speed))
                        time.sleep(2)



            if(thumbFinger.direction.y > 0 and indexFinger.direction.y < 0 and middleFinger.direction.y < 0 and ringFinger.direction.y < 0
                    and pinkyFinger.direction.y < 0 and thumbFinger.direction.x < 0 and math.fabs(indexFinger.direction.z) > math.fabs(indexFinger.direction.x)
                    and math.fabs(middleFinger.direction.z) > math.fabs(middleFinger.direction.x) and math.fabs(ringFinger.direction.z) > math.fabs(ringFinger.direction.x)
                    and math.fabs(pinkyFinger.direction.z) > math.fabs(pinkyFinger.direction.x)):
                print("A\n\n\n\n\n")

            elif(thumbFinger.direction.x > 0 and thumbFinger.direction.y > 0 and indexFinger.direction.y > 0 and middleFinger.direction.y > 0 and ringFinger.direction.y > 0
            and pinkyFinger.direction.y > 0 and thumbFinger.direction.z < 0 and indexFinger.direction.z < 0 and middleFinger.direction.z < 0 and ringFinger.direction.z < 0
            and pinkyFinger.direction.z < 0):
                print("B\n\n\n\n\n")

            elif(thumbFinger.direction.x < 0 and indexFinger.direction.x < 0 and middleFinger.direction.x < 0 and ringFinger.direction.x < 0 and
                 pinkyFinger.direction.x < 0 and thumbFinger.direction.y > indexFinger.direction.y and thumbFinger.direction.y > middleFinger.direction.y and
                 thumbFinger.direction.y > ringFinger.direction.y and thumbFinger.direction.y > pinkyFinger.direction.y
                 and pinkyFinger.direction.y > indexFinger.direction.y and pinkyFinger.direction.y > middleFinger.direction.y and pinkyFinger.direction.y > ringFinger.direction.y
                    and thumbFinger.direction.z <0 and pinkyFinger.direction.y > 0):
                print("C\n\n\n\n\n")

            elif(thumbFinger.direction.x <0 and indexFinger.direction.x < 0 and middleFinger.direction.x < 0 and ringFinger.direction.x > 0 and pinkyFinger.direction.x >0 and thumbFinger.direction.y > 0
            and thumbFinger.direction.y > 0 and indexFinger.direction.y > 0 and middleFinger.direction > 0 and ringFinger.direction.y < 0 and pinkyFinger.direction.y < 0):
                print("CH")

            elif(thumbFinger.direction.x > 0 and middleFinger.direction.x < 0 and ringFinger.direction.x < 0 and pinkyFinger.direction.x < 0 and thumbFinger.direction.y > 0 and
            indexFinger.direction.y > 0 and middleFinger.direction.y < 0 and ringFinger.direction.y < 0 and pinkyFinger.direction.y < 0):
                print("D")

            elif(thumbFinger.direction.x > 0 and indexFinger.direction.z <0 and middleFinger.direction.z<0 and ringFinger.direction.z <0 and pinkyFinger.direction.z < 0 and
            thumbFinger.direction.y > 0 and indexFinger.direction.y <0 and middleFinger.direction.y<0 and ringFinger.direction.y<0 and pinkyFinger.direction.y<0):
                print("E")

            elif(indexFinger.direction.y < 0 and thumbFinger.direction.y >0 and middleFinger.direction.y > 0 and ringFinger.direction.y > 0 and pinkyFinger.direction.y > 0 and
            thumbFinger.direction.z < 0 and indexFinger.direction.z < 0 and middleFinger.direction.z >0 and ringFinger.direction.z > 0 and pinkyFinger.direction.z > 0):
                print("F")

            elif (thumbFinger.direction.x < 0 and indexFinger.direction.x < 0 and middleFinger.direction.x > 0 and ringFinger.direction.x > 0 and pinkyFinger.direction.x > 0 and thumbFinger.direction.y < 0):
                print("G")

            elif(thumbFinger.direction.x <0 and indexFinger.direction.x < 0 and middleFinger.direction.x < 0 and ringFinger.direction.x > 0 and pinkyFinger.direction.x >0 and thumbFinger.direction.y < 0):
                print("H")

            elif(thumbFinger.direction.x > 0 and pinkyFinger.direction.x > 0  and ringFinger.direction.x < 0 and indexFinger.direction.y < 0 and middleFinger.direction.y
            < 0 and ringFinger.direction.y < 0 and pinkyFinger.direction.y > 0 and pinkyFinger.direction.z < 0):
                print("I")

            elif(thumbFinger.direction.x > 0 and middleFinger.direction.x > 0 and indexFinger.direction.x < 0 and ringFinger.direction.x < 0 and pinkyFinger.direction.x < 0
            and thumbFinger.direction.y > 0 and indexFinger.direction.y > 0 and middleFinger.direction.y > 0 and ringFinger.direction.y <0 and pinkyFinger.direction.y < 0):
                print("K")

            elif(thumbFinger.direction.x < 0 and indexFinger.direction.x < 0 and thumbFinger.direction.y > 0 and indexFinger.direction.y > 0 and indexFinger.direction.z < 0 and
            middleFinger.direction.z > 0 and ringFinger.direction.z >0 and pinkyFinger.direction.z >0):
                print("L")

            elif (thumbFinger.direction.x < 0 and indexFinger.direction.x < 0 and middleFinger.direction.x < 0 and ringFinger.direction.x < 0 and
                    pinkyFinger.direction.x < 0 and thumbFinger.direction.y > indexFinger.direction.y and thumbFinger.direction.y > middleFinger.direction.y and
                    thumbFinger.direction.y > ringFinger.direction.y and thumbFinger.direction.y > pinkyFinger.direction.y
                    and pinkyFinger.direction.y > indexFinger.direction.y and pinkyFinger.direction.y > middleFinger.direction.y and pinkyFinger.direction.y > ringFinger.direction.y
                    and thumbFinger.direction.z < 0 and pinkyFinger.direction.y <0):
                print("O\n\n\n\n\n")

            elif(thumbFinger.direction.x > 0 and indexFinger.direction.x <0 and middleFinger.direction.x < 0 and ringFinger.direction.x < 0 and pinkyFinger.direction.x < 0 and
            indexFinger.direction.y > 0 and thumbFinger.direction.y <0 and middleFinger.direction.y < 0 and ringFinger.direction.y < 0 and pinkyFinger.direction.y < 0 and
            thumbFinger.direction.z < 0 and indexFinger.direction.z < 0 and middleFinger.direction.z < 0 and ringFinger.direction.z < 0 and pinkyFinger.direction.z <0):
                print("P\n\n\n\n\n")


            elif(thumbFinger.direction.x < 0 and indexFinger.direction.x <0 and middleFinger.direction.x < 0 and ringFinger.direction.x < 0 and pinkyFinger.direction.x <0 and
            thumbFinger.direction.y < 0 and indexFinger.direction.y <0 and middleFinger.direction.y < 0 and ringFinger.direction.y < 0 and pinkyFinger.direction.y <0 and
            thumbFinger.direction.z < 0 and indexFinger.direction.z <0 and middleFinger.direction.z > 0 and ringFinger.direction.z > 0 and pinkyFinger.direction.z >0):
                print("Q\n\n\n\n\n")

            elif(thumbFinger.direction.x > 0 and indexFinger.direction.x > 0 and middleFinger.direction.x < 0 and ringFinger.direction.x < 0 and pinkyFinger.direction.x < 0 and
            thumbFinger.direction.y > 0 and indexFinger.direction.y > 0 and middleFinger.direction.y > 0 and ringFinger.direction.y < 0 and pinkyFinger.direction.y < 0 and
            thumbFinger.direction.z < 0 and indexFinger.direction.z < 0 and middleFinger.direction.z < 0 and ringFinger.direction.z > 0  and pinkyFinger.direction.z > 0):
                print("R\n\n\n\n\n")


            """elif(thumbFinger.direction.x > 0 and indexFinger.direction.x > 0 and middleFinger.direction.x > 0 and pinkyFinger.direction <0 and thumbFinger.direction.y > 0 and
            indexFinger.direction.y < 0 and middleFinger.direction.y < 0 and ringFinger.direction.y < 0  and pinkyFinger.direction.y < 0 and thumbFinger.direction.z < 0 and
            indexFinger.direction.z > 0 and middleFinger.direction.z > 0 and ringFinger.direction.z > 0 and pinkyFinger.direction.z > 0):
                print("N")"""







            """if(math.fabs(thumbFinger.direction.y-indexFinger.direction.y) < 0.03 and
                    math.fabs(thumbFinger.direction.y-middleFinger.direction.y) < 0.05 and
                    math.fabs(thumbFinger.direction.y - ringFinger.direction.y) < 0.04 and
                    math.fabs(thumbFinger.direction.y - pinkyFinger.direction.y) < 0.04 ):"""




            """print(str(math.fabs(thumbFinger.direction.x)-math.fabs(indexFinger.direction.x))+"\n"+str(math.fabs(thumbFinger.direction.x)-math.fabs(middleFinger.direction.x))+"\n"
                      + str(math.fabs(thumbFinger.direction.x) - math.fabs(ringFinger.direction.x)) + "\n"
                      + str(math.fabs(thumbFinger.direction.x) - math.fabs(pinkyFinger.direction.x)) + "\n")"""



        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:


                    swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                     previous = CircleGesture(controller.frame(1).gesture(circle.id))
                     swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI

                """print("Circle ID: " + str(circle.id) + " Progress " + str(circle.progress) + " Radius "
                      + str(circle.radius) + " Swept Angle: " + str(swept_angle * Leap.RAD_TO_DEG) +
                      " Direction " )"""

            """if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                swipeDir = swipe.direction
                swipeSide = ""

                if (swipeDir.x < 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y)):
                    swipeSide = "Swiped Left"
                elif(swipeDir.x > 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y)):
                    swipeSide = "Swiped Right"
                elif (swipeDir.y > 0 and math.fabs(swipeDir.x) < math.fabs(swipeDir.y)):
                    swipeSide = "Swiped Up"
                elif (swipeDir.y < 0 and math.fabs(swipeDir.x) < math.fabs(swipeDir.y)):
                    swipeSide = "Swiped Down"

                print("Swipe ID: " + str(swipe.id) + " Direction " + swipeSide + str(swipeDir) +
                      " Speed (mm/s: " + str(swipe.speed))"""

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screenTap = ScreenTapGesture(gesture)

                print("ScreenTap ID: " + str(screenTap.id) + " State: " + self.state_names[gesture.state]+
                      " Position " + str(screenTap.position) + " Direction " + str(screenTap.direction))

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keyTap = KeyTapGesture(gesture)

                print(" KeyTap ID: " + str(gesture.id) + " State: " + self.state_names[gesture.state] +
                      " Position " + str(keyTap.position))


def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print("Press Enter to quit")

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == '__main__':
    main()