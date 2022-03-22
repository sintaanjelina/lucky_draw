from flask import Flask, jsonify, request, render_template, send_file, make_response

app = Flask(__name__)


@app.route('/')
def index():
    path = request.path
    return render_template('index.html', data=path)


@app.route('/beranda')
def home():
    path = request.path
    return render_template('home.html', data=path)


@app.route('/peserta')
def participant():
    path = request.path
    return render_template('participant.html', data=path)


@app.route('/hadiah')
def reward():
    path = request.path
    return render_template('reward.html', data=path)


@app.route('/pemenang')
def winner():
    path = request.path
    return render_template('winner.html', data=path)


@app.route('/undian')
def lucky_draw():
    path = request.path
    return render_template('lucky_draw.html', data=path)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
