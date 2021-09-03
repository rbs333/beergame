from flask import Flask

app = Flask(__name__)


def fancy_function(data):
    return data['x'] + data['y']*2


@app.route('/')
def hello_world():
    data = {"x": 20, "y": 50}

    res = fancy_function(data)

    return f'Hello Robert!! {res}'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
