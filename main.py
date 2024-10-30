from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,make_response
import login_request
import sandbox_content as sdbox
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(12).hex()  # Required for session and flash messaging

X = None  # Global user name

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


@app.route("/sandboxContent", methods=["GET","POST"])
def sandbox():
    global X
    sandboxcontent = sdbox.fetch_sandbox_content(X).split("<br>")
    sandboxcontent = "\n".join(sandboxcontent)
    return render_template("sandbox.html", user_name=X, content=sandboxcontent)


@app.route('/receive_data', methods=["POST"])
def receive_data():
    data = request.get_json()
    print("Received data:", data)

    if data['status'] == "PASS":
        login_request.edit_sandbox(
            username=X,
            new_content=data['EditSandBoxContent']
            )
        print("sandbox edit is successfully !")
    else:
        print("sandbox edit is not found !")

    return make_response(jsonify({"status": "success"}), 200)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
