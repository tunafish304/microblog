

# Analysis of the following_posts query

"Followers" is the audience who looks at your content,  whereas "following" is the content you look at.  

followers - those who follow you<br>
followed -  those who you follow<br>

### The following_posts query builds posts authored by the current user or by users the current user follows:


```python
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

## Stage 1: Users Table

### Query Context  
_No query yet—just the base data._

###  Data Snapshot  
| id | username |
|----|----------|
| 1  | john     |
| 2  | susan    |
| 3  | mary     |
| 4  | david    |

### Concept  
Each user has a unique ID and name. No relationships yet — just identities.

---

## Stage 2: Followers Table

### Query Context  
_No query yet—just the relationship data._

### Data Snapshot  
| follower_id | followed_id |
|-------------|-------------|
| 1           | 2           | ← john → susan  
| 1           | 4           | ← john → david  
| 2           | 3           | ← susan → mary  
| 3           | 4           | ← mary → david  

### Concept  
This table models who follows whom. It’s directional: `follower_id` follows `followed_id`.

---

## Stage 3: Posts Table

### Query Context  
_No query yet—just the content data._

### Data Snapshot  
| id | text            | user_id |
|----|------------------|---------|
| 1  | post from susan  | 2  
| 2  | post from mary   | 3  
| 3  | post from david  | 4  
| 4  | post from john   | 1  

### Concept  
Each post is authored by a user (`user_id`). This is the content we’ll filter based on relationships.

---

## Stage 4: Join `Post → Author`

### Query Line  
```python
.join(Post.author.of_type(Author))
```

### Data Snapshot  
| post.id | post.text       | post.user_id | user.id | user.username |
|---------|------------------|--------------|---------|----------------|
| 1       | post from susan  | 2            | 2       | susan  
| 2       | post from mary   | 3            | 3       | mary  
| 3       | post from david  | 4            | 4       | david  
| 4       | post from john   | 1            | 1       | john  

### Concept  
We join each post to its author. This sets up the next step: checking who follows the author.

---

## Stage 5: Join `Author → Followers`

### Query Line  
```python
.join(Author.followers.of_type(Follower), isouter=True)
```

### Data Snapshot  
| post.id | post.text       | post.user_id | author.id | author.username | follower.id | follower.username |
|---------|------------------|--------------|-----------|------------------|--------------|--------------------|
| 1       | post from susan  | 2            | 2         | susan            | 1            | john  
| 2       | post from mary   | 3            | 3         | mary             | 2            | susan  
| 3       | post from david  | 4            | 4         | david            | 1            | john  
| 3       | post from david  | 4            | 4         | david            | 3            | mary  

### Concept  
We join the author’s followers. Each row now shows:
- The post
- The author
- A follower of that author

### Join Breakdown

The two join statements:

```python
.join(Post.author.of_type(Author))
.join(Author.followers.of_type(Follower), isouter=True)
```

#### 1. `.join(Post.author.of_type(Author))`

- This is a **default inner join**.
- It joins the current query to the `Author` table via the `Post.author` relationship.
- Only posts with a valid author will be included.

#### 2. `.join(Author.followers.of_type(Follower), isouter=True)`

- This is an **explicit outer join** — specifically a **left outer join**.
- It joins the query to the `followers` of each author.
- Even if an author has **no followers**, they’ll still be included in the result — with `NULL` values for the follower fields.

---

This pattern is often used when you want to:

- Get all posts and their authors (inner join).
- Optionally include follower info (outer join), even if the author has no followers.

---

## Stage 6: Apply `where` Clause

### Query Line  
```python
.where(sa.or_(
    Follower.id == self.id,
    Author.id == self.id,
))
```

### Data Snapshot (for `self.id == 1`, i.e. john)  
| post.id | post.text       | post.user_id | author.id | author.username | follower.id | follower.username |
|---------|------------------|--------------|-----------|------------------|--------------|--------------------|
| 1       | post from susan  | 2            | 2         | susan            | 1            | john  
| 3       | post from david  | 4            | 4         | david            | 1            | john  
| 4       | post from john   | 1            | 1         | john             | null         | null  

### Concept  
We include a post if:
- The current user follows the author (`Follower.id == self.id`)
- OR the current user *is* the author (`Author.id == self.id`)

This is the core of the `following_posts` query.

---

## Stage 7: Multiple Followers per Post

### Query Line  
```python
.group_by(Post)
```

### Data Snapshot  
| post.id | post.text       | post.user_id | author.id | author.username | follower.id | follower.username |
|---------|------------------|--------------|-----------|------------------|--------------|--------------------|
| 3       | post from david  | 4            | 4         | david            | 1            | john  
| 3       | post from david  | 4            | 4         | david            | 3            | mary  

### Concept  
A single post can appear multiple times—once for each follower of the author. We use `.group_by(Post)` to collapse duplicates.

---

## Final Query Assembly

```python
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

### Summary  
> “Show me all posts where I’m either the author or I follow the author. Sort by newest first. Don’t show duplicates.”

---


