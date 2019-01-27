# Udacity Project - Linux Server Configuration
This project is about taking a Linux instance from scratch and building it progressively with required system configurations and softwares. At the end of the project, the instance will be available for hosting web applications securely. The project uses Amazon Lightsale for creating and setting up the instance.

## List of installed softwares:
1. apache2
2. finger
3. git
4. postgresql
5. python2
6. flask
7 ssh-keygen

## Steps followed to setup the instance
1. Follow the steps in Udacity to create Amazon lightsale account for Ubuntu
	`Summary of the instance created:
	Instance: Ubuntu-Infy-Bangalore@52.66.206.172`	
2. From the local system ssh from VM to the remote machine
    `ssh -i LightsailDefaultKey-ap-south-1.pem ubuntu@52.66.206.172`
3. install apache
     `sudo apt-get install apache2`
4. http://52.66.206.172/ and check the apache2 home page
5. update all softwares
     `sudo apt-get update`
6. Remove not required softwares 
     `sudo apt-get autoremove`
7. Install finger software which is useful for creating users 
     `sudo apt-get install finger`
8. Create a new user grader
     `sudo adduser grader`
9. Open the below file for setting the grader `sudo` access
     `sudo vi /etc/sudoers.d/grader`
10. Installing PostgreSQL in the instance
	 `sudo apt-get install postgresql postgresql-contrib`
11. Connect to postgres:
	 `sudo -i -u postgres`
12. Created a new role:`createuser --interactive`
13. Create catalog database for new user catalog:
14. createdb catalog
	And set a password for the catalog role:
15. psql
	\password catalog
16. Install git
	`sudo apt-get install git-all`
17. Clone the latest ItemCatalog project from git to /home/grader/ItemCatalogApp directory in Ubuntu instance
	  `git clone https://github.com/VeenaBBhat/ItemCatalogApp.git`
18. Install required modules and softwares to run Python programs
19. Change the database URL to PostgreSQL in database_setup.py
	  `postgresql://catalog:catalog@localhost/catalog`

## Change the port to 2200
Edit the file `/etc/ssh/sshd_config` and `Port 22` to 2200

## Secure server
1. On local machine use `ssh-keygen`
2. Choose the default option to select file name
3. Copy the key information to `grader` user's .ssh/authorized_keys
4. Set the below privileges:
   chmod 700 .ssh
   chmod 644 .ssh/authorized_keys
5. Port configurations:
   sudo ufw allow 2200/tcp
   sudo ufw allow www
   sudo ufw allow ntp

## Keep the softwares up to date
`apt-get update`
`apt-get upgrade`

## Change timezone 
sudo timedatectl set-timezone UTC

## Deploy the ItemCatalogApp as WSGI application
[`https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps`] Digital Ocean tutorial on how to deploy a Flask app on an Ubuntu VPS
1. Create a file structure of catalog under /var/www/catalog
2. Rename `catalog_items.py` to `__init__.py`
3. Create a file `catalog.wsgi` with below content
`#!/usr/bin/python
import os
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/catalog/")

from catalog import app as application
application.secret_key = os.environ.get("SECRET_KEY")`

3. Follow the steps in the above link to create a virtual host
4. Content of /etc/apache2/sites-available/catalog.conf
`<VirtualHost *:80>
        ServerName 52.66.206.172
        ServerAdmin admin@52.66.206.172
        WSGIScriptAlias / /var/www/catalog/catalog.wsgi
        <Directory /var/www/catalog/catalog/>
                Order allow,deny
                Allow from all
        </Directory>
        Alias /static /var/www/catalog/catalog/static
        <Directory /var/www/catalog/catalog/static/>
                 Order allow,deny
                Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>`

5. Disable the default virtual host
`sudo a2dissite 000-default.conf`

6. Enable the new virtual host 
`sudo a2ensite catalog.conf`

7. Restart Apache2
`sudo service apache2 restart`

8. Run your init.py
`python __init__.py`

10. Restart Apache
`sudo service apache2 restart`
