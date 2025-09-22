
---

##  User Profile Page

###  Summary

This section introduces a route for viewing a user's profile. The URL pattern includes the username, and the view function queries the database for that user. If the user exists, it renders a profile page with their info and posts.

###  Code

```python
#app/routes.py: User profile view function

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
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
### Code

```html
#app/templates/user.html: User profile template

{% extends "base.html" %}

{% block content %}
    <h1>User: {{ user.username }}</h1>
    <hr>
    {% for post in posts %}
    <p>
    {{ post.author.username }} says: <b>{{ post.body }}</b>
    </p>
    {% endfor %}
{% endblock %}
```
### Code
```html
app/templates/base.html: User profile template

        <div>
            Microblog:
            <a href="{{ url_for('index') }}">Home</a>
            {% if current_user.is_anonymous %}
            <a href="{{ url_for('login') }}">Login</a>
            {% else %}
            <a href="{{ url_for('user', username=current_user.username) }}">Profile</a>
            <a href="{{ url_for('logout') }}">Logout</a>
            {% endif %}
        </div>
``` 
![Users table schema](https://raw.githubusercontent.com/tunafish304/microblog/refs/heads/main/docs/images/chapter6_photo_1.png)

Give the application a try now. Clicking on the Profile link at the top should take you to your own user page. At this point there are no links that will take you to the profile page of other users, but if you want to access those pages you can type the URL by hand in the browser's address bar. For example, if you have a user named "john" registered on your application, you can view the corresponding user profile by typing http://localhost:5000/user/john in the address bar.

---

## Avatars

### Summary

Gravatar (Globally Recognized Avatar) is a free service that provides profile images based on a user's email address. Flask apps can use Gravatar to automatically display avatars for users without needing to store image files.

To use Gravatar, you generate a URL that includes an MD5 hash of the user's email address. This URL returns the user's avatar image if they have one registered with Gravatar—or a default image if not.


- `email.lower().encode('utf-8')` ensures consistent hashing
- `digest` is the MD5 hash of the email
- `size` controls the pixel dimensions of the avatar
- `?d=identicon` tells Gravatar to use a geometric pattern if no avatar is found

```bash
#shell example
>>> from hashlib import md5
>>> 'https://www.gravatar.com/avatar/' + md5(b'john@example.com').hexdigest()
'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
```
If you want to see an actual example, Miguel's  Gravatar URL is:
```html
https://www.gravatar.com/avatar/729e26a2a2c7ff24a71958d4aa4e5f35
```
By default, the image size returned is 80x80 pixels, but a different size can be requested by adding an s argument to the URL's query string. For example, to obtain Miguel's avatar as a 128x128 pixel image, the URL is:

```html
https://www.gravatar.com/avatar/729e26a2a2c7ff24a71958d4aa4e5f35?s=128
```
Since avatars are associated with users, it makes sense to add the logic that generates the avatar URLs to the user model:

```python
#app/models.py: User avatar URLs

from hashlib import md5
# ...

class User(UserMixin, db.Model):
    # ...
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
```        
If you are interested in learning about other options offered by the Gravatar service, visit their documentation website(https://gravatar.com/site/implement/images).

The next step is to insert the avatar images in the user profile template:

```html
app/templates/user.html: User avatar in template

{% extends "base.html" %}

{% block content %}
    <table>
        <tr valign="top">
            <td><img src="{{ user.avatar(128) }}"></td>
            <td><h1>User: {{ user.username }}</h1></td>
        </tr>
    </table>
    <hr>
    {% for post in posts %}
    <p>
    {{ post.author.username }} says: <b>{{ post.body }}</b>
    </p>
    {% endfor %}
{% endblock %}
```
---
To show avatars for the individual posts just make one more small change in the template:

```html
app/templates/user.html: User avatars in posts

{% extends "base.html" %}

{% block content %}
    <table>
        <tr valign="top">
            <td><img src="{{ user.avatar(128) }}"></td>
            <td><h1>User: {{ user.username }}</h1></td>
        </tr>
    </table>
    <hr>
    {% for post in posts %}
    <table>
        <tr valign="top">
            <td><img src="{{ post.author.avatar(36) }}"></td>
            <td>{{ post.author.username }} says:<br>{{ post.body }}</td>
        </tr>
    </table>
    {% endfor %}
{% endblock %}
```
![Users table schema](https://raw.githubusercontent.com/tunafish304/microblog/refs/heads/main/docs/images/chapter6_photo_2.png)

## Using Jinja Sub-Templates

### Summary

To keep templates clean and reusable, Flask supports sub-templates using the `{% include %}` directive. In this section, you create a `_post.html` sub-template to render individual posts. This avoids repeating markup and makes it easier to update post formatting later.

### Code

```html
#app/templates/_post.html: Post sub-template

    <table>
        <tr valign="top">
            <td><img src="{{ post.author.avatar(36) }}"></td>
            <td>{{ post.author.username }} says:<br>{{ post.body }}</td>
        </tr>
    </table>
