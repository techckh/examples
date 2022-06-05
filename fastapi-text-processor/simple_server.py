from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/jp/convert', methods=['GET', 'POST'])
def simple_api():
    content = request.json
    print(request)
    print(content)
    return jsonify({'msg': 'hello world'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
