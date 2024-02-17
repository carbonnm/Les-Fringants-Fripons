from flask import Flask, render_template

config_data = {}
app = Flask(__name__, template_folder="../resources/templates", static_folder="../resources/static")


@app.route('/')
async def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
