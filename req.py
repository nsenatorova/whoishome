import requests
import flask_unittest


class TestProject(flask_unittest.ClientTestCase):


    app = Flask(__name__)


    def test_registration(self):
        r = requests.post('http://lemonl1me.pythonanywhere.com/register',
                          json={"id": 1, "email": "n-senat@mail.ru", "password": "password",
                                "fcm_token": "dvdvnvndn2133urhav"})

        assert r.status_code == 201
        new = requests.post('http://lemonl1me.pythonanywhere.com/register',
                            json={"id": 1, "email": "n-senat@mail.ru", "password": "JOPAjopa",
                                 "fcm_token": "dvdvnvndn2133urhav"})
        assert r.status_code == 400


    def test_login(self):
        r = requests.post('http://lemonl1me.pythonanywhere.com/login',
                      json={"id": 1, "email": "n-senat@mail.ru", "password": "password",
                            "fcm_token": "dvdvnvndn2133urhav"})

        assert r.status_code == 201
        r = requests.post('http://lemonl1me.pythonanywhere.com/login',
                      json={"id": 1, "email": "n-senat@mail.ru", "password": "wrong_password",
                            "fcm_token": "dvdvnvndn2133urhav"})
        assert r.status_code == 400
        r = requests.post('http://lemonl1me.pythonanywhere.com/login',
                      json={"id": 2, "email": "iot-project@mail.ru", "password": "qwerty",
                            "fcm_token": "kgshlgh;gsghhkdgh"})

        assert r.status_code == 400


    def test_update(self):
        r = requests.put('http://lemonl1me.pythonanywhere.com/update/n-senat@mail.ru',
                     json={"id": 1, "email": "iot-project@mail.ru", "password": "password",
                           "is_in_home": 1})

        assert r.status_code == 201
        r = requests.put('http://lemonl1me.pythonanywhere.com/update/iot-project@mail.ru',
                     json={"id": 1, "email": "n-senat@mail.ru", "password": "new_password",
                           "is_in_home": 1})
        assert r.status_code == 201
        r = requests.put('http://lemonl1me.pythonanywhere.com/update/iot-project@mail.ru',
                     json={"id": 1, "email": "blin@mail.ru", "password": "blinskiy",
                           "fcm_token": "dvdvnvndn2133urhav"})

        assert r.status_code == 404



    def test_invite(self):
        r = requests.post('http://lemonl1me.pythonanywhere.com/invite/iot-project@mail.ru',
                      json={"email": "newuser@mail.ru"})

        assert r.status_code == 201
        r = requests.post('http://lemonl1me.pythonanywhere.com/invite/iot-project@mail.ru',
                      json={"email": "khodosov2000@gmail.com"})
        assert r.status_code == 400



    def test_notification(self):
        r = requests.get('http://lemonl1me.pythonanywhere.com/trigger/777')
        assert r.status_code == 200
