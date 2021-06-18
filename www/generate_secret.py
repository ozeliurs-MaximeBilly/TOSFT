from base64 import b64encode
from os import urandom

random_bytes = urandom(64)
token = b64encode(random_bytes).decode('utf-8')

on = input("Do you want to update the .env file (Warning: You will lose access to the previous secret key) Y/[N]: ")

if on.upper() == "Y":
	with open(".env", "w", encoding="utf8") as env:
		env.write("SECRET_KEY="+token)
	print("The .env file have been updated. Your new token is : " + token)

else:
	print("The .env file have not been updated.")

input("Press a key to continue ...")