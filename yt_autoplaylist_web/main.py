import os

from autoplaylist_web import app

if __name__ == '__main__':
    # When running locally, disable OAuth-lib's HTTPs verification. When
    # running in production *do not* leave this option enabled.

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('localhost', 8080, debug=True)
