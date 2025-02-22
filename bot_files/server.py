from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "OK", 200

@app.route('/telegram')
def telegram():
    data = request.get_json()
    print(data)
    return 'OK', 200


if __name__ == "__main__":
    app.run(debug=True)
