import cv2
import threading

queue = []
frame_count = 0


def run_camera():
    """
    Bu fonksiyon videoyu okuyup, her 100 frame'de bir queue'ya ekliyor.
    Bunu yüz bulundu olarak düşünebilsin, yüz bulunduğunda isim girmesini isteyeceğimizden hangi frame'de
    yüz bulunduğunu kaydetmek için frame sayısını ve belki gösteririz diye frame'i ekliyoruz.
    Bu sayede, videoyu okuyan ve isim girmeyi bekleyen threadler arasında
    bir senkronizasyon oluyor.
    """
    global frame_count
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if frame is None or not ret:
            break
        frame_count += 1
        if frame_count % 100 == 0:
            queue.append({
                "frame": frame,
                "count": frame_count
                })
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return


if __name__ == '__main__':
    video_thread = threading.Thread(target=run_camera)
    video_thread.start()
    with open("names.txt", "w") as f:
        # Burada main thread, isim girmesini bekleyen thread olacak
        while True:
            if not video_thread.is_alive() and len(queue) == 0:
                # Videodan gelen frame'ler bitti ve queue'da da frame kalmadıysa bitirlecek,
                break
            if len(queue) > 0:
                # Queue'da frame varsa, isim girmesini bekleyen thread'e geçilecek
                frame_dict = queue.pop(0)
                f.write(f"{frame_dict.get('count')}: {input('Enter name: ')}\n")
            else:
                continue
    video_thread.join()
    cv2.destroyAllWindows()