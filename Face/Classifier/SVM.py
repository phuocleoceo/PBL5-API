from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from os.path import join, curdir
from sklearn.svm import SVC
import joblib
import json


class SVM:
    def __init__(self):
        self.classifier_path = join(curdir, "Face/SVM_Model", "svm.sav")
        # Load database chứa các vector đặc trưng
        db_path = join(curdir, "Face/Database", "Database.json")
        with open(db_path, "r") as db:
            self.database = json.load(db)

    def load_model(self):
        """
        Hàm load SVM model để sử dụng khi nhận dạng gương mặt
        """
        with open(self.classifier_path, "rb") as f:
            model = joblib.load(f)
        return model

    def split_data(self, test_size=0.2):
        """
        Hàm chia data thành train và test, đảm bảo số lượng công bằng giữa mỗi gương mặt
        test_size : kích thước tập test
        """
        # X chứa vector đặc trưng, Y chứa nhãn gương mặt
        X_train, X_test, Y_train, Y_test = [], [], [], []
        # Vào database để lấy các vector gương mặt
        for label, embedding in self.database.items():
            # Chia thành 2 tập train, test
            ebd_train, ebd_test = train_test_split(embedding, test_size=test_size)
            for ebdt in ebd_train:
                X_train.append(ebdt)
                Y_train.append(label)
            for ebdt in ebd_test:
                X_test.append(ebdt)
                Y_test.append(label)
        return X_train, X_test, Y_train, Y_test

    def train(self):
        """
        Hàm train model SVM
        """
        X_train, X_test, Y_train, Y_test = self.split_data(test_size=0.2)

        # SVC classifier
        model = SVC(kernel="linear", probability=True)

        # Fit model
        # Từ 1 embd ta dự đoán ra label tương ứng
        model.fit(X_train, Y_train)

        # Lưu lại model đẻ sử dụng sau này
        with open(self.classifier_path, "wb") as f:
            joblib.dump(model, f)

        # Đánh giá kết quả
        Y_train_pred = model.predict(X_train)
        Y_test_pred = model.predict(X_test)
        # Độ chính xác
        Y_train_accuracy = accuracy_score(Y_train, Y_train_pred)*100
        Y_test_accuracy = accuracy_score(Y_test, Y_test_pred)*100

        return Y_train_accuracy, Y_test_accuracy
