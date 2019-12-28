# Flask-Server-for-PugBot

A simple flask server for use with PugBot-for-Discord

## Installation

### Pre-Requisites
1) An Amamzon EC2 (or similar instance) with a static IP to host the bot, database, and server (this README assumes you have an EC2 instance and may need to be tweaked to work with your system, if that is not the case)
    1) If you do not already have this and need to set one up, follow these tutorials:
        1) [https://aws.amazon.com/ec2/getting-started/]
        2) [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-launch-instance]
    2) Make sure you have a static IP
        1) [https://aws.amazon.com/premiumsupport/knowledge-center/ec2-associate-static-public-ip/]
    
2) For Security we will use ngninx

    #### How To Install and Configure nginx
    
    1) Install
        ```
        sudo apt-get update
        sudo apt-get install nginx
        ```

        Once installed, you should be able to go to your public IP and see the nginx welcome page. Similar to the example below:

        ![nginx Welcome Screen](https://www.nginx.com/wp-content/uploads/2014/01/welcome-screen-e1450116630667.png)

    2) Remove the default page by deleting the default file.
        ```
        sudo rm /etc/nginx/sites-enabled/default
        ```

    3) Create a new config file in the sites-available folder.
        ```
        sudo vim /etc/nginx/sites-available/pugbot.com
        ```
    
        This is how the config file should look:    
            
            server {
                listen 80;
            
                location / {
                    proxy_pass http://127.0.0.1:8000/;
                }
            }            
        
        This config file will tell the nginx server to listen on port 80 and pass all requests with the ‘/’ prefix to the server http://127.0.0.1:8000/
    
    5) Create a symbolic link from the sites-enabled directory that points to the pugbot.com config file we created.
        ```
        sudo ln -s /etc/nginx/sites-available/pugbot.com /etc/nginx/sites-enabled/pugbot.com
        ```
        
    6) Restart the nginx web server in order for our changes to take into effect.
        ```
        sudo service nginx restart
        ```

3) A MongoDB with tables setup for PugBot-for-Discord

    #### How To Install and Configure the MongoDB
    
    1) Get the most recent stable version onto our instance: 
        1) Import the public key used by the package management system    
    ```sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5```
    
        2) Create a list file for MongoDB (Ubuntu 16.04)    
    ```echo “deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse” | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list```
    
        3)  Reload local package database  
    ```sudo apt-get update```
    
        4) Install the MongoDB packages    
    ```sudo apt-get install -y mongodb-org```
    
    2) Start the MongoDB
        1) Issue the start command        
        ```sudo service mongod start```
        
        2) Verify the MongoDB started correctly        
        ```cat /var/log/mongodb/mongod.log``` 
            - ensure you see `[initandlisten] waiting for connection on port 27017` at the end
    3) Leave the database running ***without*** access control!!
    4) Setup the database and required collections
        1) Connect to the MongoDB instance we just started          
        `mongo`
        
        2) Create the database we will be using        
        `use Game`
        
        3) Create the necessary collections
            ```
            db.banned.insertOne( { 'userid': '123456789987654321', 'length': '2 days', 'origin': 0123456789.8765432, 'reason': 'initial setup' } );        
            db.maps.insertOne( { 'name': 'map1', 'aliases': ['alias0','alias1','alias2'] } );
            db.pickups.insertOne( { 'blueteam': ['player0','player1','player2','player3'], 'last':true, 'map': 'A New Begining', 'redteam': ['player4','player5','player6','player7'], 'time': 81955354150 } );
            db.servers.insertOne( { 'names': ['server0', 'srvr0'], 'passwd': 'secret', 'serverid': '127.0.0.1:27015' } );        
            ``` 
                
### Running the Server

1) Unpack to `/home/ubuntu/Flask`
2) Run the bot using the provided shell script
    ```
    cd /home/ubuntu/Flask
    ./runServer.sh
    ```
  
## Requirements

- flask [https://github.com/pallets/flask]
- flask_pymongo [https://github.com/dcrosta/flask-pymongo]
- wtforms [https://github.com/wtforms/wtforms/]

## Resources
- [https://github.com/ccdtzccdtz/Deploy-Flask-App-on-AWS-EC2-Instance]
- [https://hackernoon.com/how-to-install-and-secure-mongodb-in-amazon-ec2-in-minutes-90184283b0a1]
