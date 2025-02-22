from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import numpy as np
import cv2
import os
from pvd_lib import pvd_lib

main = Tk()
main.title("Improved File Security System Using Multiple Image Steganography")
main.geometry("1300x1200")

global image_path, text_path

pvd_obj = pvd_lib()

def sliceText(text_file, images_path):
    with open(text_file, "rb") as myfile:
        data = myfile.read()
    myfile.close()
    files = []
    for root, dirs, directory in os.walk(images_path):
        for j in range(len(directory)):
            name = os.path.basename(root)
            if 'Thumbs.db' not in directory[j]:
                files.append(root+"/"+directory[j])

    length = len(data)
    size = int(length / len(files))
    tot_blocks = len(files)
    start = 0
    end = size
    block = []
    for i in range(0, tot_blocks):
        chunk = data[start:end]
        block.append(chunk.decode('latin1'))
        start = end
        end = end + size
    remain =  length - start
    if remain > 0:
        chunk = data[start:length]
        last = block[len(block)-1]
        last += chunk.decode('latin1')
        block[len(block)-1] = last
        print(str(start)+" "+str(length)+" "+str(chunk.decode('latin1')))
    return block, files

def PVDEncoding(image_path, slice_msg):
    base_name = os.path.basename(os.path.dirname(image_path))
    with open("data.txt", "wb") as myfile:
        myfile.write(slice_msg.encode())
    myfile.close()
    if os.path.exists('Encoded_Images/'+base_name) == False:
        os.makedirs('Encoded_Images/'+base_name)
    img_name = os.path.basename(image_path)
    img_name = img_name.replace(".jpg", ".png")
    pvd_obj.pvd_embed(image_path, "data.txt", 'Encoded_Images/'+base_name+"/"+img_name)

def PVDDecoding(image_path):
    output = ""
    base_name = os.path.basename(image_path)
    files = []
    for root, dirs, directory in os.walk(image_path):
        for j in range(len(directory)):
            name = os.path.basename(root)
            if 'Thumbs.db' not in directory[j]:
                files.append(root+"/"+directory[j])
    for i in range(len(files)):
        img_name = os.path.basename(files[i])
        img_name = img_name.replace(".jpg", ".png")
        print(files[i]+" == "+'Encoded_Images/'+base_name+"/"+os.path.basename(files[i]))
        pvd_obj.pvd_extract(files[i], "data.txt", 'Encoded_Images/'+base_name+"/"+img_name)
        with open("data.txt", "rb") as myfile:
            data = myfile.read()
        myfile.close()
        output += data.decode('latin1')
    return output           

def uploadImage():
    global image_path
    text.delete('1.0', END)
    image_path = filedialog.askdirectory(initialdir = ".")
    text.insert(END,image_path+" loaded\n\n")
    tf1.insert(0, image_path)

def uploadText():
    global text_path, image_path
    text_path = askopenfilename(initialdir = ".")
    tf2.insert(0, text_path)
    text.insert(END,text_path+" loaded")
    block, files = sliceText(text_path, image_path)
    for i in range(len(files)):
        img = cv2.imread(files[i])
        img = cv2.resize(img, (600,600))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(files[i], img)
        PVDEncoding(files[i], block[i])
        text.insert(END,"Slice Message : "+str(block[i])+"\n")
        text.insert(END,"Hidden inside : "+str(files[i])+"\n\n")
        text.update_idletasks()
        text.update()

def ExtractText():
    text.delete('1.0', END)
    encoded_path = filedialog.askdirectory(initialdir = "Encoded_Images")
    tf3.insert(0, encoded_path)
    name = os.path.basename(encoded_path)
    print("extract "+name)
    output = PVDDecoding(name)
    text.insert(END,"Extracted Text = "+output)


font = ('times', 15, 'bold')
title = Label(main, text='Improved File Security System Using Multiple Image Steganography')
title.config(bg='mint cream', fg='olive drab')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 14, 'bold')
ff = ('times', 12, 'bold')

l1 = Label(main, text='Encoding Images Folder:')
l1.config(font=font1)
l1.place(x=50,y=100)

tf1 = Entry(main,width=35)
tf1.config(font=font1)
tf1.place(x=330,y=100)

uploadButton = Button(main, text="Upload Encoding Images", command=uploadImage)
uploadButton.place(x=720,y=100)
uploadButton.config(font=ff)

l2 = Label(main, text='Upload Text File:')
l2.config(font=font1)
l2.place(x=50,y=150)

tf2 = Entry(main,width=35)
tf2.config(font=font1)
tf2.place(x=330,y=150)

encodingButton = Button(main, text="Upload Text File to Hide & PVD Encode", command=uploadText)
encodingButton.place(x=720,y=150)
encodingButton.config(font=ff)

l3 = Label(main, text='Upload Folder to Extract Text:')
l3.config(font=font1)
l3.place(x=50,y=200)

tf3 = Entry(main,width=35)
tf3.config(font=font1)
tf3.place(x=330,y=200)

encodingButton = Button(main, text="PVD Decoding", command=ExtractText)
encodingButton.place(x=720,y=200)
encodingButton.config(font=ff)



font1 = ('times', 13, 'bold')
text=Text(main,height=20,width=120)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=250)
text.config(font=font1)

main.config(bg='gainsboro')
main.mainloop()
