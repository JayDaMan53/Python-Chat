from flask import Flask, render_template, request, jsonify
import socket
import threading
import time

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

app = Flask(__name__, template_folder='Assets',)
onlineUsers = {}  # Change to dictionary to track last ping time

def remove_inactive_users():
    while True:
        current_time = time.time()
        for user, last_ping in list(onlineUsers.items()):
            if current_time - last_ping > 5:  # User inactive for more than 10 seconds
                print(f"Removing inactive user: {user}")
                del onlineUsers[user]
        time.sleep(2)  # Check every 5 seconds

@app.route('/')
def Home():
    return render_template('Main.html')

@app.route('/Send', methods=['POST'])
def Send():
    message = request.json
    print(message)
    with open('Log.txt', 'a') as file:
        file.write(message["User"] + ": " + message["Message"] + "\n")
    return "Got message"

@app.route('/Ping', methods=['POST'])
def Pong():
    User = request.json
    username = User.get("User")  # Assuming JSON has a "username" field
    if username:
        onlineUsers[username] = time.time()  # Update last ping time
    with open('Log.txt', 'r') as file:
        return jsonify({"messages": file.read(), "Users": onlineUsers})

if __name__ == '__main__':
    # Start the background thread for removing inactive users
    threading.Thread(target=remove_inactive_users, daemon=True).start()
    app.run(host=IPAddr, port=5001)