from flask import Flask, render_template, request, redirect, url_for, flash
import login_request
import sandbox_content as sdbox
import os

app = Flask(__name__)
app.secret_key = os.urandom(12).hex() # Required for session and flash messaging

X = None

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
            return redirect(url_for('index'))
        else:
            flash('Login failed! Please check your username and password.', 'error')
            return redirect(url_for('index'))

    return render_template("index.html")

@app.route("/sandboxContent", methods=["GET", "POST"])
def sandbox():
    global X
    old_word = request.form.get("old_words") 
    new_word = request.form.get("new_words") 
    sandboxcontent = sdbox.fetch_sandbox_content(X).split("\n")
    sandboxcontent = "<br>".join(sandboxcontent)
    output = sandboxcontent.replace(str(old_word), str(new_word))

    login_request.edit_sandbox(username=X, new_content=output)

    return render_template("sandbox.html", user_name=X, content=output)

if __name__ == "__main__":
    app.run(debug=True)
