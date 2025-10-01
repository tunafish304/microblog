## Chapter 8 summary detail

---

```python
# app/models.py: Followers association table

followers = sa.Table(
	'followers',
	db.metadata,
	sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
			  primary_key=True),
	sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
			  primary_key=True)
)
```

Detailed Explanation:
- `followers = sa.Table(...)`: Defines a plain SQLAlchemy table (not a model class) to represent the many-to-many relationship between users.
- `'followers'`: The name of the table in the database.
- `db.metadata`: Registers the table with SQLAlchemy’s metadata system so it’s included in migrations.
- `sa.Column('follower_id', ...)`: Each row stores the ID of the user who is doing the following.
- `sa.Column('followed_id', ...)`: Each row stores the ID of the user being followed.
- `primary_key=True`: Both columns together form a composite primary key, ensuring no duplicate follower-followed pairs.

This table is used as a bridge in the `User` model’s relationships.

---

```python
# app/models.py: Many-to-many followers relationship

class User(UserMixin, db.Model):
	# ...
	following: so.WriteOnlyMapped['User'] = so.relationship(
		secondary=followers, primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		back_populates='followers')
	followers: so.WriteOnlyMapped['User'] = so.relationship(
		secondary=followers, primaryjoin=(followers.c.followed_id == id),
		secondaryjoin=(followers.c.follower_id == id),
		back_populates='following')
```

Detailed Explanation:
- `following`: Defines the users that this user is following.
  - `secondary=followers`: Uses the `followers` table as the association.
  - `primaryjoin`: Matches rows where this user is the follower.
  - `secondaryjoin`: Matches rows where the other user is the followed.
  - `back_populates='followers'`: Links this relationship to the inverse (`followers`).
- `followers`: Defines the users who follow this user.
  - The join logic is reversed: this user is the followed, and the other is the follower.
  - `back_populates='following'`: Keeps both sides in sync.

This setup allows bidirectional access: `user.following` and `user.followers`.

---

```bash
(venv) $ flask db migrate -m "followers"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'followers'
  Generating /home/miguel/microblog/migrations/versions/ae346256b650_followers.py ... done

(venv) $ flask db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 37f06a334dbf -> ae346256b650, followers
```

Detailed Explanation:
- `flask db migrate`: Scans the models for changes and generates a migration script.
- `-m "followers"`: Adds a message to label the migration.
- Alembic detects the new `followers` table and creates the migration file.
- `flask db upgrade`: Applies the migration to the database.
- The upgrade moves the schema from the previous version (`37f06a334dbf`) to the new one (`ae346256b650`), adding the `followers` table.

This step is required before using any follower-related logic.

---

```python
app/models.py: Add and remove followers

class User(UserMixin, db.Model):
	#...

	def follow(self, user):
		if not self.is_following(user):
			self.following.add(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.following.remove(user)

	def is_following(self, user):
		query = self.following.select().where(User.id == user.id)
		return db.session.scalar(query) is not None

	def followers_count(self):
		query = sa.select(sa.func.count()).select_from(
			self.followers.select().subquery())
		return db.session.scalar(query)

	def following_count(self):
		query = sa.select(sa.func.count()).select_from(
			self.following.select().subquery())
		return db.session.scalar(query)
```

Detailed Explanation:
- `follow(user)`: Adds `user` to this user’s `following` list if not already present.
- `unfollow(user)`: Removes `user` from the `following` list if present.
- `is_following(user)`: Builds a query to check if `user.id` is in the current user’s `following` relationship.
  - `self.following.select()`: Returns a selectable query for the relationship.
  - `where(User.id == user.id)`: Filters for the target user.
  - `db.session.scalar(...)`: Returns a single result or `None`.
- `followers_count()`: Counts how many users follow this user.
  - Uses `self.followers.select().subquery()` to build a subquery.
  - `sa.func.count()` counts the rows.
- `following_count()`: Same logic, but for users this user follows.

---

