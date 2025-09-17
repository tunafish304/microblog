
## Section: Password Hashing

### Summary 1: Hashing a Password with Werkzeug

You use `generate_password_hash()` from Werkzeug to convert a plain-text password into a secure, irreversible hash. This hash includes a random salt, so even the same password produces different hashes each time. This protects against attackers identifying reused passwords.

```python
>>> from werkzeug.security import generate_password_hash
>>> hash = generate_password_hash('foobar')
>>> hash
'scrypt:32768:8:1$DdbIPADqKg2nniws$4ab051ebb6767a...'
```

---

### Summary 2: Verifying a Password

To check if a user-entered password matches the stored hash, you use `check_password_hash()`. It returns `True` if the password is correct, and `False` otherwise. This is used during login to validate credentials.

```python
>>> from werkzeug.security import check_password_hash
>>> check_password_hash(hash, 'foobar')
True
>>> check_password_hash(hash, 'barfoo')
False
```

---

### Summary 3: Adding Password Methods to the User Model

You add two methods to the `User` class:
- `set_password()` hashes and stores the password.
- `check_password()` verifies a password against the stored hash.

This encapsulates password logic inside the model and ensures that raw passwords are never stored.

```python
from werkzeug.security import generate_password_hash, check_password_hash

# ...

class User(db.Model):
    # ...

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

---

### Summary 4: Using the Password Methods in Practice

This shell example shows how to use the new methods:
- Create a user.
- Set their password.
- Verify it with correct and incorrect inputs.

This confirms that the password logic works as expected.

```python
>>> u = User(username='susan', email='susan@example.com')
>>> u.set_password('mypassword')
>>> u.check_password('anotherpassword')
False
>>> u.check_password('mypassword')
True
```
---

## Section: Introduction to Flask-Login

### Summary 1: What Flask-Login Does

Flask-Login is a widely used extension that manages user authentication. It keeps track of whether a user is logged in, allows them to stay logged in across pages, and supports "remember me" functionality so they remain logged in even after closing the browser. This is essential for building apps with personalized user experiences.

---

### Summary 2: Installing Flask-Login

Before using Flask-Login, you need to install it in your virtual environment. This makes the extension available to your Flask app.

```bash
(venv) $ pip install flask-login
```

---

### Summary 3: Initializing Flask-Login in Your App

After installing, you initialize Flask-Login by creating a `LoginManager` instance and attaching it to your Flask app. This setup goes in `app/__init__.py`, right after the app is created.

```python
# ...
from flask_login import LoginManager

app = Flask(__name__)
# ...
login = LoginManager(app)

# ...
```

This prepares your app to manage user sessions and authentication. Later in the chapter, you’ll configure how Flask-Login loads users and handles login behavior.

---

## Section: Preparing the User Model for Flask-Login

### Summary

Flask-Login expects your user model to implement four key properties and methods:

- `is_authenticated`: Returns `True` if the user is logged in.
- `is_active`: Returns `True` if the user’s account is active.
- `is_anonymous`: Returns `False` for regular users.
- `get_id()`: Returns a unique identifier for the user as a string.

These are needed so Flask-Login can manage user sessions and identify users across requests. Instead of writing these manually, you can use the `UserMixin` class provided by Flask-Login. It supplies default implementations that work for most applications.

To use it, you simply inherit from `UserMixin` in your `User` model:

```python
# ...
from flask_login import UserMixin

class User(UserMixin, db.Model):
    # ...
```

This makes your model compatible with Flask-Login without requiring any additional changes. You're now ready to let Flask-Login manage user sessions using your database-backed user model.

---

## Section: User Loader Function

### Summary

Flask-Login tracks the logged-in user by storing their unique ID in Flask’s session object. This session data persists across requests, allowing the app to “remember” who the user is as they navigate the site.

However, Flask-Login doesn’t know how to retrieve a user from your database—it needs you to define a function that takes a user ID and returns the corresponding user object. This is called the **user loader function**, and it’s registered using the `@login.user_loader` decorator.

In this example, the user loader function is added to `app/models.py`. Since Flask-Login stores the ID as a string, you convert it to an integer before querying the database.

```python
from app import login
# ...

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
```

This function allows Flask-Login to reconstruct the full user object from the session ID on every request, enabling features like `current_user` to work seamlessly.

---

## Section: Logging Users In

### Summary 1: Importing Required Modules

Before implementing the login logic, you import the necessary components:
- `current_user` and `login_user` from Flask-Login
- SQLAlchemy for querying
- Your database instance (`db`)
- The `User` model

These imports prepare your route to handle login functionality and interact with the database.

```python
# ...
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.models import User
```

---

### Summary 2: Defining the Login Route

You define a `/login` route that handles both GET and POST requests. The logic inside this route does the following:

1. **Redirects already logged-in users**:  
   If `current_user.is_authenticated` is `True`, the user is already logged in, so you redirect them to the homepage (`index`). This prevents unnecessary login attempts.

2. **Processes the login form**:  
   You create a `LoginForm` instance and check if it was submitted and validated.

3. **Queries the database for the user**:  
   You use `db.session.scalar()` with a `where()` clause to find a user whose username matches the one submitted in the form.

4. **Verifies the password**:  
   If the user exists, you call `check_password()` to verify the password. If either the user is not found or the password is incorrect, you flash an error message and redirect back to the login page.

5. **Logs the user in**:  
   If both username and password are valid, you call `login_user()` to log the user in. You also pass `remember=form.remember_me.data` to optionally keep the user logged in across sessions.

6. **Redirects to the homepage**:  
   After successful login, the user is redirected to the index page.

```python
# ...

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
```

---

## Section: Logging Users Out

### Summary 1: Logout View Function

To allow users to log out, you define a `/logout` route that calls Flask-Login’s `logout_user()` function. This clears the user’s session and effectively logs them out. After logging out, the user is redirected to the homepage.

```python
# ...
from flask_login import logout_user

