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
    password = Column(
        'password',
        String(255),
        unique=False,
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
    user_utility = relationship(
        'Utility'
    )
    email = Column(
        'email',
        String(255),
        unique=True,
        nullable=False
    )

    # define methods for User Class
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def create(self):
        """ Saves new user to the database.
        """
        session.add(self)
        session.commit()

    def get(self, id):
        """ Returns the user data for the specified id.
        
        :param id: id for the request user.
        :param type: int
        """
        return session.query(User).filter(User.id == id).first()

    def login(self, username, password):
        """ Logs in a user.

        :param username: Username for the user to be logged in.
        :param type: String
        :param password: Password for the logged in your.
        :param type: String
        """
        return session.query(User).filter(and_(User.username == username,User.password == password )).first()


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

    def create(self):
        """ Save user details in DB.
        """
        session.add(self)
        session.commit()


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
    virtual_value = Column(
        'virtual_value',
        Integer,
        default=False
    )

    #define UserWallet model methods
    def __init__(self, **kwargs):
        super(UserWallet, self).__init__(**kwargs)
    
    def create(self):
        """ Creates a new user wallet.
        """
        session.add(self)
        session.commit()

    def get(self, id):
        """ Returns user wallet info based on id.
        """
        return session.query(UserWallet).filter(UserWallet.user_wallet_id == id).first()
    
    def save(self):
        """ Saves the updated wallet status.
        """
        session.commit()

    def successful_mine(self, id):
        """ Add virtual value in the user's wallet for successful verification of the
            transaction.
        """
        user_wallet = session.query(UserWallet).filter(UserWallet.user_wallet_id == id).first()
        user_wallet.virtual_value += 10
        session.commit()


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
        'Comment'
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
        super(Post, self).__init__(**kwargs)

    def create(self):
        """ Saves new post to db.
        """
        session.add(self)
        session.commit()

    def get(self, id):
        """ Returns the post data for the specified id.
        
        :param id: id for the requested post.
        :param type: int
        """
        return session.query(Post).filter(Post.id == id).first()

    def save(self):
        """ Saves updated Post.
        """
        session.commit()

    def get_all(self):
        """ Return all posts from db.
        """
        return session.query(Post).all()

    def get_post_user(self, id):
        """ Returns information of the user who authored the post.
        """
        post = session.query(Post).filter(Post.id == id).first()
        return post.user_post_id


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

    def create(self):
        """ Adds a new comment to db.
        """
        session.add(self)
        session.commit()


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
    image = Column(
        'image',
        String(512)
    )
    user_utility_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )
    utility_item = relationship(
        'UtilityItem'
    )
    address = Column(
        'address',
        String(512),
        nullable=False
    )
    approval_count = Column(
        'approval_count',
        Integer,
        default=0
    )
    registered = Column(
        'registered',
        BOOLEAN(),
        default=False
    )

    # define methods for Utility model
    def __init__(self, **kwargs):
        super(Utility, self).__init__(**kwargs)

    def create(self):
        """ Adds new utility to db.
        """
        session.add(self)
        session.commit()
    
    def get(self, id):
        """ Returns the Utility data for the specified id.
        
        :param id: id for the requested Utility.
        :param type: int
        """
        return session.query(Utility).filter(Utility.id == id).first()

    def all(self):
        """ Returns all utilities in db.
        """
        return session.query(Utility).all()
    
    def save(self):
        """ Updates the Utility in db.
        """
        session.commit()

    def get_user_utility(self, id):
        """ Gets user id owned utilities.
        """
        return session.query(Utility).filter(Utility.user_utility_id == id).all()
    
    def get_owner(self, id):
        """ Returns the id for the utility owner.
        """
        owner = session.query(Utility).filter(Utility.id == id).first()
        return owner.id


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
    name = Column(
        'name',
        String(255)
    )
    description = Column(
        'description',
        String(512)
    )
    image = Column(
        'image',
        String(512)
    )
    price = Column(
        'price',
        Integer
    )

    # define methods for Utility model
    def __init__(self, **kwargs):
        super(UtilityItem, self).__init__(**kwargs)

    def create(self):
        """ Saves a new utility item to db.
        """
        session.add(self)
        session.commit()
    
    def get_price(self, id):
        """ Gets the item price.
        """
        item = session.query(UtilityItem).filter(UtilityItem.id == id).first()
        return item.price


class UtilityItemUser(Base):
    """ UtilityItemUser model to store the utility item bought by the user.
    """

    __tablename__ = 'utilityItemUser'

    id =  Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = Column(
        'user_id',
        Integer
    )
    utility_id = Column(
        'utility_id',
        Integer
    )
    utility_item_id = Column(
        'utility_item_id',
        Integer
    )
    transaction_registered = Column(
        'transaction_registered',
        String(255),
        default="false"
    )

    # define methods for Utility model
    def __init__(self, **kwargs):
        super(UtilityItemUser, self).__init__(**kwargs)

    def create(self):
        """ Save new utility item user relation in db.
        """
        session.add(self)
        session.commit()

    def get_for_utility(self, id):
        """ Gets all the users who bought from utility and have registered transactions.
        """
        return session.query(UtilityItemUser).filter(and_(UtilityItemUser.utility_id == id, UtilityItemUser.transaction_registered == "true")).all()

    def get_unregistered_transactions(self):
        """ Returns all the transactions that are unregistered.
        """
        return session.query(UtilityItemUser).filter(UtilityItemUser.transaction_registered == "false").all()

    def register(self, id):
        """ Register the successfully mined transaction.
        """
        transaction = session.query(UtilityItemUser).filter(UtilityItemUser.id == id).first()
        transaction.transaction_registered = "true"
        session.commit()