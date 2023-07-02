import cv2
from simple_facerec import SimpleFacerec
from attendance import Attendance
from register import Register
import psycopg2
import requests
import tempfile
import shutil
from urllib.parse import unquote
import os

conn = psycopg2.connect(
    host="localhost",
    database="attendance",
    user="postgres",
    password="123456"
)

# Veritabanı bağlantısını oluşturun
cursor = conn.cursor()

# Veritabanından fotoğraf URL'lerini çekme
cursor.execute("SELECT photo FROM student")
photo_urls = cursor.fetchall()

# Geçici dosyaları tutmak için bir klasör oluşturun
temp_dir = tempfile.mkdtemp()

# Fotoğrafları indirip geçici dosyalara kaydedin
for url in photo_urls:
    # URL'den dosya adını alma
    filename = unquote(url[0].split("/")[-1])

    # Geçici dosya yolu
    temp_file_path = os.path.join(temp_dir, filename)

    response = requests.get(url[0])
    response.raise_for_status()

    # Dosyayı geçici klasöre kaydetme
    with open(temp_file_path, "wb") as file:
        file.write(response.content)

    # İndirilen dosyanın yolunu yazdırma
    print("Downloaded image:", temp_file_path)

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images(temp_dir)

# Encode attendance file
atd = Attendance()
atd.__int__(conn)
lesson_name = atd.get_lesson_name()
print(lesson_name)

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
            atd.create_attendance(name,lesson_name)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        reg.create_window(frame)

    if cv2.waitKey(1) == ord('e'):
        break

# Geçici klasörü silme
shutil.rmtree(temp_dir)

cap.release()
cv2.destroyAllWindows()

# Veritabanı bağlantısını kapatma
conn.close()