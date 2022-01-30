# Affiliate_Scrapper

<h4>Environment Setup</h4>
<ol>
	<li>Install python 3</li>
	<li>Install pip (For Mac)</li>
		Download pip by running the following command:<br/>
		>> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	<li>Install the downloaded package by running:<br/>
	>> python3 get-pip.py</li>
	<li>Install virtualenv <br/>
 	>> python3 -m pip install virtualenv</li>
	<li>Create a folder with your project name and run the command (Use windows command prompt)<br/>
	>> virtualenv venv</li>
	<li>Extract project zip file to project folder</li>
	<li>Enable project's virtual env<br/>
	>> source venv/bin/activate</li>
	<li>Install requirements<br/>
	>> python3 -m pip install -r requirements.txt</li>
	<li>Create database<br/>
	>> python3 manage.py makemigrations<br/>
	>> python3 manage.py migrate</li>
	<li>Create a superuser<br/>
	>> python manage.py createsuperuser<br/>
	[Enter name, email(optional) and password as you wish. this will need for admin panel]</li>
</ol>

<h4>Change Project Name</h4>
<ol>
	<li>Activate env<br/>
	>> source venv/bin/activate<br/>
	>> python3 manage.py rename [new_name]</li>
</ol>

<h4>Running application</h4>
<ol>
	<li>Activate env<br/>
	>> source venv/bin/activate</li>
	<li>Run the development server<br/>
	>> python manage.py runserver</li>
	<li>Copy the ip-address from command line (example: http://127.0.0.1:8000/) and paste on your browser</li>
</ol>