```python
# app/models.py: Following posts query

class User(UserMixin, db.Model):
	#...
	def following_posts(self):
		Author = so.aliased(User)
		Follower = so.aliased(User)
		return (
			sa.select(Post)
			.join(Post.author.of_type(Author))
			.join(Author.followers.of_type(Follower), isouter=True)
			.where(sa.or_(
				Follower.id == self.id,
				Author.id == self.id,
			))
			.group_by(Post)
			.order_by(Post.timestamp.desc())
		)
```

Detailed Explanation:
- `Author = so.aliased(User)`: Creates an alias for the `User` model to represent post authors.
- `Follower = so.aliased(User)`: Creates another alias to represent followers.
- `sa.select(Post)`: Starts a query to select posts.
- `.join(Post.author.of_type(Author))`: Joins each post to its author using the `Author` alias.
- `.join(Author.followers.of_type(Follower), isouter=True)`: Joins each author to their followers, allowing posts with no followers (outer join).
- `.where(sa.or_(...))`: Filters posts where either:
  - The current user is a follower of the author (`Follower.id == self.id`), or
  - The current user is the author (`Author.id == self.id`).
- `.group_by(Post)`: Ensures each post appears only once in the result.
- `.order_by(Post.timestamp.desc())`: Sorts posts by newest first.

This query builds the user’s timeline: their own posts plus posts from users they follow.

---

```python
tests.py: User model unit tests.

import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
from app import app, db
from app.models import User, Post
```

Detailed Explanation:
- `os.environ['DATABASE_URL'] = 'sqlite://'`: Sets up an in-memory SQLite database for testing.
- `datetime`, `timezone`, `timedelta`: Used to create precise timestamps for posts.
- `unittest`: Python’s built-in testing framework.
- Imports the app, database, and models for use in tests.

---

```python
class UserModelCase(unittest.TestCase):
	def setUp(self):
		self.app_context = app.app_context()
		self.app_context.push()
		db.create_all()
```

Detailed Explanation:
- `setUp()`: Runs before each test.
- `app.app_context()`: Creates an application context so Flask can access config and database.
- `db.create_all()`: Creates all tables fresh for each test.

---

```python
	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()
```

Detailed Explanation:
- `tearDown()`: Cleans up after each test.
- `db.session.remove()`: Clears the session.
- `db.drop_all()`: Deletes all tables.
- `self.app_context.pop()`: Exits the app context.

---

```python
	def test_password_hashing(self):
		u = User(username='susan', email='susan@example.com')
		u.set_password('cat')
		self.assertFalse(u.check_password('dog'))
		self.assertTrue(u.check_password('cat'))
```

Detailed Explanation:
- Creates a user and sets a password.
- Verifies that the correct password passes and the wrong one fails.

---

```python
	def test_avatar(self):
		u = User(username='john', email='john@example.com')
		self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
										 'd4c74594d841139328695756648b6bd6'
										 '?d=identicon&s=128'))
```

Detailed Explanation:
- Tests the avatar URL generation using Gravatar.
- The hash is based on the email address.

---

```python
	def test_follow(self):
		u1 = User(username='john', email='john@example.com')
		u2 = User(username='susan', email='susan@example.com')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
```

Detailed Explanation:
- Creates two users and commits them to the test database.

---

```python
		following = db.session.scalars(u1.following.select()).all()
		followers = db.session.scalars(u2.followers.select()).all()
		self.assertEqual(following, [])
		self.assertEqual(followers, [])
```

Detailed Explanation:
- Verifies that neither user is following anyone initially.

---

```python
		u1.follow(u2)
		db.session.commit()
		self.assertTrue(u1.is_following(u2))
		self.assertEqual(u1.following_count(), 1)
		self.assertEqual(u2.followers_count(), 1)
```

Detailed Explanation:
- `u1` follows `u2`.
- Confirms the relationship and checks the counts.

---

```python
		u1_following = db.session.scalars(u1.following.select()).all()
		u2_followers = db.session.scalars(u2.followers.select()).all()
		self.assertEqual(u1_following[0].username, 'susan')
		self.assertEqual(u2_followers[0].username, 'john')
```

