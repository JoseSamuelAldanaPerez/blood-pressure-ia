from flask import Blueprint, request, jsonify
import traceback
from src.service.BloodPressureService import BloodPressureService
from src.utils.Logger import Logger

main = Blueprint('blood_pressure_blueprint', __name__)


@main.route('/', methods=['GET', 'POST'])
def blood_pressure():
    if request.method == 'GET':
        limit = request.args.get('limit')
        if limit is None:
            limit = 10
        data = BloodPressureService.get_all(limit)
        if (data is not None):
            return jsonify({
                "message": f"{len(data)} registros recuperados",
                "success": True,
                "data": data
            }), 200
        else:
            return jsonify({
                "message": "Error al recuperar los registros de presión arterial",
                "success": False,
            }), 500
    elif request.method == 'POST':
        data = request.get_json()

        if not data or 'systolic' not in data or 'diastolic' not in data:
            return jsonify({
                "message": "Los campos 'systolic' y 'diastolic' son obligatorios",
                "success": False
            }), 400

        try:
            systolic = float(data['systolic'])
            diastolic = float(data['diastolic'])
        except ValueError as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc)
            return jsonify({
                "message": "Los valores de 'systolic' y 'diastolic' deben ser números",
                "success": False,
                "error": str(ex)
            }), 400

        data = BloodPressureService.create(systolic, diastolic)
        if (data is not None):
            return jsonify({
                "message": "Presión arterial registrada",
                "success": True,
                "data": data
            }), 201
        else:
            return jsonify({
                "message": "Error al registrar la presión arterial",
                "success": False,
            }), 500


@main.route('/predict', methods=['GET'])
def predict():
    systolic = request.args.get('systolic')
    diastolic = request.args.get('diastolic')

    if systolic is None or diastolic is None:
        return jsonify({
            "message": "Los parametros 'systolic' y 'diastolic' son obligatoros",
            "success": False,
        }), 400

    try:
        systolic = float(systolic)
        diastolic = float(diastolic)
    except ValueError as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc)
        return jsonify({
            "message": "Los parametros 'systolic' y 'diastolic' deben ser números",
            "success": False,
            "error": str(ex)
        }), 400

    prediccion = str(BloodPressureService.predict(systolic, diastolic))
    return jsonify({
        "message": "Predicción realizada con éxito",
        "data": {
            "systolic": systolic,
            "diastolic": diastolic,
            "prediction": prediccion
        },
        "success": True
    })
