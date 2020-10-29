from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer,  SignatureExpired

app = Flask(__name__)
app.config.from_pyfile("config.cfg")

mail = Mail(app)
url = URLSafeTimedSerializer("SENHA_SECRETA")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return "<form method='POST' action='/'><input type='email' name='email'/><input type='submit' value='Enviar'/></form>"
    if request.method == "POST":
        try:
            email = request.form["email"]
            token = url.dumps(email, salt="email-confirm")

            msg = Message("Confirm Email", sender="agavi2014@hotmail.com", recipients=[email])
            link = url_for('confirm_email', token = token, external = True)
            msg.body = "Seu link está assim {}".format(link)
            mail.send(msg)
            return "<h1>O E-mail é {}. O token é {}</h1>".format(email, token)
        except Exception as e:
            print(e)
        

@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        email = url.loads(token, salt="email-confirm", max_age=100)
    except SignatureExpired:
        return '<h1>The Token is Expired</h1>'
   
    return "O token está funcionando. E-mail: {}".format(email)

if __name__ == "__main__":
    app.debug = True
    app.run()