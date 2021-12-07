import os
import uuid

from flask import Flask, request, abort
from flask import make_response, jsonify
import redis

r = redis.Redis(host='localhost', port=6379)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/generate_codes')
    def generate_codes():
        brand_id = request.args.get('brand_id', None)
        codes_number = int(request.args.get('codes_number', 0))
        if not brand_id or not codes_number:
            abort(400)
        uuids = []
        for i in range(1, codes_number + 1):
            uuids.append(str(uuid.uuid4()))
            if i % 100 == 0 or i == codes_number:
                r.sadd(f"brand:{brand_id}", *uuids)
                uuids = []

        r.set('foo', 'bar')
        return {"generated_codes_number": r.scard(f"brand:{brand_id}")}

    @app.route('/get_code')
    def get_code():
        brand_id = request.args.get('brand_id', None)
        user_id = request.args.get('user_id', None)
        if not user_id or not brand_id:
            abort(400)
        # ToDo transaction operate
        code = r.spop(f"brand:{brand_id}")
        r.sadd(f"brand:{brand_id}_assigned", code)
        r.hset(f"brand:{brand_id}_user", code, user_id)
        return {"code": code.decode()}

    def activate_code():
       pass

    @app.errorhandler(400)
    def bad_request(error):
        return make_response(jsonify({'error': 'Bad Request'}), 400)

    return app
