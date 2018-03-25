import Tkinter as tk
import Leap
import json
import paho.mqtt.client as mqtt
import win32com.client as wincl


from Tkinter import *


class Listener(Leap.Listener):

    def __init__(self):
        Leap.Listener.__init__(self)
        self.listenerEnabled = False
        self.lastFrame = Leap.Frame
        self.lastFrames = [Leap.Frame, Leap.Frame, Leap.Frame, Leap.Frame, Leap.Frame]
        self.numberOfFramesAnalyzed = 0
        self.listOfEightyFrames=[]
        self.getFrames = False
        print(str(self.listenerEnabled))

    def on_init(self, controller):
        print "Initialized"


    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_frame(self, controller):
        #if self.listenerEnabled == True:

            self.lastFrame = controller.frame()

            for n in range(79):
                if(len(self.lastFrames) == 80):
                    self.lastFrames.pop(0)
                    self.lastFrames.append(controller.frame(n))
                else:
                    self.lastFrames.append(controller.frame(n))

            if (self.getFrames == True and len(self.listOfEightyFrames) != 80):
                self.listOfEightyFrames.append(controller.frame())
            else:
                self.getFrames = False

            #print("Lectura del Leap" + str(len(self.lastFrame.hands)))
            #self.write()
            #self.listenerEnabled = False






    def set_textBox(self, textBox):
        self.textBox = textBox


    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb



class Reader(Tk):

    def __init__(self):
        Tk.__init__(self)
        speak = wincl.Dispatch("SAPI.SpVoice")
        #speak.Speak("A")
        self.leap = Leap.Controller()
        self.title("Touch Points")
        self.geometry("800x600")
        self.mainFrame = Frame(self, width=800, height=600, bg="black")
        self.mainFrame.place(x=0,y=0)

        self.infoReadTextBox = Text(self, width = 4, height=1, font=("Consolas", 72))
        self.infoReadTextBox.place(x=10, y=300)
        self.infoReadTextBox.insert(END, "HOLA")
        self.infoReadTextBox.config(state=DISABLED)


        self.entrySign = Entry(self, font=("Consolas", 32))
        self.entrySign.place(x=5, y=100)
        self.entrySign.bind("<Return>", self.setSignToRead)

        self.labelSignToRead = Label(self, bg="black", fg="Pink", text="Digite el codigo de gesto", font=("Consolas", 32))
        self.labelSignToRead.place(x=5, y=0)

        self.labelSignRead = Label(self, bg="black", fg="Pink", text="Codigo de gesto leido", font=("Consolas", 32))
        #self.labelSignRead.place(x=5, y=200)

        self.getFrameButton = Button(self, command = self.getLastFrame, text="Capturar Cuadro", bg="Pink", font=("Consolas", 32))
        self.getFrameButton.place(x=340, y=500)

        self.deleteLastButton = Button(self, command=self.deleteLastFrame, text = "Borrar ultimo cuadro", bg="Pink", font=("Consolas", 32))
        self.deleteLastButton.place(x=0,y=200)

        self.listener = Listener()
        self.leap.add_listener(self.listener)
        self.listener.set_textBox(self.infoReadTextBox)

        self.lastFrameProcessed = Leap.Frame
        self.frameToCompare = Leap.Frame

        self.gestureToReadCode = 0


        self.finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

        self.client = mqtt.Client("leapLesco")
        self.client.connect("iot.eclipse.org", 1883, 60)





    def deleteLastFrame(self):
        msgJson = {'command': 'delete_last'}
        self.client.publish("leapLesco", json.dumps(msgJson))
        print("ultimo borrado")

    def setSignToRead(self, event):
        try:
            self.gestureToReadCode = int(self.entrySign.get())
            self.getLastFrame()
            print("Gesto a leer: "+self.entrySign.get())
        except Exception as ValueError:
            print(self.entrySign.get(), '\n', 'Error de Entrada')

    def getLastFrame(self):
        self.lastFrameProcessed = self.listener.lastFrame
        self.lastFiveFramesProcessed = self.listener.lastFrames
        self.listener.getFrames = True

        while(len(self.listener.listOfEightyFrames) != 80):
            print(len(self.listener.listOfEightyFrames))

        self.getFrameInfo(self.listener.listOfEightyFrames[-1], self.listener.listOfEightyFrames)

        self.listener.listOfEightyFrames = []
        self.listener.getFrames = False

        print("Last Frame Updated")

        #self.getFrameInfo(self.lastFrameProcessed, self.lastFiveFramesProcessed)


    def getFrameInfo(self, frame, lastFiveFrames):
        self.handType = ""

        self.frameToCompare = lastFiveFrames[0]

        for n in range(len(frame.hands)):
            if frame.hands[n].is_right: self.handType = "Right"
            else: self.handType = "Left"

            print(str(self.handType))

            print ("Hand Movement: \n" + " Position X LastFrame: "+ str(frame.hands[n].palm_position.x)+
                   " Position X FirstFrame: "+ str(self.frameToCompare.hands[n].palm_position.x)+ " \nDelta X: " +
                   str(frame.hands[n].palm_position.x - self.frameToCompare.hands[n].palm_position.x) +
                   " \nPosition Y LastFrame: " + str(frame.hands[n].palm_position.y) + " Position Y FirstFrame: "+ str(self.frameToCompare.hands[n].palm_position.y)+
                   " \nDelta Y: " + str(
                        frame.hands[n].palm_position.y - self.frameToCompare.hands[n].palm_position.y) +
                   " \nPosition Z LastFrame: " + str(frame.hands[n].palm_position.z) + " Position Z FirstFrame: "+ str(self.frameToCompare.hands[n].palm_position.z)+
                   " \nDelta Z: " + str(
                        frame.hands[n].palm_position.z - self.frameToCompare.hands[n].palm_position.z))

            for m in range(len(frame.hands[n].fingers)):
                print ("Finger Type: " + self.finger_names[frame.hands[n].fingers[m].type] + " Tip Direction X: " + str(
                    frame.hands[n].fingers[m].direction.x) + " Tip Direction Y: " + str(frame.hands[n].fingers[m].direction.y) + " Tip Direction Z: " + str(
                    frame.hands[n].fingers[m].direction.z))
            self.createJSON(frame, self.frameToCompare)

