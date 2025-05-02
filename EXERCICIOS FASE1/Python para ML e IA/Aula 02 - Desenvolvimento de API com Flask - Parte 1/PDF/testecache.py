from flask import Flask, jsonify
from flask_caching import Cache
import time

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def realizar_calculo_complexo():
    time.sleep(5)  # Simula uma operação demorada
    return "cálculo finalizado"


@app.route('/expensive')
@cache.cached(timeout=50)
def expensive_operation():
    resultado = realizar_calculo_complexo()
    return jsonify({"resultado": resultado})


if __name__ == '__main__':
    app.run(debug=True)
