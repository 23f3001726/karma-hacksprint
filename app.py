from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template_string('KARMA TESTING')

if __name__ == '__main__':
    app.run()