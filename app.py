from flask import Flask, render_template, redirect, Response
app = Flask(__name__)
from gevent.pywsgi import WSGIServer
from distutils.util import strtobool

from Unifi import Unifi
from Passwords import Passwords

# ENVs
from dotenv import load_dotenv
config = load_dotenv(".env")
import os

# Allow password regeneration to be toggled
regen_passwd_enabled = strtobool(os.getenv("PASSWORD_REGEN", default="false"))


@app.route("/")
def index():
    session_token, anti_forgery = Unifi.auth()
    data = Unifi.get_wifi_config(session_token, anti_forgery)
    return render_template("index.j2", ssid=data["name"], passwd=data["x_passphrase"], regen_passwd_enabled=regen_passwd_enabled)

@app.route("/new", methods = ["POST"])
def regenerate_password():
    if regen_passwd_enabled:
        # Auth to Unifi
        session_token, anti_forgery = Unifi.auth()
        
        # Get current config
        current_config = Unifi.get_wifi_config(session_token, anti_forgery)

        # Create a new password
        new_password = Passwords.generate_passphrase()

        # Create a new config
        new_config = Unifi.create_set_wifi_config_payload(current_config, new_password)
        
        # Set that new password in the controller
        Unifi.set_wifi_config(session_token, anti_forgery, new_config)
        
        # Redirect to normal page
        return redirect(location="/")
    
    # Fail-safe is password regen is disabled...
    else:
        return Response("Password regeneration has not been enabled")


if (os.getenv("ENVIRONMENT") == "prod"):
    # Prod
    if __name__ == '__main__':
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
        print("Server running on port 5000")
    
elif (os.getenv("ENVIRONMENT") == "dev"):
    # Dev
    app.run(host='0.0.0.0', port='5000', debug=True)

else:
    print("ENVIRONMENT must be configured as 'dev' or 'prod'")