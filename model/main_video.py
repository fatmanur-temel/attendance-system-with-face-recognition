import cv2
from simple_facerec import SimpleFacerec
from attendance import Attendance
from register import Register

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Encode attendance file
atd = Attendance()
atd.__int__("Matemetik")
file_name = atd.create_file()

reg = Register()

# Load Camera
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, "fotograf cekmek icin q bas", (10, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (200, 0, 200), 1)
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        cv2.imshow("Frame", frame)


        if name != 'Unknown':
            atd.create_attendance(name, file_name, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        reg.create_window(frame)

    if cv2.waitKey(1) == ord('e'):
        break


atd.create_excel(file_name)

cap.release()
cv2.destroyAllWindows()

