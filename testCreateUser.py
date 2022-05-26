import requests
import base64

url = 'http://127.0.0.1:8000/user'


class User:
    def __init__(self, username, password, fullname, gender,
                 address, mobile, indentityNumber, role):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.gender = gender
        self.address = address
        self.mobile = mobile
        self.indentityNumber = indentityNumber
        self.role = role
        self.image = []

    def add_image(self, image_path: str):
        img = open(image_path, "rb")
        img = img.read()
        img = base64.b64encode(img)
        img = img.decode("ascii")
        self.image.append(img)

    def as_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "fullname": self.fullname,
            "gender": self.gender,
            "address": self.address,
            "mobile": self.mobile,
            "indentityNumber": self.indentityNumber,
            "role": self.role,
            "image": self.image
        }


myobj = User()

x = requests.post(url, json=myobj)
response = x.json()
print(response)
