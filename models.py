"""
 Xena - Smart city solutions.

 title          : models.py
 description    : Defines the models for Xena.
 author         : Surya Saini
 email          : sainisurya.1@gmail.com
 created_at     : 2019-06-20
 """

import os
import json

# import functions from sqlalchemy package
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Table,
    Text,
    ForeignKey,
    Date,
    DateTime,
    BOOLEAN
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import and_, or_
from sqlalchemy.sql.expression import true
from sqlalchemy.ext.declarative import declarative_base

# Define engine to interact with postgresql db
engine = create_engine("postgresql+psycopg2://surya:stein@localhost/conduent")