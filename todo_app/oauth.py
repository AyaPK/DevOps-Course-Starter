import os
from flask_dance.contrib.github import make_github_blueprint

blueprint = make_github_blueprint(
    client_id=os.getenv('OAUTH_CLIENT_ID'),
    client_secret=os.getenv('OAUTH_CLIENT_SECRET'),
    redirect_url="http://localhost:5000/login/github/authorized"
)


@blueprint.before_app_request
def debug_redirect_uri():
    if blueprint.session:
        print(f"Redirect URI: {blueprint.session.redirect_uri}")