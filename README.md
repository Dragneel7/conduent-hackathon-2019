# Condent Blockchain Hackathonn 2019

This application was built as a part of the 36hrs conitnous hackathon hosted by Conduent.

## Xena - Smart City Solutions

Xena is social platform that incentivises people to work for the betterment of society and improve their social behaviuor as a whole.

This is done by exploiting the most basic of human tendency, i.e. the sensation each one of use gets when we are appreciated. Xena not only appreciates the user for their good social behaviour, but also awards them with virtual currency which they can then redeem at various shops(Utilities) registered with Xena.

## Xena Users :

There are 3 types of role a user can experience with Xena platfrom.

1. Post User: A user who has the access to post about his/her work/ideology to the common platform and upote/downvote the posts.
2. Utiltity Owners: A user can register his/her own utility/shop, add items for sale and exchanges in the subsidised user environment.
3. Miners: They are the users who support the economy of Xena. Each transaction between a user and a utility is verified by the miners by solving puzzles and adding the transaction to the blockchain.

## Structure for the application
The application is divided into 2 part :

1. Xena : The side of the application where users can post and interact with one another and with the utilities.
2. Xena Blockchain : This is miner panel where users can log into using the Xena credentials and validate(mine) transaction blocks.

## Deployment

### Setup Postgresql Database

Create 2 databased with the names a conduent and conduent_blockchain.

To see how to create a database in postgres visit the following [link](https://www.linode.com/docs/databases/postgresql/how-to-install-postgresql-on-ubuntu-16-04/)

### Export your Database user credentials as env variables

* export DB_OWNER=<DATABASE_OWNER>
* export DB_PASSWORD=<DATABASE_PASSWORD>

### Docker based deployement

To install docker on an Ubuntu machine, visit the following [link](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)

* clone the code repository

    `git clone https://github.com/Dragneel7/conduent-hackathon-2019.git`

* change directory to xena and build the image

    `cd conduent-hackathon-2019/xena`

    `docker build -t xena:latest .`

* deploy the docker container

    `docker run -d -p 5000:5000 xena`

* change directory to xena_blockchain
    
    `cd conduent-hackathon-2019/xena_blockchain`

* build and deploy the Dockerfile
 
    `docker build -t xena_blockchain:latest .`

    `docker run -d -p 7000:7000 xena_blockchain`

### Manual deployement

* clone the code repository

    `git clone https://github.com/Dragneel7/conduent-hackathon-2019.git`

* change directory to xena and install the required dependncies

    `cd conduent-hackathon-2019/xena`

    `pip3 install -r requirements.txt`

* run xena and xena_blockchain server

    `python3 views.py`

    `cd conduent-hackathon-2019/xena_blockchain`

    `python3 views.py`

visit the url to log in and be a part of xena: [xena](http://localhost:5000) and [xena_blockchain](http://localhost:7000)


## Technology and Techstack used

* Flask
* Blockchain
* Docker

This is an open source project, reviews and pull requests would be highly appreciated.