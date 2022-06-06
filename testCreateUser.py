import requests

url = 'http://127.0.0.1:8000/user'


class User:
    def __init__(self, username, password, fullname, gender,
                 address, mobile, identityNumber, role, floor, room):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.gender = gender
        self.address = address
        self.mobile = mobile
        self.identityNumber = identityNumber
        self.role = role
        self.floor = floor
        self.room = room

    def as_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "fullname": self.fullname,
            "gender": self.gender,
            "address": self.address,
            "mobile": self.mobile,
            "identityNumber": self.identityNumber,
            "role": self.role,
            "floor": self.floor,
            "room": self.room
        }


my_user = User(username="namnhi", password="blackpink", fullname="Ong Nguyen Uyen Nhi",
               gender="Nữ", address="Đà Nẵng", mobile="0596548526",
               identityNumber="162358641", role="user", floor=2, room="p202")

x = requests.post(url, json=my_user.as_dict())
print(x.status_code)
