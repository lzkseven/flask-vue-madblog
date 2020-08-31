from flask import jsonify, make_response, json

from app.api import bp
@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify("pong!")


@bp.route('/test1', methods=["GET"])
def test_make_response():
    resp=make_response(json.dumps({'status':'sucess'}))
    resp.headers['Content-Type']='application/json'
    return resp


@bp.route('/test2', methods=["GET"])
def test_make_response1():

    resp=jsonify({'status':'sucess'})
    resp.status_code=201
    return resp

