from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import login_request
import sandbox_content as sdbox
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(12).hex()  # Required for session and flash messaging

X = None  # Global user name
responseData = None

@app.route("/", methods=["GET", "POST"])
def index():
    global X
    if request.method == "POST":
        user_name = request.form.get("name")
        user_password = request.form.get("password")
        X = user_name

        login_checking = login_request.login(
            USERNAME=user_name,
            PASSWORD=user_password
        )

        if login_checking:
            flash('Login successful! Redirecting to sandbox...', 'success')
            return redirect(url_for('sandbox'))
        else:
            flash('Login failed! Please check your username and password.', 'error')
            return redirect(url_for('index'))

    return render_template("index.html")

# API endpoint to receive data from frontend
@app.route("/sandData", methods=["POST"])
def sand_data():
    global responseData
    data = request.get_json()  # Retrieve JSON data from the request
    print("Data received:", data)  # Print data to verify
    responseData = {"status": "success", "data": data}  # Create a response object
    return jsonify(responseData)  # Return a JSON response to the client


@app.route("/sandboxContent", methods=["GET", "POST"])
def sandbox():
    global X
    old_word = request.form.get("old_words")
    new_word = request.form.get("new_words")
    sandboxcontent = sdbox.fetch_sandbox_content(X).split("<br>")
    
    sandboxcontent = "\n".join(sandboxcontent)
    
    output = sandboxcontent.replace(str(old_word), str(new_word),responseData['data']['index'])

    if old_word and new_word:
        login_request.edit_sandbox(username=X, new_content=output)
    else:
        print("not editing sandbox!")

    return render_template("sandbox.html", user_name=X, content=output)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
