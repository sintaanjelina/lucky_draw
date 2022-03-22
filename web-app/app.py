from flask import Flask, jsonify, request, render_template, send_file, make_response

app = Flask(__name__)


@app.route('/')
def index():
    path = request.path
    return render_template('index.html', data=path)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
