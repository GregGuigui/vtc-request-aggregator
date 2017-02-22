import os
from flask import Flask

app = Flask(__name__)

env = os.getenv('ENV', 'dev')

import routes
import db
import middlewares.auth