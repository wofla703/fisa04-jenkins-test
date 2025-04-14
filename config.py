import os
from dotenv import load_dotenv

# .env 불러오기
load_dotenv()

myDBid = os.environ.get('DB_USER')
myDBpw = os.environ.get('DB_PASSWORD')
mySecretKey = os.environ.get('SECRET_KEY')
myDB = os.environ.get('DB_HOST')
mySchema = os.environ.get('DB_NAME')

# db를 저장할 폴더/파일이름 
BASE_DIR = os.path.dirname(__file__)

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'test.db'))
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{myDBid}:{myDBpw}@{myDB}:3306/{mySchema}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY= mySecretKey
