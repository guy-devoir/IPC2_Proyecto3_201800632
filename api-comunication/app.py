from flask import Flask
import sys
from flask_cors import CORS

from routes.factura import factura

app = Flask(__name__)
CORS(app)

@app.route('/')
def getDatos():
    return 'Sir Isaac Newton'

app.register_blueprint(factura, url_prefix='/api/factura')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4000)