#Last frame es el primero de los 80, first frame es el ultimo de los 80
    def createJSON(self, firstFrame, lastFrame):
        if(len(lastFrame.hands) ==1):
            frameJson = {'valid': lastFrame.is_valid, 'frameId': lastFrame.id, 'hands': []}
            for hand in lastFrame.hands:
                handtype = 0 if hand.is_left else 1
                handJson = {'valid': hand.is_valid, 'type': handtype, 'id': hand.id, 'fingers': [], 'gesture': self.gestureToReadCode}
                handJson['direction'] = {'x': hand.direction.x, 'y': hand.direction.y, 'z': hand.direction.z}
                handJson['deltas'] = {'x': firstFrame.hands[0].palm_position.x - hand.palm_position.x,'y': firstFrame.hands[0].palm_position.y -hand.palm_position.y,
                                      'z': firstFrame.hands[0].palm_position.z - hand.palm_position.z}
                for finger in hand.fingers:
                    fingerJson = {'valid': finger.is_valid, 'bones': [], 'type': finger.type, 'id': finger.id,
                                  'direction': {'x': finger.direction.x, 'y': finger.direction.y, 'z': finger.direction.z}}
                    for index in range(4):
                        fingerJson['bones'].append({'valid': finger.bone(index).is_valid, 'type': finger.bone(index).type,
                                                    'direction': {'x': finger.bone(index).direction.x,
                                                                  'y': finger.bone(index).direction.y,
                                                                  'z': finger.bone(index).direction.z}})
                    handJson['fingers'].append(fingerJson)
                frameJson['hands'].append(handJson)
            if (lastFrame.hands):
                msgJson={'command':'frame', 'frame':frameJson}

                self.client.publish("leapLesco", json.dumps(msgJson))

            print json.dumps(frameJson)

        else:
            print("MANO FANTASMAAA")




    def write(self, string):
        self.infoReadTextBox.config(state=NORMAL)
        self.infoReadTextBox.delete(1.0, END)
        self.infoReadTextBox.insert(END, string)
        self.infoReadTextBox.config(state=DISABLED)




def main():
    Reader().mainloop()


if __name__ == "__main__":
    main()






