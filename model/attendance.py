import datetime


class Attendance:
    def __int__(self, conn):
        # Veritabanı bağlantısı
        self.conn = conn

    def get_lesson_name(self):
        # O anki güncel gün ve saat bilgisi
        current_day = datetime.datetime.today().weekday() + 1  # Haftanın günleri 0'dan başladığı için +1 ekliyoruz
        current_time = datetime.datetime.now().time()

        # Veritabanı bağlantısını oluşturun
        cursor = self.conn.cursor()

        # SQL sorgusu
        query = "SELECT lesson_id FROM schedule WHERE day = %s AND start_time <= %s AND end_time >= %s"
        cursor.execute(query, (current_day, current_time, current_time))
        result = cursor.fetchone()

        lesson_id = result[0]
        
        if lesson_id == 1:
            lesson_name = "ders1"
        elif lesson_id == 2:
            lesson_name = "ders2"
        elif lesson_id == 3:
            lesson_name = "ders3"
        elif lesson_id == 4:
            lesson_name = "ders4"
        elif lesson_id == 5:
            lesson_name = "ders5"
        elif lesson_id == 6:
            lesson_name = "ders6"
        elif lesson_id == 7:
            lesson_name = "ders7"
        elif lesson_id == 8:
            lesson_name = "ders8"
        elif lesson_id == 9:
            lesson_name = "ders9"
        elif lesson_id == 10:
            lesson_name = "ders10"
        else:
            print("No lesson scheduled at the moment.")
            return

        return lesson_name


    def create_attendance(self,name,lesson_name):
        # İsimdeki boşluk karakterine göre ayrıştırma
        first_name, last_name, number = name.split(" ")

        # Anlık tarihin alınması
        current_date = datetime.date.today()

        # Veritabanı bağlantısını oluşturun
        cursor = self.conn.cursor()

        # Katılım kaydının var olup olmadığını kontrol etme
        cursor.execute("SELECT * FROM {} WHERE date = %s AND student_no = %s".format(lesson_name),
                   (current_date, number))
        existing_attendance = cursor.fetchone()

        if existing_attendance:
            return
        else:
            # Veritabanına katılım kaydının eklenmesi
            cursor.execute("INSERT INTO {} (student_no, date, student_name, student_surname) VALUES (%s, %s, %s, %s)".format(lesson_name),
                        (number, current_date, first_name, last_name))

            # Veritabanı işlemlerinin kaydedilmesi
            self.conn.commit()

            print("Attendance created for:", name)

        # Veritabanı bağlantısının kapatılması
        cursor.close()
