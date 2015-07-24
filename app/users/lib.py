from app import app
import hashlib
class PasswordCheck:
	def md5_encrypt(self,string):
		md5 = hashlib.md5()
		md5.update(str(string))
		return md5.hexdigest()


	def password_encrypt(self,email,password):
		md5_once = self.md5_encrypt(str(password)+app.config['SECRET_KEY'])
		md5_sec = self.md5_encrypt(md5_once+email)
		return md5_sec