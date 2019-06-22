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

# import modules from sqlalchemy
from sqlalchemy.sql.expression import true

# import application modules
from app import app
from models import (
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


# define User registerations views
@app.route('/register/user/new', methods=['POST'])
def register_user():
    """ Registers a new user to Xena's User model.
    
    :return : Renders the user detail template. 
    """

    if request.method == 'POST':
        data = request.form()  # access form data from request.
        new_user = User(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            private_key='<USERS_PRIVATE_KEY>',
            public_key='<USERS_PUBLIC_KEY>'
        )
        new_user.create()  # create new user in DB.
        context = {}
        context['user'] = new_user
        return render_template('user_details.html', **context)
    
    else:
        return "Method not accessible."


@app.route('/register/user/details', methods=['POST'])
def register_user_details():
    """ Registers a new user details to Xena's UserDetail model.

    :return : Render the common post platform template.
    """

    if request.method == 'POST':
        data = request.form()  # access form data from request.
        user_detail = UserDetail(
            user_detail_id=data['user_id'],
            age=data['age'],
            first_name=data['firstname'],
            last_name=data['lastname'],
            address=data['address'],
            contact_num=data['contact_number']
        )
        user_detail.create()  # add details for the specified user.

        return redirect(
            url_for(
                'app.get_common_post'
            )
        )


# define Common Post's views.
@app.route('/common/posts', methods=['GET'])
def get_common_posts():
    """ Get all Posts from Xena's db.
    """

    posts = Post().get_all()
    context = {}
    context['posts'] = posts
    return render_template('common_post.html', **context)


@app.route('/post/add/<user_id>', methods=['GET'])
def new_post(user_id):
    """ Renders template to add new post.

    :param id: id of the user adding the post.
    :param type: int
    """
    
    user = User().get(user_id)
    context = {}
    context['user'] = user
    return render_template('add_post.html', **context)


@app.route('/post/add/new', methods=['POST'])
def add_new_post():
    """ Adds new post to Xena's db.
    """

    if request.method == 'POST':
        data = request.form()  # access form data from request.
        post = Post(
            user_post_id=data['id'],
            title=data['title'],
            image=data['image'],
            content=data['content']
        )
        post.create()
        return redirect(
            url_for(
                'app.get_common_post'
            )
        )


# define Post Upvote views.
@app.route('/upvote', methods=['POST'])
def upvote_post():
    """ Increase or decrease user post upvote count.
    """

    if request.method == 'POST':
        post_id = request.json['post_id']
        vote_type = request.json['type']
        post = Post().get(post_id)
        if vote_type == 'upvote':
            post.upvote += 1
        elif vote_type == 'downvote':
            post.upvote -= 1
        post.save()
        post_user = post.get_post_user(post_id)
        post_user_wallet = UserWallet().get(post_user.id)
        post_user_wallet.virtual_value = post.upvote
        post_user_wallet.save()  


# define Comment views
@app.route('/add/comment', methods=['POST'])
def add_new_comment():
    """ Adds new comment to a post.
    """

    if request.method == 'POST':
        data = request.form()
        comment = Comment(
            post_comment_id=data['post_id'],
            user_comment_id=data['user_id'],
            content=data['content']
        )
        comment.create()


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

    utility = Utility().get(id)
    context = dict(
        utility=utility
    )
    return render_template('show_utility.html', **context)


@app.route('/add/utility/<user_id>', methods=['GET'])
def new_utility(user_id):
    user = User().get(user_id)
    context = {}
    context['user'] = user
    return render_template('add_utility.html', **context)


@app.route('/add/utility/new', methods=['POST'])
def add_new_utility():
    """ Adds a new utility to Xena's db.
    """
    
    if request.method == 'POST':
        data = request.form()
        new_utility = Utility(
            name=data['name'],
            description=data['description'],
            user_utility_id=data['user_id'],
            address=data['address']
        )
        new_utility.create()
        return redirect(
            url_for(
                'app.get_common_post'
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
@app.route('add/utility-item/<utility_id>', methods=['GET'])
def utility_item(utility_id):
    """ Renders template to add new utility item.

    :param utility_id: id for the requested utility.
    :param type: int
    """

    utility = Utility().get(utility_id)
    context = {}
    context['utility'] = utility
    return render_template('add_utility_item.html', **context)


@app.route('add/utility-item/new', methods=['POST'])
def add_utility_item():
    """ Add new utility item for the utility.
    """

    if request.method == 'POST':
        data = request.form()
        utility_item = UtilityItem(
            utility_item_id=data['utility_id'],
            name=data['name'],
            description=data['description'],
            image=data['image'],
            price=data['price']
        )
        utility_item.create()

        return redirect(
            url_for(
                'app.get_utility',
                utility_id=data['utility_id']
            )
        )


# defines views to buy utility Item
@app.route('/buy_utility_item/<utility_id>/<item_id>/<user_id>', methods=['GET'])
def buy_utility_item(utility_id, item_id, user_id):
    """ Buys the utility item for the user.
    
    :param utility_id: Id of the utility owning the item.
    :param type: int
    :param item_id: Id of the item requested by the user.
    :param type: int
    :param user_id: Id of the logged in user.
    :param type: int
    """

    user_item_rel = UtilityItemUser(
        user_id='user_id',
        utility_id='utility_id',
        utility_item_id='utility_item_id'
    )
    user_item_rel.create()
    user_wallet = UserWallet().get(user_id)
    utility_item = UtilityItem.get(item_id)
    user_wallet.virtual_value -= utility_item.price
    user_wallet.save()
    return redirect(
            url_for(
                'app.get_utility',
                utility_id=request.json['utility_id']
            )
        )


# defines view to allow Utility owner see sold utility
@app.route('/user/utility/<user_id>', methods=['GET'])
def get_user_owned_utility(user_id):
    """ Returns User owned Utilities
    """

    utilities = Utility().get_user_utility(user_id)
    context = dict(
        utilities=utilities
    )
    return render_template('owned_utilities.html', **context)


@app.route('/utility/sold/<utility_id>', methods=['GET'])
def get_utility_item_sold_info(utility_id):
    """ Returns the information of the items sold by the utility.
    """

    items_sold = UtilityItemUser.get_for_utility(utility_id)
    context = dict(
        items=items_sold
    )
    return render_template('utility_items_sold.html', **context)