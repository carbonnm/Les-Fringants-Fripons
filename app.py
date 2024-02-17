import routes
from __init__ import app

if __name__ == '__main__':
    app.route('/')(routes.index)
    app.route('/login', methods=["GET", "POST"])(routes.login)
    app.route('/logout')(routes.logout)
    app.route('/profile')(routes.profile)
    app.errorhandler(404)(routes.page_not_found)
    app.errorhandler(500)(routes.server_error)
    app.run()
