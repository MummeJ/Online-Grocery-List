# Online Grocery List

## ==Description== ##
This online grocery list keeps track of each user's grocery list which can be modified by only the signed in user. You will be prompted to create an account if you do not already have one. Only the admin account is able to view other user's grocery lists.

### ==Files and directories== ###
   - `static` - Contains all static files.
      - `css` - Contains main.css
   - `template` - Contains all html files for the app.
      - `base.html` - The base template that all other templates extend.
         - `index.html` - Main template or "homepage".
         - `login.html` - Page where users and login to their account.
         - `signup.html` - Page where users can create account.
         - `update.html` - Page where users can update their grocery list items.
         - `user-items.html` - Page where users can view/add/delete grocery list items.
      - `app.py` - File that creates an instance of Flask app.
      - `forms.py` - Contains all the forms.

### ==Executing Program== ###
To run, set the following environment variables:
* Powershell
	* `$env:FLASK_APP = "app"`
	* `$env:FLASK_ENV = "development"`
	* `flask run`
* CMD
	* `set FLASK_APP=app`
	* `set FLASK_ENV=development`
	* `flask run`
* Bash
	* `export FLASK_APP=app`
	* `export FLASK_ENV=development`
	* `flask run`
