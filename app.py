import os
from datetime import timedelta
# dotenv setup

from dotenv import load_dotenv
load_dotenv()

env_var = "GENX_GOOGLE_OAUTH"
# env_var = "ANDROID_SDK_ROOT"


try:
    # user logged in
    access_token = os.environ[env_var]
    print(access_token)
except:
    print("User not logged in")
    # use flask server for google oauth and store it as env variable
    import webbrowser
    from multiprocess import Process

    #flask setup
    from flask import Flask, redirect, url_for, session,request
    app = Flask(__name__)
    server = Process(target=app.run)
    
    # authlib setup
    from authlib.integrations.flask_client import OAuth
    oauth = OAuth(app)

    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    # Session config
    app.secret_key = os.getenv("APP_SECRET_KEY")
    app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

    google = oauth.register(
        name='google',
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
        client_kwargs={'scope': 'email profile'},
    )


    @app.route("/login")
    def login():
        google = oauth.create_client('google')  # create the google oauth client
        redirect_uri = url_for('authorize', _external=True)
        return google.authorize_redirect(redirect_uri)

    @app.route("/authorize")
    def authorize():
        google = oauth.create_client('google')  # create the google oauth client
        # global access_token
        access_token = google.authorize_access_token()  # Access token from google (needed to get user info)
        print(access_token)
        # server.terminate()
        shutdown_server()
        # return "Loggen In"

    # open a webbrowser with the login route
    webbrowser.open_new_tab("localhost:5000/login")
    # how to wait till the access_token is received 

    # print(access_token)
    # close the flask server 
    # storing the access_token in environment variable
    if __name__ == "__main__":
        # server.start()
        app.run(debug=True)
        # server.join()



