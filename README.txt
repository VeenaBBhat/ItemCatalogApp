# Udacity Project - Linux Server Configuration
This project is about taking a Linux instance from scratch and building it progressively with required system configurations and softwares. At the end of the project, the instance will be available for hosting web applications securely. The project uses Amazon Lightsale for creating and setting up the instance.

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
17. Clone the latest ItemCatalog project to git
	  `git clone https://github.com/VeenaBBhat/ItemCatalogApp.git`
18. Install required modules and softwares to run Python programs
19. Change the database URL to PostgreSQL in database_setup.py
	  `postgresql://catalog:catalog@localhost/catalog`

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


    

