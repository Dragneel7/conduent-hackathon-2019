"""
Xena - Smart city solutions.

title          : views.py
description    : Defines the views for Xena.
author         : Surya Saini
email          : sainisurya.1@gmail.com
created_at     : 2019-06-20
"""

# import default packages
import os
import json

#from default modules import package
from datetime import datetime

# import modules from flask
from flask import jsonify, flash
from flask import session as flask_session
from flask import url_for, redirect
from flask import (
    request,
    render_template,
    Response,
    abort,
    jsonify
)

# import modules from flask_socketio
from flask_socketio import send

# import modules from sqlalchemy
from sqlalchemy.sql.expression import true

# import application modules
from app import app, socketio
from models import (
    session,
    User,
    UserDetail,
    UserWallet,
    Post,
    Comment,
    Utility,
    UtilityItem,
    UtilityItemUser
) 


# define views for Xena.
@app.route('/', methods=['GET'])
def home():
    """ Home View page when a user logs in.
    """

    context = {}
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """ Log in a registered user.
    """

    if request.method == "POST":
        data = request.form
        if User().login(data['username'], data['password']):
            return redirect(
                url_for('get_common_posts')
            )
        else:
            return redirect(
                url_for('register')
            )
    else:
        return render_template('login.html')

# define User registerations views
@app.route('/register', methods=['GET'])
def register():
    """  Renders register user template.
    """
    
    return render_template('register.html')


@app.route('/register/user/new', methods=['POST'])
def register_user():
    """ Registers a new user to Xena's User model.
    
    :return : Renders the user detail template. 
    """

    if request.method == 'POST':
        data = request.form  # access form data from request.
        new_user = User(
            username=data['username'],
            password=data['password'],
            email=data['email']
        )
        new_user.create()  # create new user in DB.
        new_user_wallet = UserWallet(
            user_wallet_id=new_user.id,
            socail_score=0,
            virtual_value=0
        )
        new_user_wallet.create()
        context = {}
        context['user'] = new_user
        flask_session['user_id'] = new_user.id
        return render_template('user_details.html', **context)


@app.route('/register/user/details', methods=['POST'])
def register_user_details():
    """ Registers a new user details to Xena's UserDetail model.

    :return : Render the common post platform template.
    """

    if request.method == 'POST':
        data = request.form  # access form data from request.
        user_detail = UserDetail(
            user_detail_id=data['user_id'],
            age=data['age'],
            first_name=data['firstname'],
            last_name=data['lastname'],
            address=data['address'],
            contact_num=data['contact_num']
        )
        user_detail.create()  # add details for the specified user.

        return redirect(
            url_for(
                'get_common_posts'
            )
        )


# define Common Post's views.
@app.route('/common/posts', methods=['GET'])
def get_common_posts():
    """ Get all Posts from Xena's db.
    """

    user_id = flask_session.get('user_id')
    user = User().get(user_id)
    posts = Post().get_all()
    context = {}
    context['posts'] = posts
    context['user'] = user
    return render_template('common_post.html', **context)


@app.route('/post/add', methods=['GET'])
def new_post():
    """ Renders template to add new post.
    """
    
    user_id = flask_session.get('user_id')
    user = User().get(user_id)
    context = {}
    context['user'] = user
    return render_template('add_post.html', **context)


@app.route('/post/add/new', methods=['POST'])
def add_new_post():
    """ Adds new post to Xena's db.
    """

    user_id = flask_session.get('user_id')
    if request.method == 'POST':
        data = request.form  # access form data from request.
        post = Post(
            user_post_id=user_id,
            title=data['title'],
            image=data['image'],
            content=data['content'],
            upvote=0,
            posted_on=datetime.now()
        )
        post.create()
        return redirect(
            url_for(
                'get_common_posts'
            )
        )


# define Post Upvote views.
@socketio.on('message')
def trigger_socket_function(msg_obj):
    """ Triggers the function based on the msg_obj param func_type.

    :param msg_obj: Details of the message and the function to trigger.
    :param type: dict
    :rparam send_obj: Upvote count or comment message.
    :rtype: String
    """

    if(msg_obj['func_type'] == 'vote'):
        send_obj = dict(
            upvote=upvote_post(msg_obj),
            post_id=msg_obj['post_id'],
            func_type=msg_obj['func_type']
        )
    else:
        send_obj = dict(
            comments=add_new_comment(msg_obj),
            post_id=msg_obj['post_id'],
            func_type=msg_obj['func_type']
        )
    send(send_obj, broadcast=True)


def upvote_post(msg_obj):
    """ Increase or decrease user post upvote count.

    :param msg_obj: Details of the post user want to upvote.
    :param type: dict
    """

    post_id = msg_obj['post_id']
    vote_type = msg_obj['type']
    post = Post().get(post_id)
    if vote_type == 'upvote':
        post.upvote += 1
    elif vote_type == 'downvote':
        post.upvote -= 1
    post.save()
    post_user_id = post.get_post_user(post_id)
    post_user_wallet = UserWallet().get(post_user_id)
    post_user_wallet.virtual_value = post.upvote
    post_user_wallet.socail_score = post.upvote
    post_user_wallet.save()
    return post.upvote


# define Comment views
def serialize_comment(comments):
    """ Serialize the comments in JSON format.

    :param comments: list of comments for a post.
    :param type: list
    """
    comment_dict = {}
    i=0
    for comment in comments:
        i += 1
        comment_thread = {}
        comment_thread['content'] = comment.content
        comment_dict['comment' + str(i)] = comment_thread
    return comment_dict


