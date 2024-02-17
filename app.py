import routes
from __init__ import app

if __name__ == '__main__':
    app.route('/')(routes.index)
    app.run()
