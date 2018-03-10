from Tkinter import Frame, Canvas, YES, BOTH

import Leap


class TouchPointListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):
        self.paintCanvas.delete("all")
        frame = controller.frame()

        interactionBox = frame.interaction_box

        for pointable in frame.pointables:
            normalizedPosition = interactionBox.normalize_point(pointable.tip_position)
            if (pointable.touch_distance > 0 and pointable.touch_zone != Leap.Pointable.ZONE_NONE):
                color = self.rgb_to_hex((0, 255 - 255 * pointable.touch_distance, 0))

            elif (pointable.touch_distance <= 0):
                color = self.rgb_to_hex((-255 * pointable.touch_distance, 0, 0))
                # color = self.rgb_to_hex((255,0,0))

            else:
                color = self.rgb_to_hex((0, 0, 200))

            self.draw(normalizedPosition.x * 800, 600 - normalizedPosition.y * 600, 40, 40, color)

    def draw(self, x, y, width, height, color):
        self.paintCanvas.create_oval(x, y, x + width, y + height, fill=color, outline="")

    def set_canvas(self, canvas):
        self.paintCanvas = canvas

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb


class PaintBox(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.leap = Leap.Controller()
        self.painter = TouchPointListener()
        self.leap.add_listener(self.painter)
        self.pack(expand=YES, fill=BOTH)
        self.master.title("Touch Points")
        self.master.geometry("800x600")

        # create Canvas component
        self.paintCanvas = Canvas(self, width="800", height="600")
        self.paintCanvas.pack()
        self.painter.set_canvas(self.paintCanvas)


def main():
    PaintBox().mainloop()


if __name__ == "__main__":
    main()