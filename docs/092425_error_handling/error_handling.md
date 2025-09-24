
---

# Chapter 7: Error Handling

In this chapter, Miguel pauses feature development to address error handling strategies in Flask. He introduces a bug from Chapter 6 (duplicate username) to illustrate the importance of robust error management.

---

## Error Handling in Flask

Flask shows a generic “Internal Server Error” page when a bug occurs. For example, changing a username to one that already exists triggers a `sqlite3.IntegrityError` due to a `UNIQUE` constraint violation.


![Internal server error](https://raw.githubusercontent.com/tunafish304/microblog/refs/heads/main/docs/images/chapter7_photo_1.png)

The terminal shows a stack trace:

```
[2023-04-28 23:59:42,300] ERROR in app: Exception on /edit_profile [POST]
Traceback (most recent call last):
  File "venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1963, in _exec_single_context
	self.dialect.do_execute(
  File "venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 918, in do_execute
	cursor.execute(statement, parameters)
sqlite3.IntegrityError: UNIQUE constraint failed: user.username
```

---

## Debug Mode

Enabling debug mode provides an interactive debugger in the browser.

Set the environment variable:

```
(venv) $ export FLASK_DEBUG=1
```

On Windows:

```
(venv) > set FLASK_DEBUG=1
```

Then run:

```
(venv) $ flask run
 * Serving Flask app 'microblog.py' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 118-204-854
```

Now make the application crash one more time to see the interactive debugger in your browser:

![sqlalchemy.exc.IntegrityError](https://raw.githubusercontent.com/tunafish304/microblog/refs/heads/main/docs/images/chapter7_photo_2.png)
---
The debugger allows you expand each stack frame and see the corresponding source code. You can also open a Python prompt on any of the frames and execute any valid Python expressions, for example to check the values of variables.


## Custom Error Pages

Let's define custom error pages for the HTTP errors 404 and 500, the two most common ones. Defining pages for other errors works in the same way.

Create a new module for error handlers:

```python
# app/errors.py: Custom error handlers
from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500
```

Templates:

```html
<!-- app/templates/404.html: Not found error template -->
{% extends "base.html" %}
{% block content %}
  <h1>File Not Found</h1>
  <p><a href=" url_for('index') ">Back</a></p>
{% endblock %}
```

```html
<!-- app/templates/500.html: Internal server error template -->
{% extends "base.html" %}
{% block content %}
  <h1>An unexpected error has occurred</h1>
  <p>The administrator has been notified. Sorry for the inconvenience!</p>
  <p><a href=" url_for('index') ">Back</a></p>
{% endblock %}
```

Register the module:

```python
# app/init.py: Import error handlers
# ...
from app import routes, models, errors
```
If you set FLASK_DEBUG=0 in your terminal session (or delete the FLASK_DEBUG variable), and then trigger the duplicate username bug one more time, you are going to see a slightly more friendly error page.

![Friendly error page](https://raw.githubusercontent.com/tunafish304/microblog/refs/heads/main/docs/images/chapter7_photo_3.png)

---

## Sending Errors by Email

Add email config to `config.py`:

```python
# config.py: Email configuration
class Config:
	# ...
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['your-email@example.com']
```

Add SMTPHandler to `app/init.py`:

```python
# app/init.py: Log errors by email
import logging
from logging.handlers import SMTPHandler
# ...
if not app.debug:
	if app.config['MAIL_SERVER']:
		auth = None
		if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
			auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
		secure = None
		if app.config['MAIL_USE_TLS']:
			secure = ()
		mail_handler = SMTPHandler(
			mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
			fromaddr='no-reply@' + app.config['MAIL_SERVER'],
			toaddrs=app.config['ADMINS'], subject='Microblog Failure',
			credentials=auth, secure=secure)
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)

from app import routes, models, errors
```

An alternative is to test with aiosmtpd:

```
(venv) $ pip install aiosmtpd
(venv) $ aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025
```

Set environment:

```
export MAIL_SERVER=localhost
export MAIL_PORT=8025
```

Or use Gmail:

```
export MAIL_SERVER=smtp.googlemail.com
export MAIL_PORT=587
export MAIL_USE_TLS=1
export MAIL_USERNAME=<your-gmail-username>
export MAIL_PASSWORD=<your-gmail-password>
```
Yet another alternative is to use a dedicated email service such as SendGrid(https://sendgrid.com/), which allows you to send up to 100 emails per day on a free account.
---

## Logging to a File

Add RotatingFileHandler:

```python
# app/init.py: Logging to a file
# ...
from logging.handlers import RotatingFileHandler
import os
# ...
if not app.debug:
	# ...
	if not os.path.exists('logs'):
		os.mkdir('logs')
	file_handler = RotatingFileHandler('logs/microblog.log',
									   maxBytes=10240, backupCount=10)
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.setLevel(logging.INFO)
	app.logger.info('Microblog startup')
```

---

## Fixing the Duplicate Username Bug

Update the form:

```python
# app/forms.py: Validate username in edit profile form.
class EditProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
	submit = SubmitField('Submit')

	def init(self, original_username, *args, **kwargs):
		super().init(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = db.session.scalar(sa.select(User).where(
				User.username == username.data))
			if user is not None:
				raise ValidationError('Please use a different username.')
```

Update the route:

```python
# app/routes.py: Validate username in edit profile form.
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	# ...
```

---

## Enabling Debug Mode Permanently

Add to `.flaskenv`:

```bash
# .flaskenv: Environment variables for flask command
FLASK_APP=microblog.py
FLASK_DEBUG=1
```

---

