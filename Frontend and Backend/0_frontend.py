from logging import exception
from tkinter import *
from turtle import delay
from PIL import Image, ImageTk
import cv2

import datetime as dt

from numpy import e

pre_save = '0'

wn = Tk()
wn.geometry("800x800")
wn.resizable(0,0)
wn.option_add("*font","tahoma 30 bold")

fm1 = Frame(wn)
fm1.pack(side=TOP)

fm2 = Frame(wn)
fm2.pack(side=TOP)


cap= cv2.VideoCapture(0)
label_greeding = Label(fm1,text="กล้องตรวจจับใบหน้า",justify=CENTER)
label_greeding.pack(side=TOP,padx=10,pady=10)
label_camera =Label(fm1,justify=CENTER)
label_camera.pack(padx=10,pady=10)

def show_frames():
    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = img)
    label_camera.imgtk = imgtk
    label_camera.configure(image=imgtk)
    label_camera.after(10, show_frames)



label1 = Label(fm2)
label1.pack(pady=5)


ent1 = Label(fm2,justify=CENTER)
ent1.pack(pady=5)

label2 = Label(fm2)
label2.pack(pady=5)

enter_log = False

def scan_face():
    global pre_save,enter_log
    label1.after(1000,scan_face) 
    try:
        file_status = open(file="./log/1_status.txt",mode="r")
        save = file_status.read().strip('\n')   
    except Exception as err:
        print(err)
    else:
        file_status.close()
        print(save)
    if (save=='0'):
        if pre_save == '1' :
            ent1.config(text="")
            ent1.config(text="รอรหัสผ่านนานเกินไป แสกนใบหน้าใหม่")
            if not enter_log :
                x = dt.datetime.now()
                f = open('./log/1_status.log', 'a')
                f.write(x.strftime("%c")+' ... ')
                f.write("too long for waiting password, reset to scan face")
                f.write('\n')
                f.close()
                enter_log = True
        elif pre_save == '2' :
            ent1.config(text="")
            ent1.config(text="ประตูปิดแล้ว แสกนใบหน้าใหม่")
            if not enter_log :
                x = dt.datetime.now()
                f = open('./log/1_status.log', 'a')
                f.write(x.strftime("%c")+' ... ')
                f.write("door close, reset to scan face")
                f.write('\n')
                f.close()
                enter_log = True
        else :
            ent1.config(text="")
            ent1.config(text="รอแสกนใบหน้า")
    if (save=='1'):
        ent1.config(text="")
        ent1.config(text="รอใส่รหัสผ่าน")
        enter_log = False
        pre_save = save
    if (save=='2'):
        ent1.config(text="")
        ent1.config(text="ยืนยันรหัสผ่านเสร็จสิ้น เปิดประตูได้")
        pre_save = save
        enter_log = False
        
show_frames()    
scan_face()  
mainloop()

