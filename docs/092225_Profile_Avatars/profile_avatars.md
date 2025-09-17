
---

##  Section 1: User Profile Page

###  Summary

This section introduces a route for viewing a user's profile. The URL pattern includes the username, and the view function queries the database for that user. If the user exists, it renders a profile page with their info and posts.

###  Code: View Function for Profile Page

```python
@app.route('/user/<username>')
@login_required
def user(username):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is None:
        abort(404)
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)
```

- The `<username>` part in the route makes it dynamic.
- If the user isn’t found, it returns a 404 error.
- The `posts` list is mocked for now—real posts will come later.

---

###  Code: Profile Template (`user.html`)

```html
{% extends "base.html" %}

{% block content %}
    <h1>User: {{ user.username }}</h1>
    {% for post in posts %}
        {% include '_post.html' %}
    {% endfor %}
{% endblock %}
```

This template uses a sub-template (`_post.html`) to render each post. That’s coming up next.

---

## Section 2: Avatars with Gravatar

### Summary

Gravatar (Globally Recognized Avatar) is a free service that provides profile images based on a user's email address. Flask apps can use Gravatar to automatically display avatars for users without needing to store image files.

To use Gravatar, you generate a URL that includes an MD5 hash of the user's email address. This URL returns the user's avatar image if they have one registered with Gravatar—or a default image if not.

### Code: Add `avatar()` Method to User Model

In `app/models.py`, add a method to the `User` class:

```python
import hashlib

class User(db.Model):
    # ...
    def avatar(self, size):
        digest = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
```

- `email.lower().encode('utf-8')` ensures consistent hashing
- `digest` is the MD5 hash of the email
- `size` controls the pixel dimensions of the avatar
- `?d=identicon` tells Gravatar to use a geometric pattern if no avatar is found

### Code: Update `user.html` Template

You can now display the avatar in the profile page:

```html
<img src="{{ user.avatar(128) }}">
<h1>User: {{ user.username }}</h1>
```

This adds a 128x128 avatar image above the username.

---

## Section 3: Sub-Templates for Posts

### Summary

To keep templates clean and reusable, Flask supports sub-templates using the `{% include %}` directive. In this section, you create a `_post.html` sub-template to render individual posts. This avoids repeating markup and makes it easier to update post formatting later.

### Code: Create `_post.html` Template

Save this as `app/templates/_post.html`:

```html
<p>{{ post.author.username }} says: <b>{{ post.body }}</b></p>
```

This is a minimal version, but you can expand it later with timestamps, avatars, or formatting.

### Code: Use Sub-Template in `user.html`

Update the loop in `user.html` to include the sub-template:

```html
{% for post in posts %}
    {% include '_post.html' %}
{% endfor %}
```

This keeps your main template focused and readable.

---

## Section 4: More Interesting Profiles (about_me and last_seen)

### Summary

To make user profiles more meaningful, you add two new fields to the `User` model:

- `about_me`: a short bio or personal description
- `last_seen`: a timestamp of the user's last activity

These fields are stored in the database and later displayed on the profile page.

### Code: Update the `User` Model

In `app/models.py`, add the new fields:

```python
from datetime import datetime

class User(db.Model):
    # ...
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
```

- `about_me` is limited to 140 characters
- `last_seen` defaults to the current UTC time when the user is created

After updating the model, you’ll need to generate a migration and apply it.

---

### Code: Generate and Apply Migration

Run these commands in your terminal:

```bash
flask db migrate -m "add about_me and last_seen to User model"
flask db upgrade
```

This updates your database schema to include the new fields.

---

## Section 5: Recording Last Seen Time

### Summary

This section adds logic to update the `last_seen` field in the `User` model every time a logged-in user makes a request. It uses Flask’s `before_request` hook, which runs before every request is processed.

This gives you a simple way to track user activity and display it on their profile.

### Code: Add `before_request` Handler

In `app/routes.py`, add this near the top:

```python
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
```

- `before_request()` runs before every request
- `current_user.last_seen` is updated to the current UTC time
- The change is committed to the database immediately

This keeps the `last_seen` field fresh and accurate.

### Code: Display `last_seen` in `user.html`

Update your profile template to show the timestamp:

```html
<p>Last seen on: {{ user.last_seen }}</p>
```

You can format this later using Jinja filters or Flask-Moment if you want prettier output.

---

## Section 6: Profile Editor Form and View

### Summary

This section adds a form that lets users edit their profile information—specifically their username and bio (`about_me`). You’ll create a new form class, a route to handle the form, and a template to render it.

---

### Step 1: Create the Edit Profile Form

In `app/forms.py`, add:

```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
```

---

### Step 2: Add the Route to Handle the Form

In `app/routes.py`, add:

```python
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', title='Edit Profile', form=form)
```

- `obj=current_user` pre-fills the form with existing data
- On submit, it updates the user and saves changes to the database

---

### Step 3: Create the Template

In `app/templates/edit_profile.html`, add:

```html
{% extends "base.html" %}

{% block content %}
    <h1>Edit Your Profile</h1>
    <form method="post">
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}
        </p>
        <p>
            {{ form.about_me.label }}<br>
            {{ form.about_me(rows=4, cols=40) }}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

---





