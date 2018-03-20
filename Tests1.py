import Tkinter as tk
import Leap


from Tkinter import *


class Listener(Leap.Listener):

    def __init__(self):
        Leap.Listener.__init__(self)
        self.listenerEnabled = False
        self.lastFrame = Leap.Frame
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
        self.leap = Leap.Controller()
        self.title("Touch Points")
        self.geometry("800x600")
        self.mainFrame = Frame(self, width=800, height=600, bg="black")
        self.mainFrame.place(x=0,y=0)

        self.infoReadTextBox = Text(self, width = 4, height=1, font=("Monospace", 72))
        self.infoReadTextBox.place(x=10, y=300)
        self.infoReadTextBox.insert(END, "HOLA")
        self.infoReadTextBox.config(state=DISABLED)


        self.entrySign = Entry(self, font=("Monospace", 32))
        self.entrySign.place(x=5, y=100)
        self.entrySign.bind("<Return>", self.setSignToRead)

        self.labelSignToRead = Label(self, bg="black", fg="Pink", text="Digite el codigo de gesto", font=("Monospace", 32))
        self.labelSignToRead.place(x=5, y=0)

        self.labelSignRead = Label(self, bg="black", fg="Pink", text="Codigo de gesto leido", font=("Monospace", 32))
        self.labelSignRead.place(x=5, y=200)

        self.getFrameButton = Button(self, command = self.getLastFrame, text="Capturar Cuadro", bg="Pink", font=("Monospace", 32))
        self.getFrameButton.place(x=340, y=500)

        self.listener = Listener()
        self.leap.add_listener(self.listener)
        self.listener.set_textBox(self.infoReadTextBox)

        self.lastFrameProcessed = Leap.Frame


        self.finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']



    def setSignToRead(self, event):
        try:
            print(self.entrySign.get())
        except Exception as ValueError:
            print(self.entrySign.get(), '\n', 'Error de Entrada')

    def getLastFrame(self):
        self.lastFrameProcessed = self.listener.lastFrame

        print("Last Frame Updated")

        self.getFrameInfo(self.lastFrameProcessed)


    def getFrameInfo(self, frame):
        self.handType = ""
        for hand in frame.hands:
            if hand.is_right: self.handType = "Right"
            else: self.handType = "Left"

            print(str(self.handType))


            for finger in hand.fingers:
                print ("Finger Type: " + self.finger_names[finger.type] + " Tip Direction X: " + str(
                    finger.direction.x) + " Tip Direction Y: " + str(finger.direction.y) + " Tip Direction Z: " + str(
                    finger.direction.z))


            thumbFinger = hand.fingers[0]
            indexFinger = hand.fingers[1]
            middleFinger = hand.fingers[2]
            ringFinger = hand.fingers[3]
            pinkyFinger = hand.fingers[4]

            if (thumbFinger.direction.x < 0 and indexFinger.direction.x < 0 and middleFinger.direction.x < 0 and ringFinger.direction.x < 0 and pinkyFinger.direction.x > 0 and
                thumbFinger.direction.y > 0 and indexFinger.direction.y < 0 and middleFinger.direction.y < 0 and ringFinger.direction.y < 0 and pinkyFinger.direction.y > 0 and
                thumbFinger.direction.z < 0 and pinkyFinger.direction.z < 0):

                print("Y\n\n\n\n\n")
                self.write("Y")

            else:
                self.write("NONE")



    def write(self, string):
        self.infoReadTextBox.config(state=NORMAL)
        self.infoReadTextBox.delete(1.0, END)
        self.infoReadTextBox.insert(END, string)
        self.infoReadTextBox.config(state=DISABLED)




def main():
    Reader().mainloop()


if __name__ == "__main__":
    main()






