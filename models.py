"""
 Xena - Smart city solutions.

 title          : models.py
 description    : Defines the models for Xena.
 author         : Surya Saini
 email          : sainisurya.1@gmail.com
 created_at     : 2019-06-20
 """


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
    BOOLEAN,
    BigInteger
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import and_, or_
from sqlalchemy.sql.expression import true
from sqlalchemy.ext.declarative import declarative_base

# Define engine, session to interact with postgresql db
engine = create_engine("postgresql+psycopg2://surya:stein@localhost/conduent")
Base = declarative_base()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

# Define model structure for the application
class User(Base):
    """ User model to store basic User info.
    """

    __tablename__ = 'user'
    
    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )
    username = Column(
        'username',
        String(255),
        unique=True,
        nullable=False
    )
    user_detail = relationship(
        'UserDetail',
        back_populates='user',
        lazy=True,
        uselist=False
    )
    user_wallet = relationship(
        'UserWallet',
        back_populates='user',
        lazy=True,
        uselist=False
    )
    user_post = relationship(
        'Post',
        back_populates='user',
        lazy=True,
        uselist=False
    )
    user_comment = relationship(
        'Comment',
        back_populates='user',
        lazy=True,
        uselist=False
    )
    email = Column(
        'email',
        String(255),
        unique=True,
        nullable=False
    )
    private_key = Column(
        'private_key',
        String(512),
        unique=True,
        nullable=False
    )
    public_key = Column(
        'public_key',
        String(512),
        unique=True,
        nullable=False
    )

    # define methods for User Class
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class UserDetail(Base):
    """ UserDetail model to store basic user details like name, address,
        contact info etc.
    """
    
    __tablename__ = 'userDetail'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_detail_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )
    user = relationship(
        'User',
        back_populates='user_detail'
    )
    age = Column(
        'age',
        Integer
    )
    first_name = Column(
        'first_name',
        String(255)
    )
    last_name = Column(
        'last_name',
        String(255)
    )
    address = Column(
        'address',
        String(1024)
    )
    contact_num = Column(
        'contact_num',
        BigInteger,
        unique=True
    )

    # define UserDetail model methods
    def __init__(self, **kwargs):
        super(UserDetail, self).__init__(**kwargs)


class UserWallet(Base):
    """ UserWallet model to store SocialScore and Virtual Value.
    """

    __tablename__ = 'userWallet'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_wallet_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )
    user = relationship(
        'User',
        back_populates='user_wallet'
    )
    socail_score = Column(
        'social_score',
        Integer,
        default=0
    )
    virtual_coin = Column(
        'virtual_coin',
        Integer,
        default=False
    )
    virtual_value = Column(
        'virtual_value',
        Integer,
        default=False
    )

    #define UserWallet model methods
    def __init__(self, **kwargs):
        super(UserWallet).__init__(**kwargs)


class Post(Base):
    """ Post Model to store user created post.
    """

    __tablename__ = 'post'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_post_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )
    user = relationship(
        'User',
        back_populates='user_post'
    )
    post_comment = relationship(
        'Comment',
        back_populates='post',
        lazy=True,
        uselist=False
    )
    title = Column(
        'title',
        String(255),
        nullable=False
    )
    image = Column(
        'image',
        String(255)
    )
    content = Column(
        'content',
        String(512)
    )
    upvote = Column(
        'upvote',
        Integer
    )
    posted_on = Column(
        'posted_on',
        DateTime()
    )

    # define Post model methods
    def __init__(self, **kwargs):
        super(Post).__init__(**kwargs)


class Comment(Base):
    """ Comment model to store comments on a post.
    """

    __tablename__ = 'comment'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )
    parent_id = Column(
        'parent_id',
        Integer,
        nullable=False,
        default=0
    )
    post_comment_id = Column(
        Integer,
        ForeignKey('post.id'),
        nullable=False
    )
    post = relationship(
        'Post',
        back_populates='post_comment'
    )
    user_comment_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )
    user = relationship(
        'User',
        back_populates='user_comment'
    )
    content = Column(
        'content',
        String(255),
        nullable=False
    )

    # define methods for Comment model
    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)


class Utility(Base):
    """ Utility model to store utility(shop) details.
    """

    __tablename__ = 'utility'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name = Column(
        'name',
        String(255),
        nullable=False
    )
    description = Column(
        'description',
        String(512),
        nullable=False
    )
    utility_item = relationship(
        'Utility',
        back_populates='utility',
        lazy=True,
        uselist=False
    )
    address = Column(
        'address',
        String(512),
        nullable=False
    )
    registered = Column(
        'registered',
        BOOLEAN(),
        default=False
    )

    # define methods for Utility model
    def __init__(self, **kwargs):
        super(Utility, self).__init__(**kwargs)


class UtilityItem(Base):
    """ UtilityItem model to store the items on sale by the
        utility.
    """
    
    __tablename__ = 'utilityItem'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )
    utility_item_id = Column(
        Integer,
        ForeignKey('utility.id'),
        nullable=False
    )
    utility = relationship(
        'Utility',
        back_populates='utility_item'
    )
    name = Column(
        'name',
        String(255)
    )
    description = Column(
        'description',
        String(512)
    )
    price = Column(
        'price',
        Integer
    )

    # define methods for Utility model
    def __init__(self, **kwargs):
        super(UtilityItem, self).__init__(**kwargs)
