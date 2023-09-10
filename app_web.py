from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/incorporar")
def incorporar():
    return render_template('incorporar.html')

@app.route("/receber")
def receber():
    return render_template('receber.html')

