import random
from app import app
from app.lib.common import CommonClass

class UserCheck(CommonClass):
    def password_encrypt(self,email,password):
        md5_once = CommonClass.md5_encrypt(self,str(password)+app.config['SECRET_KEY'])
        md5_sec = CommonClass.md5_encrypt(self,md5_once+email)
        return md5_sec

    def forgetstring_encrypt(self,email):
        md5_once = CommonClass.md5_encrypt(self,str(email)+str(random.randrange(1000000, 999999999)))
        md5_sec = CommonClass.md5_encrypt(self,md5_once + app.config['SECRET_KEY'])
        return md5_sec