Detailed Explanation:
- Verifies that the correct usernames appear in the relationship lists.

---

```python
		u1.unfollow(u2)
		db.session.commit()
		self.assertFalse(u1.is_following(u2))
		self.assertEqual(u1.following_count(), 0)
		self.assertEqual(u2.followers_count(), 0)
```

Detailed Explanation:
- `u1` unfollows `u2`.
- Confirms the relationship is removed and counts reset.

---

```python
	def test_follow_posts(self):
		# create four users
		u1 = User(username='john', email='john@example.com')
		u2 = User(username='susan', email='susan@example.com')
		u3 = User(username='mary', email='mary@example.com')
		u4 = User(username='david', email='david@example.com')
		db.session.add_all([u1, u2, u3, u4])
```

Detailed Explanation:
- Sets up four users for timeline testing.

---

```python
		# create four posts
		now = datetime.now(timezone.utc)
		p1 = Post(body="post from john", author=u1,
				  timestamp=now + timedelta(seconds=1))
		p2 = Post(body="post from susan", author=u2,
				  timestamp=now + timedelta(seconds=4))
		p3 = Post(body="post from mary", author=u3,
				  timestamp=now + timedelta(seconds=3))
		p4 = Post(body="post from david", author=u4,
				  timestamp=now + timedelta(seconds=2))
		db.session.add_all([p1, p2, p3, p4])
		db.session.commit()
```

Detailed Explanation:
- Creates one post per user with staggered timestamps.
- Commits all posts to the database.

---

```python
		# setup the followers
		u1.follow(u2)  # john follows susan
		u1.follow(u4)  # john follows david
		u2.follow(u3)  # susan follows mary
		u3.follow(u4)  # mary follows david
		db.session.commit()
```

Detailed Explanation:
- Sets up a follower graph to test post visibility.

---

```python
		# check the following posts of each user
		f1 = db.session.scalars(u1.following_posts()).all()
		f2 = db.session.scalars(u2.following_posts()).all()
		f3 = db.session.scalars(u3.following_posts()).all()
		f4 = db.session.scalars(u4.following_posts()).all()
		self.assertEqual(f1, [p2, p4, p1])
		self.assertEqual(f2, [p2, p3])
		self.assertEqual(f3, [p3, p4])
		self.assertEqual(f4, [p4])
```

Detailed Explanation:
- Calls `following_posts()` for each user.
- Verifies that each timeline includes the correct posts based on follower relationships.

---

```bash
(venv) $ python tests.py
[2023-11-19 14:51:07,578] INFO in init: Microblog startup
test_avatar (main.UserModelCase.test_avatar) ... ok
test_follow (main.UserModelCase.test_follow) ... ok
test_follow_posts (main.UserModelCase.test_follow_posts) ... ok
test_password_hashing (main.UserModelCase.test_password_hashing) ... ok

--------------------
Ran 4 tests in 0.259s

OK
```

Detailed Explanation:
- Runs the test suite.
- All four tests pass, confirming that follower logic, password hashing, avatar generation, and post visibility are working correctly.

---

```python
# app/forms.py: Empty form for following and unfollowing.

class EmptyForm(FlaskForm):
	submit = SubmitField('Submit')
```

Detailed Explanation:
- `class EmptyForm(FlaskForm)`: Defines a minimal form class using Flask-WTF. It’s used for actions that don’t require user input — just a secure POST.
- `submit = SubmitField('Submit')`: Adds a single submit button. The label `'Submit'` is usually overridden in the template to say `'Follow'` or `'Unfollow'`.
- This form exists solely to provide CSRF protection for follow/unfollow actions. Even though it looks empty, it includes a hidden CSRF token via `form.hidden_tag()`.

---