# ...

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
```

This simple route ensures that users can end their session securely and cleanly.

---

### Summary 2: Conditional Login/Logout Links in the Navigation Bar

To reflect the user’s login status in the UI, you update the navigation bar in `base.html`. You use `current_user.is_anonymous` to determine whether to show a **Login** or **Logout** link.

- If the user is anonymous (not logged in), show the **Login** link.
- If the user is authenticated, show the **Logout** link.

```html
<div>
    Microblog:
    <a href="{{ url_for('index') }}">Home</a>
    {% if current_user.is_anonymous %}
    <a href="{{ url_for('login') }}">Login</a>
    {% else %}
    <a href="{{ url_for('logout') }}">Logout</a>
    {% endif %}
</div>
```

This dynamic behavior improves the user experience by clearly showing their authentication state and offering the appropriate action.

---

## Section: Requiring Users to Login

### Summary 1: Setting the Login View

To enable automatic redirection for protected pages, Flask-Login needs to know which view handles logins. You configure this in `app/__init__.py` by setting `login.login_view` to the name of your login view function.

```python
# ...
login = LoginManager(app)
login.login_view = 'login'
```

This tells Flask-Login to redirect unauthenticated users to `/login` when they try to access protected routes.

---

### Summary 2: Protecting Routes with `@login_required`

To restrict access to certain views, you use the `@login_required` decorator. This ensures that only authenticated users can access the route. If a user isn’t logged in, Flask-Login redirects them to the login page.

```python
from flask_login import login_required

@app.route('/')
@app.route('/index')
@login_required
def index():
    # ...
```

This is a simple and powerful way to enforce authentication across your app.

---

### Summary 3: Redirecting to the Original Page After Login

When Flask-Login redirects a user to the login page, it appends a `next` query string to the URL, indicating the page the user originally wanted to visit. After a successful login, you can read this value and redirect the user back to that page—if it’s safe.

You use `request.args.get('next')` to retrieve the value, and `urlsplit()` to ensure it’s a relative URL (to prevent open redirects to malicious sites).

```python
from flask import request
from urllib.parse import urlsplit

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ...
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # ...
```

This logic ensures that:
- If no `next` argument is provided, the user is redirected to the homepage.
- If `next` is a relative path, the user is redirected there.
- If `next` is a full URL with a domain, it’s ignored for security reasons.

---

## Section: Showing the Logged-In User in Templates

### Summary 1: Using `current_user` in Templates

Now that your app has real users, you can replace the placeholder user from Chapter 2 with Flask-Login’s `current_user` object. This object is automatically available in templates and represents the currently logged-in user. You use it to personalize the homepage with a greeting and to display who authored each post.

```html
{% extends "base.html" %}

{% block content %}
    <h1>Hi, {{ current_user.username }}!</h1>
    {% for post in posts %}
    <div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div>
    {% endfor %}
{% endblock %}
```

This makes the homepage dynamic and user-specific, showing real data from your database.

---

### Summary 2: Removing the User Argument from the View Function

Since `current_user` is available globally in templates, you no longer need to pass a `user` argument manually from the view function. You simplify the route by removing that argument and just passing the list of posts.

```python
@app.route('/')
@app.route('/index')
@login_required
def index():
    # ...
    return render_template("index.html", title='Home Page', posts=posts)
```

This keeps your view logic cleaner and leverages Flask-Login’s built-in functionality.

---

### Summary 3: Creating a User via the Flask Shell

Because user registration hasn’t been implemented yet, you manually add a user to the database using the Flask shell. This allows you to test the login and logout flow with a real user.

```python
>>> u = User(username='susan', email='susan@example.com')
>>> u.set_password('cat')
>>> db.session.add(u)
>>> db.session.commit()
```

Once this user is added, you can log in through the app and see personalized content. After logging out, Flask-Login redirects you back to the login page, confirming that session management is working correctly.

---

## Section: User Registration

### Summary 1: Creating the Registration Form Class

You define a `RegistrationForm` in `app/forms.py` using Flask-WTF. It includes fields for username, email, password, and password confirmation. You also add custom validation methods to ensure the username and email are unique.

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User

# ...

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
```

This form uses both built-in and custom validators. The `Email()` validator requires an extra package:

```bash
(venv) $ pip install email-validator
```

---

### Summary 2: Creating the Registration Template

You create `register.html` to display the form. It’s structured similarly to the login form and includes error messages for each field.

```html
{% extends "base.html" %}

{% block content %}
    <h1>Register</h1>
    <form action="" method="post">
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}<br>
            {% for error in form.username.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>
            {{ form.email.label }}<br>
            {{ form.email(size=64) }}<br>
            {% for error in form.email.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}<br>
            {% for error in form.password.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>
            {{ form.password2.label }}<br>
            {{ form.password2(size=32) }}<br>
            {% for error in form.password2.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

---

### Summary 3: Adding a Link to the Registration Page

You update `login.html` to include a link for new users to register.

```html
<p>New User? <a href="{{ url_for('register') }}">Click to Register!</a></p>
```

This improves navigation and encourages sign-ups.

---

### Summary 4: Creating the Registration View Function

You define a `/register` route in `app/routes.py`. It checks if the user is already logged in, processes the form, creates a new user, hashes the password, saves the user to the database, and redirects to the login page.

```python
from app import db
from app.forms import RegistrationForm

# ...

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
```

This completes the user registration flow. New users can now sign up, log in, and log out—all with secure password handling and validation.

---





