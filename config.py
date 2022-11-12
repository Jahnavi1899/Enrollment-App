import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b"\x1fU\x8b0\x9fTLk0\x1d\xa4\x84'*\x90<" #to make sure the data sent is not hacked or altered
    MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment' }