```python
app/routes.py: Follow and unfollow routes.

from app.forms import EmptyForm

# ...

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = db.session.scalar(
			sa.select(User).where(User.username == username))
		if user is None:
			flash(f'User {username} not found.')
			return redirect(url_for('index'))
		if user == current_user:
			flash('You cannot follow yourself!')
			return redirect(url_for('user', username=username))
		current_user.follow(user)
		db.session.commit()
		flash(f'You are following {username}!')
		return redirect(url_for('user', username=username))
	else:
		return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = db.session.scalar(
			sa.select(User).where(User.username == username))
		if user is None:
			flash(f'User {username} not found.')
			return redirect(url_for('index'))
		if user == current_user:
			flash('You cannot unfollow yourself!')
			return redirect(url_for('user', username=username))
		current_user.unfollow(user)
		db.session.commit()
		flash(f'You are not following {username}.')
		return redirect(url_for('user', username=username))
	else:
		return redirect(url_for('index'))
```

Detailed Explanation:
- `@app.route('/follow/<username>', methods=['POST'])`: Defines a POST-only route to follow a user.
- `@login_required`: Ensures only authenticated users can follow/unfollow.
- `form = EmptyForm()`: Instantiates the CSRF-protected form.
- `form.validate_on_submit()`: Validates the form and CSRF token.
- `db.session.scalar(...)`: Queries the database for the target user.
- `if user is None`: Handles the case where the username doesn’t exist.
- `if user == current_user`: Prevents users from following themselves.
- `current_user.follow(user)`: Adds the target user to the current user’s `following` relationship.
- `db.session.commit()`: Saves the change to the database.
- `flash(...)`: Sends a feedback message to the user.
- `return redirect(...)`: Redirects back to the profile page.

The `unfollow` route mirrors this logic but removes the relationship instead.

---

```python
# app/routes.py: Follow and unfollow routes.
@app.route('/user/<username>')
@login_required
def user(username):
	# ...
	form = EmptyForm()
	return render_template('user.html', user=user, posts=posts, form=form)
```

Detailed Explanation:
- `@app.route('/user/<username>')`: Defines the route for viewing a user’s profile.
- `@login_required`: Ensures only logged-in users can access profiles.
- `form = EmptyForm()`: Prepares the CSRF-protected form to be passed into the template.
- `render_template(...)`: Renders the profile page and passes the user object, their posts, and the form.

This setup allows the template to conditionally render follow/unfollow buttons.

---

```html
# app/templates/user.html: Follow and unfollow links in user profile page.
...
		<h1>User:  user.username </h1>
		{% if user.about_me %}<p> user.about_me </p>{% endif %}
		{% if user.last_seen %}<p>Last seen on:  user.last_seen </p>{% endif %}
		<p> user.followers_count()  followers,  user.following_count()  following.</p>
		{% if user == current_user %}
		<p><a href=" url_for('edit_profile') ">Edit your profile</a></p>
		{% elif not current_user.is_following(user) %}
		<p>
			<form action=" url_for('follow', username=user.username) " method="post">
				 form.hidden_tag() 
				 form.submit(value='Follow') 
			</form>
		</p>
		{% else %}
		<p>
			<form action=" url_for('unfollow', username=user.username) " method="post">
				 form.hidden_tag() 
				 form.submit(value='Unfollow') 
			</form>
		</p>
		{% endif %}
...
```

Detailed Explanation:
- `<h1>User:  user.username </h1>`: Displays the username of the profile being viewed.
- ` user.about_me ` and ` user.last_seen `: Show optional profile metadata.
- ` user.followers_count() ` and ` user.following_count() `: Call model methods to display follower stats.
- `{% if user == current_user %}`: If viewing your own profile, show an edit link.
- `{% elif not current_user.is_following(user) %}`: If viewing another user and not following them, show a follow button.
- `<form action=" url_for('follow', ...) " method="post">`: Submits a POST request to follow the user.
- ` form.hidden_tag() `: Inserts CSRF token.
- ` form.submit(value='Follow') `: Renders the button with a custom label.
- The `else` block renders the unfollow form if already following.

This template dynamically adjusts based on the relationship between the viewer and the profile owner.

---

