import random
from app import app
from app.lib import common


class UserCheck():

    def password_encrypt(self, email, password):
        md5_once = common.md5_encrypt(str(password) + app.config['SECRET_KEY'])
        md5_sec = common.md5_encrypt(md5_once + email)
        return md5_sec

    def forgetstring_encrypt(self, email):
        md5_once = common.md5_encrypt(
            str(email) + str(random.randrange(1000000, 999999999)))
        md5_sec = common.md5_encrypt(md5_once + app.config['SECRET_KEY'])
        return md5_sec
