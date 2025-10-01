

### The Setup: Self-Referential Many-to-Many

You're using a `followers` association table to model a social graph where users can follow other users. The table likely looks like this:

```python
followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id')),
    Column('followed_id', Integer, ForeignKey('users.id'))
)
```

This means:
- Each row represents one user following another.
- `follower_id` is the person doing the following.
- `followed_id` is the person being followed.

---

### The Relationships: Following vs Followers

You're defining two relationships on the `User` model:

#### 1. `following` — Who the current user is following

```python
following: so.WriteOnlyMapped['User'] = so.relationship(
    secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    back_populates='followers'
)
```

- `primaryjoin`: match rows where `follower_id == current_user.id`
- `secondaryjoin`: get the `followed_id` from those rows
- Result: a list of users the current user is following

#### 2. `followers` — Who is following the current user

```python
followers: so.WriteOnlyMapped['User'] = so.relationship(
    secondary=followers,
    primaryjoin=(followers.c.followed_id == id),
    secondaryjoin=(followers.c.follower_id == id),
    back_populates='following'
)
```

- `primaryjoin`: match rows where `followed_id == current_user.id`
- `secondaryjoin`: get the `follower_id` from those rows
- Result: a list of users who follow the current user

---

### Summary

| Relationship | Description | SQLAlchemy Join Logic |
|--------------|-------------|------------------------|
| `following`  | Users the current user follows | `follower_id == id → followed_id` |
| `followers`  | Users who follow the current user | `followed_id == id → follower_id` |


### Think of `back_populates` as a Two-Way Mirror

When you define:

```python
User.following = relationship(..., back_populates="followers")
User.followers = relationship(..., back_populates="following")
```

You’re saying:

- `user.following` and `user.followers` are **two sides of the same relationship**.
- If you **append** a user to `user.following`, SQLAlchemy will **automatically update** the other user’s `.followers` list in memory — and vice versa.

---

### Example

```python
alice.following.append(bob)
```

Now, without querying the database again:

```python
bob.followers  # will include alice
```

That’s the magic of `back_populates`: it keeps both ends of the relationship in sync **in memory**, so your app logic stays clean and intuitive.

---


