import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
from flask import Flask, request, jsonify, make_response
import csv

class App:
    def __init__(self,window,video_source=0):
        self.window = window
    
        self.video_source = video_source

        self.vid = MyVideoCapture(self.video_source)
        self.state = False

        self.background = tkinter.Canvas(window, width = 1920, height = 1080)
        self.background.place(x=0, y=0)
        self.img_background = PIL.ImageTk.PhotoImage(PIL.Image.open('background.png').convert('RGB'))
        self.background.create_image(0, 0, image = self.img_background, anchor = tkinter.NW)

        self.stream = tkinter.Canvas(window, width = 950, height = 720)
        self.stream.grid(row=0, rowspan=2, column=0, padx=55, pady=150)

        self.rain = tkinter.Canvas(window, width = 794, height = 500)
        self.rain.grid(row=1, column=1, padx=0, pady=220)

        self.btn = tkinter.Button(window, text='START', font=("", 40))
        self.btn.grid(row=1, column=1, padx=300, pady=80, sticky=tkinter.S+tkinter.W+tkinter.E)


        def StartStop(event):
            if self.state == False:
                self.state = not self.state
                self.btn.configure(text="STOP")
                file = open('rainInfo.csv', 'w')
                file.write("0\n")
                file.close()
                self.count = 0
                self.tmp = 0
            else:
                self.state = False
                self.btn.configure(text="START")

        self.btn.bind("<Button-1>", StartStop)


        self.delay = 15
        self.update()


    def update(self):
        ret,frame = self.vid.get_frame()
        self.img_rain = PIL.ImageTk.PhotoImage(PIL.Image.open('stop.png').convert('RGB'))

        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            if self.state is not False:
                self.img_rain = PIL.ImageTk.PhotoImage(PIL.Image.open('norain.png').convert('RGB'))
                #circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=57, param2=40, minRadius=50, maxRadius=100000)
                circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=70, param2=75, minRadius=50, maxRadius=1000)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for i in circles[0,:]:
                        cv2.circle(frame,(i[0],i[1]),i[2],(0,255,255),8)
                        cv2.circle(frame,(i[0],i[1]),2,(255,0,0),3)
                    self.img_rain = PIL.ImageTk.PhotoImage(PIL.Image.open('rain.png').convert('RGB'))
                    self.count = 0
                    if self.tmp == 0:
                        file = open('rainInfo.csv', 'w')
                        file.write("1\n")
                        file.close()
                        print(1)
                    self.tmp = 1
                else:
                    self.count += 1
                    if self.count < 30 and self.tmp == 1:
                        self.img_rain = PIL.ImageTk.PhotoImage(PIL.Image.open('rain.png').convert('RGB'))
                    elif self.count >= 30:
                        if self.tmp == 1:
                            file = open('rainInfo.csv', 'w')
                            file.write("0\n")
                            file.close()
                            print(0)
                        self.tmp = 0
                
            self.img_stream = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame)) 
            self.stream.create_image(0, 0, image = self.img_stream, anchor = tkinter.NW)
            self.rain.create_image(0, 0, image = self.img_rain, anchor = tkinter.NW)


        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret,frame = self.vid.read()
        if ret:
            return(ret,cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    def __del__(self):
       if self.vid.isOpened():
           self.vid.release()

def main():
    app = App(tkinter.Tk(),"http://192.168.1.44:8080/?action=stream")
    app.window.mainloop()

if __name__ == '__main__':
    main()