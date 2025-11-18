from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Welcome to Rajneesh’s Web App!</h1>"


@app.route('/about')
def about():
    return "This is a simple Flask app running on Python."


if __name__ == '__main__':
    app.run(debug=True)
