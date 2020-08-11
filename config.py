import os

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(base_dir, "instance")
load_dotenv(os.path.join(base_dir, ".env"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
    ADMINS = ["christophpryer@gmail.com"]
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
