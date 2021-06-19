from dotenv import load_dotenv
from datetime import date, timedelta
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
print(date.today().isoformat().replace("-","/"))
print(SECRET_KEY)