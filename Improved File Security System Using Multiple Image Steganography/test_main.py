

import os
from pvd_lib import pvd_lib
import cv2

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
        block.append(chunk.decode('latin1'))
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
'''
block, files = sliceText("angular.txt", "images")
for i in range(len(files)):
    img = cv2.imread(files[i])
    img = cv2.resize(img, (600,600))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite(files[i], img)
    PVDEncoding(files[i], block[i])
'''
output = PVDDecoding("images")
print(output)
    
