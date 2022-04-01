import face_recognition
import cv2
import numpy as np
import time
import os


from practicum import find_mcu_boards, McuBoard, PeriBoard
devices = find_mcu_boards()
mcu = McuBoard(devices[0])
peri = PeriBoard(mcu)

# Get own path and picture path
working_directory = os.getcwd()
can_pass = os.listdir(working_directory+'/Can_Pass')
can_not_pass = os.listdir(working_directory+'/Can_not_Pass')

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
pass_face_name = list()
pass_not_face_name = list()

can_pass_image = list()
can_pass_face_encoding = list()
for i in range(len(can_pass)) :
    pass_face_name.append( can_pass[i].split('.')[0] )
    can_pass_image.append(face_recognition.load_image_file(working_directory+'/Can_Pass/'+can_pass[i]))
    can_pass_face_encoding.append(face_recognition.face_encodings(can_pass_image[i])[0])

can_not_pass_image = list()
can_not_pass_face_encoding = list()
for i in range(len(can_not_pass)) :
    pass_not_face_name.append( can_not_pass[i].split('.')[0] )
    can_not_pass_image.append(face_recognition.load_image_file(working_directory+'/Can_not_Pass/'+can_not_pass[i]))
    can_not_pass_face_encoding.append(face_recognition.face_encodings(can_not_pass_image[i])[0])


# Create arrays of known face encodings and their names
known_face_encodings = can_pass_face_encoding + can_not_pass_face_encoding
known_face_names = pass_face_name + pass_not_face_name

#print(known_face_names)


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

timeout = 150           # 150 sec
start_time = 0


while True:

    try :
        start_tt = mcu.usb_read(4, length=1)

        # 2 == door opened
        if start_tt[0] == 2 :
            #face_names = []
            #process_this_frame = True
            #print(face_names)
            print("open door")

        # 1 == check pass
        if start_tt[0] == 1 :
            if time.time() < start_time + timeout:
                tmp = mcu.usb_read(2, length=10)
                
                read_hardware_password = ""
                print(tmp)
                for i in tmp:
                    if str(i) != "0" :
                        read_hardware_password = read_hardware_password + str(i)
                print(read_hardware_password)

                if read_hardware_password == "" :
                    pass
                elif read_hardware_password == "3579" :
                    print("Is TRUE")
                    mcu.usb_write(3, value=1)
                    # break
                else :
                    print("Is False")
                    mcu.usb_write(3, value=0)

            else:
                mcu.usb_write(1, value=0)         # set end        

        # 0 == check face
        if start_tt[0] == 0 :
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    face_names.append(name)
                
                #check face_names in pass_face_name
                check_face = False
                for i in face_names :
                    if i in pass_face_name :
                        check_face = True

                if check_face :
                    # mcu.usb_write(0, value=1, index=0)
                    # mcu.usb_write(3, value=90)
                    # peri.set_led(1,1)

                    mcu.usb_write(1, value=1)         # set start
                    
                    start_time = time.time()
                    
                print(face_names)
            process_this_frame = not process_this_frame

    except :
        print("ERROR !!!!!!!!!!!!!!!!!!!!!!")
        devices = find_mcu_boards()
        mcu = McuBoard(devices[0])
        peri = PeriBoard(mcu)
    
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    time.sleep(1)       # sleep 1 sec

    


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