```

To invoke this sub-template from the user.html template just use Jinja's include statement:

```html
#app/templates/user.html: User avatars in posts

{% extends "base.html" %}

{% block content %}
    <table>
        <tr valign="top">
            <td><img src="{{ user.avatar(128) }}"></td>
            <td><h1>User: {{ user.username }}</h1></td>
        </tr>
    </table>
    <hr>
    {% for post in posts %}
        {% include '_post.html' %}
    {% endfor %}
{% endblock %}
```
This keeps your main template focused and readable.

---

## More Interesting Profiles 

### Summary

To make user profiles more meaningful, you add two new fields to the `User` model:

- `about_me`: a short bio or personal description
- `last_seen`: a timestamp of the user's last activity

These fields are stored in the database and later displayed on the profile page.

### Code

```python
#app/models.py: New fields in user model

class User(UserMixin, db.Model):
    # ...
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
```

After updating the model, you’ll need to generate a migration and apply it.

---

### Code

Run these commands in your terminal:

```bash
(venv) $ flask db migrate -m "new fields in user model"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'user.about_me'
INFO  [alembic.autogenerate.compare] Detected added column 'user.last_seen'
  Generating migrations/versions/37f06a334dbf_new_fields_in_user_model.py ... done
```
This updates your database schema to include the new fields. Now apply this change to the database:

```bash
(venv) $ flask db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 780739b227a7 -> 37f06a334dbf, new fields in user model
```
Realize how useful it is to work with a migration framework. Any users that were in the database are still there, the migration framework surgically applies the changes in the migration script without destroying any data.

For the next step, add these two new fields to the user profile template:

### Code

```python
app/templates/user.html: Show user information in user profile template

{% extends "base.html" %}

{% block content %}
    <table>
        <tr valign="top">
            <td><img src="{{ user.avatar(128) }}"></td>
            <td>
                <h1>User: {{ user.username }}</h1>
                {% if user.about_me %}<p>{{ user.about_me }}</p>{% endif %}
                {% if user.last_seen %}<p>Last seen on: {{ user.last_seen }}</p>{% endif %}
            </td>
        </tr>
    </table>
    ...
{% endblock %}
```
Note that these two fields are in Jinja's conditionals, because they should only be visible if they are set. At this point these two new fields are empty for all users, so you are not going to see these fields yet.

## Recording The Last Visit Time For a User

### Summary

This section adds logic to update the `last_seen` field in the `User` model every time a logged-in user makes a request. It uses Flask’s `before_request` hook, which runs before every request is processed.

This gives you a simple way to track user activity and display it on their profile. 

### Code

Take a look at the solution. In `app/routes.py`, add this near the top:

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

---
![Users table schema](https://raw.githubusercontent.com/tunafish304/microblog/refs/heads/main/docs/images/chapter6_photo_3.png)

## Profile Editor

### Summary

This section adds a form that lets users edit their profile information—specifically their username and bio (`about_me`). You’ll create a new form class, a route to handle the form, and a template to render it.

---

### Step 1: Create the Edit Profile Form

In `app/forms.py`, add:

```python
#app/forms.py: Profile editor form

from wtforms import TextAreaField
from wtforms.validators import Length

# ...

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
```

---

### Step 2: Create the Template

In `app/templates/edit_profile.html`, add:

```html
#app/templates/edit_profile.html: Profile editor form

{% extends "base.html" %}

{% block content %}
    <h1>Edit Profile</h1>
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
            {{ form.about_me.label }}<br>
            {{ form.about_me(cols=50, rows=4) }}<br>
            {% for error in form.about_me.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```
### Step 3: Add the Route to Handle the Form

In `app/routes.py`, add:

```python
#app/routes.py: Edit profile view function

from app.forms import EditProfileForm

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
```

![Users table schema](https://raw.githubusercontent.com/tunafish304/microblog/refs/heads/main/docs/images/chapter6_photo_4.png)

---
To make it easy for users to access the profile editor page, you can add a link in their profile page:

```html
#app/templates/user.html: Edit profile link

                {% if user == current_user %}
                <p><a href="{{ url_for('edit_profile') }}">Edit your profile</a></p>
                {% endif %}
```
Pay attention to the clever conditional I'm using to make sure that the Edit link appears when you are viewing your own profile, but not when you are viewing the profile of someone else.

![Users table schema](https://raw.githubusercontent.com/tunafish304/microblog/refs/heads/main/docs/images/chapter6_photo_5.png)
