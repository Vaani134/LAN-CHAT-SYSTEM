from flask import Flask, render_template
from blueprints.register import register_blueprint
from blueprints.login import login_blueprint  
from conn2 import create_connection, insert_user, insert_contact, insert_audit, insert_message
from blueprints.chat import chat_blueprint
from blueprints.logout import logout_blueprint
from blueprints.add import add_blueprint

app = Flask(__name__)
app.secret_key = 'vani'

# Register blueprints
app.register_blueprint(register_blueprint)  # For registration
app.register_blueprint(login_blueprint)     # For login
app.register_blueprint(chat_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(add_blueprint)


# Home route
@app.route('/')
def home():
    return render_template('dashboard.html')

if __name__ == "__main__":
    #app.run(debug=True,host='10.112.67.84')
    app.run(debug=True)
