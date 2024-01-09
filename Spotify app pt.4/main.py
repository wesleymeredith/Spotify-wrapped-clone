# gonna create a flask app that will authenticate? authorize? to use spotifys data
# it's going to publish the results on a html page, nice.

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")