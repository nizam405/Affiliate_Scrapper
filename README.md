# Affiliate_Scrapper
Environment Setup
Install python 3
Install pip (For Mac)
Download pip by running the following command:
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
Install the downloaded package by running:
python3 get-pip.py
Install virtualenv 
 >> python3 -m pip install virtualenv
Create a folder with your project name and run the command (Use windows command prompt)
>> virtualenv venv
Extract project zip file to project folder
Enable project's virtual env
>> source venv/bin/activate
Install requirements
>> python3 -m pip install -r requirements.txt
Create database
>> python3 manage.py makemigrations
>> python3 manage.py migrate
Create a superuser
>> python manage.py createsuperuser
[Enter name, email(optional) and password as you wish. this will need for admin panel]

Change Project Name
Activate env
>> source venv/bin/activate
Run command
		>> python3 manage.py rename [new_name]

Running application
Activate env
>> source venv/bin/activate
Run the development server
>> python manage.py runserver
Copy the ip-address from command line (example: http://127.0.0.1:8000/) and paste on your browser

#########
# Programming language used to make this project:
Python - for scraping (with Django framework - for UI)
HTML - for UI
Bootstrap - for UI
Javascript - for UI
# Database - sqlite 3
# Scrapper module located on [project_name]/post/scrapper.py
