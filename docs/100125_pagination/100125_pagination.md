## Chapter 9 Pagination

The home page needs to have a form in which users can type new posts. First I create a form class:

```python
# app/forms.py: Blog submission form.

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
```

Next, I can add this form to the template for the main page of the application:

```html
# app/templates/index.html: Post submission form in index template

{% extends "base.html" %}

{% block content %}
    <h1>Hi, {{ current_user.username }}!</h1>
    <form action="" method="post">
        {{ form.hidden_tag() }}
        <p>
            {{ form.post.label }}<br>
            {{ form.post(cols=32, rows=4) }}<br>
            {% for error in form.post.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
    {% for post in posts %}
    <p>
    {{ post.author.username }} says: <b>{{ post.body }}</b>
    </p>
    {% endfor %}
{% endblock %}
```

The changes in this template are similar to how previous forms were handled. The final part is to add the form creation and handling in the view function:

#app/routes.py: Post submission form in index view function.

```python
from app.forms import PostForm
from app.models import Post

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home Page', form=form,
                           posts=posts)
```

Now I have the following_posts() method in the User model that returns a query for the posts that a given user wants to see. So now I can replace the fake posts with real posts:

```python
# app/routes.py: Display real posts in home page.

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # ...
    posts = db.session.scalars(current_user.following_posts()).all()
    return render_template("index.html", title='Home Page', form=form,
                           posts=posts)
```

## Making it easier to find users to follow

I'm going to create a new page that I'm going to call the "Explore" page. This page will work like the home page, but instead of only showing posts from followed users, it will show a global post stream from all users. Here is the new explore view function:

```python
app/routes.py: Explore view function.

@app.route('/explore')
@login_required
def explore():
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.session.scalars(query).all()
    return render_template('index.html', title='Explore', posts=posts)
```

Did you notice something odd in this view function? The render_template() call references the index.html template, which I'm using in the main page of the application. Since this page is going to be very similar to the main page, I decided to reuse the template. But one difference with the main page is that in the explore page I do not want to have a form to write blog posts, so in this view function I did not include the form argument in the render_template() call.

To prevent the index.html template from crashing when it tries to render a web form that does not exist, I'm going to add a conditional that only renders the form if it was passed by the view function:

```html
# app/templates/index.html: Make the blog post submission form optional.

{% extends "base.html" %}

{% block content %}
    <h1>Hi, {{ current_user.username }}!</h1>
    {% if form %}
    <form action="" method="post">
        ...
    </form>
    {% endif %}
    ...
{% endblock %}
```

I'm also going to add a link to this new page in the navigation bar, right after the index page link:

```html
# app/templates/base.html: Link to explore page in navigation bar.

        <a href="{{ url_for('explore') }}">Explore</a>
```

Remember the _post.html sub-template that I have introduced in Chapter 6 to render blog posts in the user profile page? This was a small template that was included from the user profile page template, and was written in a separate file so that it can also be used from other templates. I'm now going to make a small improvement to it, which is to show the username of the blog post author as a clickable link:

```html
# app/templates/_post.html: Show link to author in blog posts.

    <table>
        <tr valign="top">
            <td><img src="{{ post.author.avatar(36) }}"></td>
            <td>
                <a href="{{ url_for('user', username=post.author.username) }}">
                    {{ post.author.username }}
                </a>
                says:<br>{{ post.body }}
            </td>
        </tr>
    </table>
```

I can now use this sub-template to render blog posts in the home and explore pages:

