import requests
import base64

url = 'http://127.0.0.1:8000/user/save_image'


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.image = []

    def add_image(self, image_path: str):
        img = open(image_path, "rb")
        img = img.read()
        img = base64.b64encode(img)
        img = img.decode("ascii")
        self.image.append(img)

    def as_dict(self):
        return {
            "user_id": self.user_id,
            "image": self.image
        }


base_dir = "../FaceRecognition/Dataset/People/"

my_user = User("628f83024d02afad275af03f")

my_user.add_image(base_dir + "NamNhi/image.jpg")
my_user.add_image(base_dir + "NamNhi/IMG_3296.JPG")
my_user.add_image(base_dir + "NamNhi/IMG_3301.JPG")
my_user.add_image(base_dir + "NamNhi/IMG_3315.JPG")
my_user.add_image(base_dir + "NamNhi/IMG_3316.JPG")

x = requests.post(url, json=my_user.as_dict())
print(x.status_code)