```python
app/forms.py: Empty form for following and unfollowing.

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
```

**Detailed Explanation**:
- `class EmptyForm(FlaskForm)`: Defines a minimal form class using Flask-WTF. It’s used for actions that don’t require user input — just a secure POST.
- `submit = SubmitField('Submit')`: Adds a single submit button. The label `'Submit'` is usually overridden in the template to say `'Follow'` or `'Unfollow'`.
- This form exists solely to provide CSRF protection for follow/unfollow actions. Even though it looks empty, it includes a hidden CSRF token via `form.hidden_tag()`.

---

```python
app/routes.py: Follow and unfollow routes.

from app.forms import EmptyForm

# ...

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
```

**Detailed Explanation**:
- `@app.route('/follow/<username>', methods=['POST'])`: Defines a POST-only route to follow a user.
- `@login_required`: Ensures only authenticated users can follow/unfollow.
- `form = EmptyForm()`: Instantiates the CSRF-protected form.
- `form.validate_on_submit()`: Validates the form and CSRF token.
- `db.session.scalar(...)`: Queries the database for the target user.
- `if user is None`: Handles the case where the username doesn’t exist.
- `if user == current_user`: Prevents users from following themselves.
- `current_user.follow(user)`: Adds the target user to the current user’s `following` relationship.
- `db.session.commit()`: Saves the change to the database.
- `flash(...)`: Sends a feedback message to the user.
- `return redirect(...)`: Redirects back to the profile page.

The `unfollow` route mirrors this logic but removes the relationship instead.

---

```python
# app/routes.py: Follow and unfollow routes.
@app.route('/user/<username>')
@login_required
def user(username):
    # ...
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)
```

**Detailed Explanation**:
- `@app.route('/user/<username>')`: Defines the route for viewing a user’s profile.
- `@login_required`: Ensures only logged-in users can access profiles.
- `form = EmptyForm()`: Prepares the CSRF-protected form to be passed into the template.
- `render_template(...)`: Renders the profile page and passes the user object, their posts, and the form.

This setup allows the template to conditionally render follow/unfollow buttons.

---

```html
# app/templates/user.html: Follow and unfollow links in user profile page.
...
        <h1>User: {{ user.username }}</h1>
        {% if user.about_me %}<p>{{ user.about_me }}</p>{% endif %}
        {% if user.last_seen %}<p>Last seen on: {{ user.last_seen }}</p>{% endif %}
        <p>{{ user.followers_count() }} followers, {{ user.following_count() }} following.</p>
        {% if user == current_user %}
        <p><a href="{{ url_for('edit_profile') }}">Edit your profile</a></p>
        {% elif not current_user.is_following(user) %}
        <p>
            <form action="{{ url_for('follow', username=user.username) }}" method="post">
                {{ form.hidden_tag() }}
                {{ form.submit(value='Follow') }}
            </form>
        </p>
        {% else %}
        <p>
            <form action="{{ url_for('unfollow', username=user.username) }}" method="post">
                {{ form.hidden_tag() }}
                {{ form.submit(value='Unfollow') }}
            </form>
        </p>
        {% endif %}
...
```

**Detailed Explanation**:
- `<h1>User: {{ user.username }}</h1>`: Displays the username of the profile being viewed.
- `{{ user.about_me }}` and `{{ user.last_seen }}`: Show optional profile metadata.
- `{{ user.followers_count() }}` and `{{ user.following_count() }}`: Call model methods to display follower stats.
- `{% if user == current_user %}`: If viewing your own profile, show an edit link.
- `{% elif not current_user.is_following(user) %}`: If viewing another user and not following them, show a follow button.
- `<form action="{{ url_for('follow', ...) }}" method="post">`: Submits a POST request to follow the user.
- `{{ form.hidden_tag() }}`: Inserts CSRF token.
- `{{ form.submit(value='Follow') }}`: Renders the button with a custom label.
- The `else` block renders the unfollow form if already following.

This template dynamically adjusts based on the relationship between the viewer and the profile owner.

---


