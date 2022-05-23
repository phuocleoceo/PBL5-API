from Face.Inference.FaceRecognition import FaceRecognition
from Face.Inference.FaceDetection import FaceDetection
from scipy.spatial import distance
from os.path import join, curdir
from Face.Classifier.SVM import SVM
import json


class Facenet:
    def __init__(self):
        self.detector = FaceDetection()
        self.recognizer = FaceRecognition()
        self.classifier = SVM()
        # Load database chứa các vector đặc trưng
        db_path = join(curdir, "Face/Database", "Database.json")
        with open(db_path, "r") as db:
            self.database = json.load(db)

    def Euclidean_Distance(self, embd_db, embd_recog):
        """
        Hàm tính khoảng cách Euclidean giữa 2 vector
        embd_db : vector khuôn mặt đang được lưu trong database
        embd_recog : vector khuôn mặt đang nhận dạng
        """
        # return np.sqrt(np.sum((embd_db-embd_recog)**2))
        return distance.euclidean(embd_db, embd_recog)

    def Get_People_Identity_SVM(self, image, resize=True, scale=4):
        """
        Hàm trả về tên khuôn mặt sử dụng SVM
        image : ảnh
        resize : có giảm kích thước ảnh hay không nhằm tăng tốc độ xử lý
        scale : tỉ lệ giảm kích thước ảnh
        """
        svm = self.classifier.load_model()
        # Detect hình chữ nhật bao quanh khuôn mặt
        rec = self.detector.Detect_Face(image, resize, scale)
        # Ma trận gương mặt được detect
        face_crop = self.detector.Crop_Face(image, rec)

        # Nhận diện nhiều gương mặt cho chắc
        identity = []
        for face in face_crop:
            # Trích xuất đặc trưng
            face_embd = self.recognizer.Get_Face_Embedding(face)
            # Nhận dạng
            person_name = svm.predict(face_embd)[0]
            # Truy cập vào lại database để lấy ra khoảng cách
            distance = min([self.Euclidean_Distance(ed, face_embd) for ed in self.database[person_name]])
            if distance > 1:
                person_name = "UNKNOWN"
            identity.append((person_name, distance))
        return identity
