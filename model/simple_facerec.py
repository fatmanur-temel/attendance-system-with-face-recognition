import face_recognition
import cv2
import os
import glob
import numpy as np


class SimpleFacerec:
    def __init__(self):
        #
        self.known_face_encodings = []
        self.known_face_names = []

        # Daha hızlı olması için frame'i yeniden boyutlandır
        self.frame_resizing = 0.25

    # images klasöründeki fotoğrafların yüklenmesi
    def load_encoding_images(self, images_path):

        #main'den gönderilen path'deki görsellerin liste olarak tutulması
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        # Path'de kaç tane fotoğraf bulunduysa yazdır
        print("{} encoding images found.".format(len(images_path)))


        for img_path in images_path:
            img = cv2.imread(img_path)

            #BGR --> RGB renk dönüşümü
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Dosya adını yalnızca ilk path'den alın.
            basename = os.path.basename(img_path)

            # Dosya uzantısını ayırır
            (filename, ext) = os.path.splitext(basename)

            # fotoğraflar matris haline getirildi
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Dosya adını ve matrisleri listelere ekledik (append)
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):

        #yüz bulma işleminin daha hızlı olması için frame 1/4 yapılır
        small_frame = cv2.resize(frame, (0,0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        # videodaki geçerli frame'deki yüz bulunur.
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # videoda bulunan yüz ile klasördeki yüzler arasında eşleşme var mı diye kontrol edilir
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

            name = "Unknown"

            #karşılaştırma sonucunda bir öklid mesafesi elde edilir
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            #array'daki min index'i döndürür
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Çerçeveyi hızlı bir şekilde yeniden boyutlandırarak koordinatları ayarlamak için numpy dizisine dönüştürün
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names
