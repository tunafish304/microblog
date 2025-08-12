
---

## 🧩 Chapter 2 Summary: Templates in Flask

### 🔹 1. Why Templates?
Miguel starts by showing how embedding raw HTML in Python view functions quickly becomes messy and unscalable. Instead, Flask uses Jinja2 templates to separate logic from presentation.

### 🔹 2. Mock Data for Early Development
He introduces a mock `user` dictionary:
```python
user = {'username': 'Miguel'}
```
🧠 *Teaching Tip*: This models how to isolate front-end development from backend dependencies.

---

## 🐍 `routes.py` (initial version)

```python
from flask import Flask
app = Flask(name)

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Miguel'}
	return f"<html><head><title>Home Page</title></head><body><h1>Hello, {user['username']}!</h1></body></html>"
```

🧠 *Annotation*: This hardcoded HTML is fine for prototyping, but it mixes logic and layout—making future changes brittle.

---

## 🗂️ Transition to Templates

### 🔹 3. Create `templates/index.html`

```html
<!doctype html>
<html>
  <head>
	<title> title  - Microblog</title>
  </head>
  <body>
	<h1>Hello,  user.username !</h1>
  </body>
</html>
```

🧠 *Annotation*:
- ` ... ` injects dynamic values.
- `user.username` accesses nested dictionary keys.

---

## 🐍 Updated `routes.py` with `render_template`

```python
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Miguel'}
	return render_template('index.html', title='Home', user=user)
```

🧠 *Annotation*:
- `render_template()` loads the HTML file and fills in placeholders.
- This separates logic (Python) from layout (HTML).

---

## 🔄 Conditional Logic in Templates

```html
<title>
  {% if title %}
	 title  - Microblog
  {% else %}
	Welcome to Microblog!
  {% endif %}
</title>
```

🧠 *Annotation*: `{% ... %}` handles control flow like `if`, `for`, etc.

---

## 🔁 Looping Over Posts

```python
posts = [
	{'author': {'username': 'John'}, 'body': 'Beautiful day in Portland!'},
	{'author': {'username': 'Susan'}, 'body': 'The Avengers movie was so cool!'}
]
```

```html
{% for post in posts %}
  <div><p> post.author.username  says: <b> post.body </b></p></div>
{% endfor %}
```

🧠 *Annotation*: This models dynamic content rendering—students can experiment by adding more posts.

---

## 🧬 Template Inheritance

### 🔹 `base.html`

```html
<!doctype html>
<html>
  <head>
	<title>{% if title %} title  - Microblog{% else %}Welcome to Microblog{% endif %}</title>
  </head>
  <body>
	<div>Microblog: <a href="/index">Home</a></div>
	<hr>
	{% block content %}{% endblock %}
  </body>
</html>
```

### 🔹 `index.html` (refactored)

```html
{% extends "base.html" %}

{% block content %}
  <h1>Hi,  user.username !</h1>
  {% for post in posts %}
	<div><p> post.author.username  says: <b> post.body </b></p></div>
  {% endfor %}
{% endblock %}
```

🧠 *Annotation*: This models DRY principles—shared layout lives in `base.html`, while each page injects its own content.

---