def add_new_comment(msg_obj):
    """ Adds new comment to a post.

    :param msg_obj: Details of the post user want to comment.
    :param type: dict
    """
    comment = Comment(
        post_comment_id=msg_obj['post_id'],
        user_comment_id=msg_obj['user_id'],
        content=msg_obj['comment']
    )
    comment.create()
    comments = Post().get(msg_obj['post_id']).post_comment
    comments = serialize_comment(comments)
    return comments


# define Utility views
@app.route('/utilities', methods=['GET'])
def get_all_utilities():
    """ Returns all the utilities and renders them in utility template.
    """
    
    utilities = Utility().all()
    context = {}
    context['utilities'] = utilities
    return render_template('utilities.html', **context)


@app.route('/utilities/<utility_id>', methods=['GET'])
def get_utility(utility_id):
    """ Returns data for a selected utility.

    :param utility_id: Id for the requested utility.
    :param type: int
    """

    utility = Utility().get(utility_id)
    context = dict(
        utility=utility
    )
    return render_template('show_utility.html', **context)


@app.route('/add/utility', methods=['GET'])
def new_utility():
    """ Render template to add new utility.
    """

    user_id = flask_session.get('user_id')
    user = User().get(user_id)
    context = {}
    context['user'] = user
    return render_template('add_utility.html', **context)


@app.route('/add/utility/new', methods=['POST'])
def add_new_utility():
    """ Adds a new utility to Xena's db.
    """
    
    user_id = flask_session.get('user_id')
    if request.method == 'POST':
        data = request.form
        new_utility = Utility(
            name=data['name'],
            description=data['description'],
            image=data['image'],
            user_utility_id=user_id,
            address=data['address']
        )
        new_utility.create()
        return redirect(
            url_for(
                'get_all_utilities'
            )
        )


@app.route('/register/utility', methods=['POST'])
def register_new_utility():
    """ Register_new_utility.
    """

    if request.method == 'POST':
        utility_id = request.json['utility_id']
        utility = Utility().get(utility_id)
        utility.approval_count += 1
        if utility.approval_count >= 10:
            utility.registered = True
        utility.save()


# define views for UtilityItem
@app.route('/add/utility-item/<utility_id>', methods=['GET'])
def utility_item(utility_id):
    """ Renders template to add new utility item.

    :param utility_id: id for the requested utility.
    :param type: int
    """

    utility = Utility().get(utility_id)
    context = {}
    context['utility'] = utility
    return render_template('add_utility_item.html', **context)


@app.route('/add/utility-item/new', methods=['POST'])
def add_utility_item():
    """ Add new utility item for the utility.
    """

    if request.method == 'POST':
        data = request.form
        utility_item = UtilityItem(
            utility_item_id=data['utility_item_id'],
            name=data['name'],
            description=data['description'],
            image=data['image'],
            price=data['price']
        )
        utility_item.create()

        return redirect(
            url_for(
                'get_utility',
                utility_id=data['utility_item_id']
            )
        )


# defines views to buy utility Item
@app.route('/buy_utility_item/<utility_id>/<item_id>', methods=['GET'])
def buy_utility_item(utility_id, item_id):
    """ Buys the utility item for the user.
    
    :param utility_id: Id of the utility owning the item.
    :param type: int
    :param item_id: Id of the item requested by the user.
    :param type: int
    """

    user_id = flask_session.get('user_id')
    user_item_rel = UtilityItemUser(
        user_id=user_id,
        utility_id=utility_id,
        utility_item_id=item_id,
        transaction_registered="false"
    )
    user_item_rel.create()
    user_wallet = UserWallet().get(user_id)
    utility_item_price = UtilityItem().get_price(item_id)
    user_wallet.virtual_value -= utility_item_price
    user_wallet.save()
    return redirect(
            url_for(
                'get_utility',
                utility_id=utility_id
            )
        )


# defines view to allow Utility owner see sold utility
@app.route('/user/utility', methods=['GET'])
def get_user_owned_utility():
    """ Returns User owned Utilities
    """

    user_id = flask_session.get('user_id')
    utilities = Utility().get_user_utility(user_id)
    context = dict(
        utilities=utilities
    )
    return render_template('owned_utilities.html', **context)


@app.route('/utility/sold/<utility_id>', methods=['GET'])
def get_utility_item_sold_info(utility_id):
    """ Returns the information of the items sold by the utility.
    """

    items_sold = UtilityItemUser().get_for_utility(utility_id)
    context = dict(
        items=items_sold
    )
    return render_template('utility_sold_items.html', **context)


@app.route('/get_unregistered_transactions', methods=['GET'])
def get_unregistered_tran():
    """ Returns all the unregistered transactions to send for mining.
    """
    
    transactions = UtilityItemUser().get_unregistered_transactions()
    transactions_dict = {}
    i = 0
    for transaction in transactions:
        i += 1
        trans = {}
        trans['sender_id'] = transaction.user_id
        trans['transaction_id'] = transaction.id
        reciever_id = Utility().get_owner(transaction.utility_id)
        amount = UtilityItem().get_price(transaction.utility_item_id)
        trans['amount'] = amount
        trans['reciever'] = reciever_id
        transactions_dict['trans' + str(i)] = trans
    return jsonify(transactions_dict)
 

if __name__ == "__main__":
    session.rollback()
    socketio.run(app)