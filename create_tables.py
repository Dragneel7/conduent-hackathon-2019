"""
Xena - Smart city solutions.

title          : create_tables.py
description    : Creates table schema for Xena.
author         : Surya Saini
email          : sainisurya.1@gmail.com
created_at     : 2019-06-22
"""

from models import *


# drop existing models.
Base.metadata.drop_all(engine)
# create new models.
Base.metadata.create_all(engine)