from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#default home page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)