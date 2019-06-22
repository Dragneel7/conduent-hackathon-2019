"""
Xena - Smart city solutions.

title          : app.py
description    : Defines the app structure for Xena Blockchain.
author         : Surya Saini
email          : sainisurya.1@gmail.com
created_at     : 2019-06-23
"""

from flask import Flask
from config import Config
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)