from flask import Flask,render_template,request
import login_request
import  sandbox_content as sdbox

app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_name=request.form.get("name")
        user_password=request.form.get("password")
        
        login_request.login(
            USERNAME=user_name,
            PASSWORD=user_password)

    return render_template("index.html")


@app.route("/sandboxConten")
def sandbox():
    name = sdbox.USERNAME
    sandboxcontent  = sdbox.content.split("\n")
    sandboxcontent = "<br>".join(sandboxcontent)
    return render_template("sandbox.html" ,user_name=name, content=sandboxcontent)


if __name__ == "__main__":
    app.run(debug=True)