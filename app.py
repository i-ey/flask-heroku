from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_wolrd():
    return "Hello le monde"
           
if __name__=='__name__':
    app.run()