##  1. Intro to Flask-WTF

Flask-WTF integrates WTForms with Flask, simplifying form creation and validation. It also adds CSRF protection, which requires a `SECRET_KEY`.

###  Configuration Setup

```python
# config.py
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
```

####  Line-by-Line Explanation
- `import os`: Accesses environment variables.
- `class Config(object)`: Defines a configuration class for Flask.
- `SECRET_KEY = ...`: Sets a secret key for CSRF protection. Uses an environment variable if available, otherwise defaults to a hardcoded string.
---
### app/\_\_init\_\_.py
 Now that we have a config file we need to tell Flask how to read it and apply it. We can do it right after we create the Flask application instance:
```bash
#app/__init__.py
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
```
The lowercase "config" is the name of the Python module config.py, and obviously the one with the uppercase "C" is the actual class.

The following illustrates how to access configuration items with a dictionary syntax:
```bash
>>> from microblog import app
>>> app.config['SECRET_KEY']
'you-will-never-guess'
```
---

##  2. User Login Form

Defines a login form using Flask-WTF. The form includes username, password, a "remember me" checkbox, and a submit button.

###  LoginForm Definition

```python
# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
```

####  Line-by-Line Explanation
- `FlaskForm`: Base class for forms in Flask.
- `StringField`, `PasswordField`, etc.: Define input types.
- `DataRequired()`: Validator that ensures the field isn't empty.
- `LoginForm`: Custom form class with four fields.

---

##  3. Form Templates

The form is rendered in `login.html` using Jinja2. CSRF protection is handled via `form.hidden_tag()`.

###  login.html Template

```html
{% extends "base.html" %}
{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post">
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}
        </p>
        <p>
            {{ form.remember_me() }} {{ form.remember_me.label }}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

####  Line-by-Line Explanation
- `form.hidden_tag()`: Inserts hidden fields for CSRF protection.
- `form.username.label`: Renders the label for the username field.
- `form.username(size=32)`: Renders the input field with a size attribute.
- Similar structure for password and remember_me.
- `form.submit()`: Renders the submit button.

---

##  4. Form Views

The `/login` route handles form rendering and submission logic.

###  routes.py View Function

```python
# app/routes.py
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
```

####  Line-by-Line Explanation
- `render_template`: Renders HTML templates.
- `flash`: Displays one-time messages.
- `redirect`, `url_for`: Handle navigation.
- `LoginForm()`: Instantiates the form.
- `render_template(...)`: Passes form to the template.

---

##  5. Receiving Form Data

Handles form submission and validation using `validate_on_submit()`.

###  Updated login View

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
```

####  Line-by-Line Explanation
- `validate_on_submit()`: Returns `True` if form is submitted and valid.
- `form.username.data`: Accesses submitted username.
- `form.remember_me.data`: Accesses checkbox value.
- `flash(...)`: Displays a message.
- `redirect(...)`: Navigates to the index page.

---

##  6. Improving Field Validation

Adds error feedback to the form template.

###  Error Display in login.html

```html
<p>
    {{ form.username.label }}<br>
    {{ form.username(size=32) }}<br>
    {% for error in form.username.errors %}
        <span style="color: red;">[{{ error }}]</span>
    {% endfor %}
</p>
```

####  Line-by-Line Explanation
- `form.username.errors`: List of validation errors.
- Loop renders each error in red text below the field.

---

##  7. Generating Links

Replaces hardcoded URLs with `url_for()` for maintainability.

###  Template Navigation Example

```html
<a href="{{ url_for('login') }}">Login</a>
```

####  Line-by-Line Explanation
- `url_for('login')`: Dynamically generates the URL for the login route.
- Ensures links stay valid even if route paths change.

---
