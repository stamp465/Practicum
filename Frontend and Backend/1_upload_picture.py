from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

import datetime as dt

wn = Tk()
wn.geometry("800x600")
wn.resizable(0,0)
wn.option_add("*font","tahoma 15 bold")

fm1 = Frame(wn)
fm1.pack(side=TOP,padx=5,pady=5)
fm2 = Frame(wn)
fm2.pack(side=TOP,padx=5,pady=5)
fm3 = Frame(wn)
fm4 = Frame(wn)
fm3.pack(side=TOP,padx=5,pady=5)
fm4.pack(side=TOP,padx=5,pady=5)

strvar1 = StringVar()
lb = Label(fm1,text="Choose File : ")
lb.grid(row=0,column=0,padx=3,pady=7)
ent = Entry(fm1,textvariable=strvar1)
ent.grid(row=0,column=1,padx=3,pady=7)

strvar2 = StringVar(value=0)
radiobutton1 = Radiobutton(fm2,text="Can Pass",variable=strvar2,value="Can_Pass")
radiobutton2 = Radiobutton(fm2,text="Can not Pass",variable=strvar2,value="Can_not_Pass")

radiobutton1.grid(row=0,column=0,padx=5,pady=5,sticky=NW)
radiobutton2.grid(row=1,column=0,padx=5,pady=5,sticky=NW)

lb = Label(fm3,text="Upload Photo",justify=CENTER)
lb.pack(side=LEFT,padx=5,pady=5)

bt1 = Button(fm3,text="Choose file",command=lambda:choose_file(),justify=CENTER)
bt1.pack(side=LEFT,padx=5,pady=5)


bt3 = Button(fm4,justify=CENTER,text="Upload",command=lambda:save_file())
bt3.grid(row=3,column=2,padx=5,pady=10)

def choose_file():
    global img,im,bt2
    bt2 = Button(fm4,justify=CENTER)
    filename = filedialog.askopenfilename(filetypes=[('Jpg Files', '*.jpg')])
    img=Image.open(filename)
    im = Image.open(filename)
    img_resized=img.resize((300,300)) 
    img=ImageTk.PhotoImage(img_resized)
    bt2.config(image=img) 
    bt2.grid(row=2,column=2)

def save_file():
    global im,bt2
    name = strvar1.get()
    folder = strvar2.get()
    #print(name,folder)
    im.save(f"./{folder}/{name}.jpg", 'JPEG')
    messagebox.showinfo("แสดงผลลัพธ์","อัพโหลดรูปภาพสำเร็จ")

    x = dt.datetime.now()
    f = open('./log/1_status.log', 'a')
    f.write(x.strftime("%c")+' ... ')
    f.write(f'upload {name}.jpg to folder {folder}')
    f.write('\n')
    f.close()

    strvar1.set("")
    strvar2.set(value=0)
    bt2.destroy()

    
 


mainloop()
