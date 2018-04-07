#Biblioteca para Interfaz grafica
import Tkinter as tk
from Tkinter import *
#Biblioteca para utilizar los comandos del Leap
import Leap
#Biblioteca para enviar datos en formato JSON
import json
#Bilbioteca para comunicacion por red
import paho.mqtt.client as mqtt


#Clase del Leap Motion que incluye todos sus metodos

class Listener(Leap.Listener):
#Metodo de inicializacion
    def __init__(self):
        Leap.Listener.__init__(self)
        self.listenerEnabled = False
        self.lastFrame = Leap.Frame
        self.lastFrames = [Leap.Frame, Leap.Frame, Leap.Frame, Leap.Frame, Leap.Frame]
        self.numberOfFramesAnalyzed = 0
        self.listOfEightyFrames=[]
        self.getFrames = False #Variable de control para obtener datos del Leap
        print(str(self.listenerEnabled))

    def on_init(self, controller):
        print "Initialized"
#Metodo que identifica cuando el Leap Motion es conectado
    def on_connect(self, controller):
        print "Connected"
#Metodo que identifica cuando el Leap Motion es desconectado
    def on_disconnect(self, controller):
        print("Disconnected")

#Metodo principal encargado de obtener frames con los datos del Leap
    def on_frame(self, controller):
        #if self.listenerEnabled == True:

            self.lastFrame = controller.frame()

            for n in range(79): #Ciclo encargado de ir actualizando los ultimos 80 cuadros que lee el Leap
                if(len(self.lastFrames) == 80):
                    self.lastFrames.pop(0)
                    self.lastFrames.append(controller.frame(n))
                else:
                    self.lastFrames.append(controller.frame(n))

            if (self.getFrames == True and len(self.listOfEightyFrames) != 80):
                self.listOfEightyFrames.append(controller.frame())
            else:
                self.getFrames = False


class Reader(Tk):

    def __init__(self):
        Tk.__init__(self)

        #Inicializacion de controlador para utilizar el Leap
        self.leap = Leap.Controller()

        #Metodos de interfaz de Tkinter
        self.title("Interfaz de entrenamiento")
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

        self.analyzeButton = Button(self, command = self.analyze, text = "Analisis", bg="Pink", font=("Consolas", 32))
        self.analyzeButton.place(x=500, y=350)

        self.deleteLastButton = Button(self, command=self.deleteLastFrame, text = "Borrar ultimo cuadro", bg="Pink", font=("Consolas", 32))
        self.deleteLastButton.place(x=0,y=200)

        self.listener = Listener()
        self.leap.add_listener(self.listener)


        self.lastFrameProcessed = Leap.Frame
        self.frameToCompare = Leap.Frame

        self.gestureToReadCode = 0


        self.finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

        self.client = mqtt.Client("leapLesco")
        self.client.connect("iot.eclipse.org", 1883, 60)


    #Funcion que indica al Interprete que debe analizar los gestos enviados
    def analyze(self):
        msgJson = {'command': 'analyze'}
        self.client.publish("leapLesco", json.dumps(msgJson))
        print("analisis solicitado")

    def deleteLastFrame(self):
        msgJson = {'command': 'delete_last'}
        self.client.publish("leapLescoTraining", json.dumps(msgJson))
        print("ultimo borrado")

    def setSignToRead(self, event):
        try:
            self.gestureToReadCode = int(self.entrySign.get())
            self.getLastFrame()
        except Exception as ValueError:
            print(self.entrySign.get(), '\n', 'Error de Entrada')

    #Funcion encargada de obtener el ultimo cuadro y el primero desde que se empezo a obtener datos
    def getLastFrame(self):
        self.lastFrameProcessed = self.listener.lastFrame
        self.lastFiveFramesProcessed = self.listener.lastFrames
        self.listener.getFrames = True
        print("inicia muestra")
        while(len(self.listener.listOfEightyFrames) != 80):
            pass
        print("finaliza muestra")
        self.getFrameInfo(self.listener.listOfEightyFrames[-1], self.listener.listOfEightyFrames)

        self.listener.listOfEightyFrames = []
        self.listener.getFrames = False

    #Funcion encargada de obtener los datos de las manos que se observan en el cuadro final e inicial para posteriormente
    #enviar el JSON a la biblioteca Keras
    def getFrameInfo(self, frame, lastEightyFrames):
        self.handType = ""

        self.frameToCompare = lastEightyFrames[0]
        if(len(frame.hands) != 0):
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

                """for m in range(len(frame.hands[n].fingers)):
                    print ("Finger Type: " + self.finger_names[frame.hands[n].fingers[m].type] + " Tip Direction X: " + str(
                        frame.hands[n].fingers[m].direction.x) + " Tip Direction Y: " + str(frame.hands[n].fingers[m].direction.y) + " Tip Direction Z: " + str(
                        frame.hands[n].fingers[m].direction.z))"""
                self.createJSON(frame, self.frameToCompare)
        else:#En caso de que no haya manos, se indica un espacio al interprete
            msgJson = {'command': 'space'}
            self.client.publish("leapLesco", json.dumps(msgJson))
            print("ESPACIO")
#Last frame es el primero de los 80, first frame es el ultimo de los 80
    #Funcion encargada de crear y enviar el JSON por mqtt, solo se envian datos de la mano derecha
    def createJSON(self, firstFrame, lastFrame):
        if(len(lastFrame.hands) >=1):
            frameJson = {'valid': lastFrame.is_valid, 'frameId': lastFrame.id, 'hands': []}
            for hand in lastFrame.hands:
                handtype = 0 if hand.is_left else 1

                if(handtype == 1):#Solo se envian datos de la mano derecha
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

                self.client.publish("leapLescoTraining", json.dumps(msgJson))

            print json.dumps(frameJson)

        #elif len(lastFrame.hands) > 1:
         #   print("MANO FANTASMAAA")



    def write(self, string):

        self.infoReadTextBox.config(state=NORMAL)
        self.infoReadTextBox.delete(1.0, END)
        self.infoReadTextBox.insert(END, string)
        self.infoReadTextBox.config(state=DISABLED)

def main():
    Reader().mainloop()


if __name__ == "__main__":
    main()






