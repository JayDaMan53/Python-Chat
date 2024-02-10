from flask import Flask, render_template, request, jsonify
import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

app = Flask(__name__, template_folder='Assets')

@app.route('/')
def Home():
    return render_template('Main.html')

if __name__ == '__main__':
    app.run(host=IPAddr, port=5001)