from app import (  # noqa: F401
    app,
    cli,  # noqa: F401
    db,
)
from app.models import Post, User  # noqa: F401


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Post": Post}
