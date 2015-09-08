import hashlib

class CommonClass:
    def md5_encrypt(self,string):
        md5 = hashlib.md5()
        md5.update(str(string))
        return md5.hexdigest()