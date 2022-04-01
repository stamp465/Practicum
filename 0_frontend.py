from tkinter import *
from turtle import delay
from PIL import Image, ImageTk
import cv2


wn = Tk()
wn.geometry("800x800")
wn.resizable(0,0)
wn.option_add("*font","tahoma 30 normal")

fm1 = Frame(wn)
fm1.pack(side=TOP)

fm2 = Frame(wn)
fm2.pack(side=TOP)

label_greeding = Label(fm1,text="กล้องตรวจจับใบหน้า",justify=CENTER)
label_greeding.pack(side=TOP,padx=10,pady=10)
label_camera =Label(fm1,justify=CENTER)
label_camera.pack(padx=10,pady=10)

cap= cv2.VideoCapture(0)

def show_frames():
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   imgtk = ImageTk.PhotoImage(image = img)
   label_camera.imgtk = imgtk
   label_camera.configure(image=imgtk)
   label_camera.after(10, show_frames)


show_frames()

label1 = Label(fm2)
label1.pack(pady=5)

strvar1 = StringVar()
ent1 = Entry(fm2,width=15,state=DISABLED,textvariable=strvar1,justify=CENTER)
ent1.pack(pady=5)

label2 = Label(fm2)
label2.pack(pady=5)

numr1 = 11
numr2 = 6

def reset_ent():
    global numr2
    numr2-=1
    label2.config(text=f"เวลาจะรีเซ็ตในอีก {numr2}")
    id = label2.after(1000,reset_ent)
    if (numr2==0):
        label2.config(text=f"หมดเวลา")
    
    if (numr2 < 0):
        global numr1
        numr1 = 11
        strvar1.set('')
        label2.config(text='')
        label2.after_cancel(id)
        update()
        

def update():
    global numr1
    numr1-=1
    label1.config(text=f"นับถอยหลัง {numr1}")  
    id = label1.after(1000,update) 
    
    if (numr1==0):
        global numr2
        numr2 = 6
        label1.config(text=f"นับถอยหลัง {numr1}")  
        strvar1.set("คุณสามารถผ่านได้")
        label1.after_cancel(id)
        reset_ent()
        
update()
wn.mainloop()

