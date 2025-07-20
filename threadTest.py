import threading

from flask import Flask, current_app

app = Flask(__name__)
app.config["EXAMPLE"] = "Hello from Flask!"


def worker(app_instance):
    with app_instance.app_context():  # manually create a context
        print("In thread:", current_app.config["EXAMPLE"])


@app.route("/")
def index():
    real_app = current_app._get_current_object()
    thread = threading.Thread(target=worker, args=(real_app,))
    thread.start()
    return "Thread started!"


if __name__ == "__main__":
    app.run()
