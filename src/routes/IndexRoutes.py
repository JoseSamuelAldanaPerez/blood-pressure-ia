from flask import Blueprint, jsonify, request
import traceback
from src.utils.Logger import Logger

main = Blueprint('index_blueprint', __name__)


@main.route('/')
def index():
    try:
        Logger.add_to_log('info', '{} {}'.format(request.method, request.path))
        return "OK"
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())

        response = jsonify(
            {'message': 'Internal Server Error', 'success': False})
        return response, 500


@main.route('/about')
def about():
    return jsonify({
        "name": "Proyecto IA Agosto-Diciembre 2024",
        "version": "0.0.0",
        "authors": "Samuel Aldana"
    })