```html
# app/templates/index.html: Use blog post sub-template.

    ...
    {% for post in posts %}
        {% include '_post.html' %}
    {% endfor %}
    ...
```
![Users table schema](https://raw.githubusercontent.com/tunafish304/microblog/refs/heads/main/docs/images/chapter9_photo1.png)

## Pagination of blog posts

Initially I'm going to show just a limited number of posts at a time, and include links to navigate forward and backward through the complete list of posts. Flask-SQLAlchemy supports pagination natively with the db.paginate() function, which works like db.session.scalars(), but with pagination built-in. If for example, I want to get the first twenty followed posts of the user, I can do this:

```Bash
>>> query = sa.select(Post).order_by(Post.timestamp.desc())
>>> posts = db.paginate(query, page=1, per_page=20, error_out=False).items
```
Now let's think about how I can implement pagination in the index() view function. I can start by adding a configuration item to the application that determines how many items will be displayed per page.

```python
# config.py: Posts per page configuration.

class Config:
    # ...
    POSTS_PER_PAGE = 3
```
Next, I need to decide how the page number is going to be incorporated into application URLs. A fairly common way is to use a query string argument to specify an optional page number, defaulting to page 1 if it is not given. Here are some example URLs that show how I'm going to implement this:

- Page 1, implicit: http://localhost:5000/index
- Page 1, explicit: http://localhost:5000/index?page=1
- Page 3: http://localhost:5000/index?page=3

Below you can see how I added pagination to the home and explore view functions:

```python
# app/routes.py: Followers association table

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # ...
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(current_user.following_posts(), page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items)

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    return render_template("index.html", title='Explore', posts=posts.items)
```

With these changes, the two routes determine the page number to display, either from the page query string argument or a default of 1, and then use the paginate() method to retrieve only the desired page of results. The POSTS_PER_PAGE configuration item that determines the page size is accessed through the app.config object.

## Page navigation

The next change is to add links at the bottom of the blog post list that allow users to navigate to the next and/or previous pages. Remember that I mentioned that the return value from a paginate() call is an object of a Pagination class from Flask-SQLAlchemy? So far, I have used the items attribute of this object, which contains the list of items retrieved for the selected page. But this object has a few other attributes that are useful when building pagination links:

- has_next: True if there is at least one more page after the current one
- has_prev: True if there is at least one more page before the current one
- next_num: page number for the next page
- prev_num: page number for the previous page

With these four elements, I can generate next and previous page links and pass them down to the templates for rendering:

```python
# app/routes.py: Next and previous page links.

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # ...
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(current_user.following_posts(), page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

 @app.route('/explore')
 @login_required
 def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)
```
The next_url and prev_url in these two view functions are going to be set to URLs returned by Flask's url_for() function, but only if there is a page to go to in that direction. If the current page is at one of the ends of the collection of posts, then the has_next or has_prev attributes of the Pagination object will be False, and in that case the link in that direction will be set to None.

The pagination links are being set to the index.html template, so now let's render them on the page, right below the post list:

```html
# app/templates/index.html: Render pagination links on the template.

    ...
    {% for post in posts %}
        {% include '_post.html' %}
    {% endfor %}
    {% if prev_url %}
    <a href="{{ prev_url }}">Newer posts</a>
    {% endif %}
    {% if next_url %}
    <a href="{{ next_url }}">Older posts</a>
    {% endif %}
    ...
```
![Users table schema](https://raw.githubusercontent.com/tunafish304/microblog/refs/heads/main/docs/images/chapter9_photo2.png)

## Pagination in the user profile

The changes for the index page are sufficient for now. However, there is also a list of posts in the user profile page, which shows only posts from the owner of the profile. To be consistent, the user profile page should be changed to match the pagination style of the index page.

I begin by updating the user profile view function, which still had a list of fake post objects in it.

```html
# app/routes.py: Pagination in the user profile view function.

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)
    query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=app.config['POSTS_PER_PAGE'],
                        error_out=False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)
```

Finally, the changes to the user.html template are identical to those I made on the index page:

```html
# app/templates/user.html: Pagination links in the user profile template.

    ...
    {% for post in posts %}
        {% include '_post.html' %}
    {% endfor %}
    {% if prev_url %}
    <a href="{{ prev_url }}">Newer posts</a>
    {% endif %}
    {% if next_url %}
    <a href="{{ next_url }}">Older posts</a>
    {% endif %}
```
After you are done experimenting with the pagination feature, you can set the POSTS_PER_PAGE configuration item to a more reasonable value:

```python
# config.py: Posts per page configuration.

class Config:
    # ...
    POSTS_PER_PAGE = 25
```


