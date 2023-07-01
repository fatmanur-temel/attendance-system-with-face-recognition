import datetime
import psycopg2


class Attendance:
    def __int__(self, conn):
        # Veritabanı bağlantısı
        self.conn = conn

    def create_attendance(self,name):
        # İsimdeki boşluk karakterine göre ayrıştırma
        first_name, last_name, number = name.split(" ")

        # Anlık tarihin alınması
        current_date = datetime.date.today()

        # Veritabanı bağlantısını oluşturun
        cursor = self.conn.cursor()

        # Katılım kaydının var olup olmadığını kontrol etme
        cursor.execute("SELECT * FROM ders1 WHERE date = %s AND student_no = %s",
                   (current_date, number))
        existing_attendance = cursor.fetchone()

        if existing_attendance:
            return
        else:
            # Veritabanına katılım kaydının eklenmesi
            cursor.execute("INSERT INTO ders1 (student_no, date, student_name, student_surname) VALUES (%s, %s, %s, %s)",
                        (number, current_date, first_name, last_name))

            # Veritabanı işlemlerinin kaydedilmesi
            self.conn.commit()

            print("Attendance created for:", name)

        # Veritabanı bağlantısının kapatılması
        cursor.close()
