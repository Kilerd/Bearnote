import hashlib
from flask import request
class CommonClass:
    def md5_encrypt(self,string):
        md5 = hashlib.md5()
        md5.update(str(string))
        return md5.hexdigest()



def get_domain():
    url_root = request.url_root[:len(request.url_root)-1]
    if url_root[:4] == 'http':
        return url_root[7:]
    else:
        return url_root[8:]