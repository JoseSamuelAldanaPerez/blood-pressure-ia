import traceback
# from tensorflow.keras.models import load_model
import numpy as np
import joblib
from src.database.db import get_db
from src.utils.Logger import Logger

# modelo = load_model('tensorflow/saved_model/')
# modelo = load_model('tensorflow/blood_pressure.h5')
# modelo = load_model('tensorflow/blood_pressure.keras')
scaler = joblib.load('tensorflow/scaler.pkl')


class BloodPressureService():
    @classmethod
    def get_by_id(cls, id):
        try:
            connection = get_db()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM blood_pressure WHERE id = ?', (id,))
            row = cursor.fetchone()
            return {
                "id": row["id"],
                "systolic": row["systolic"],
                "diastolic": row["diastolic"],
                "created_at": row["created_at"],
                "anomaly": row["anomaly"]
            }
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc)
        finally:
            connection.close()

    @classmethod
    def get_all(cls, limit=10):
        try:
            connection = get_db()
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM blood_pressure ORDER BY id desc LIMIT ?;', (limit,))
            resulset = cursor.fetchall()
            rows = []
            for row in resulset:
                rows.append({
                    "id": row["id"],
                    "systolic": row["systolic"],
                    "diastolic": row["diastolic"],
                    "created_at": row["created_at"],
                    "anomaly": row["anomaly"]
                })
            return rows
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc)
        finally:
            connection.close()

    @classmethod
    def create(cls, systolic, diastolic, anomaly):
        id = 0
        try:
            connection = get_db()
            cursor = connection.cursor()
            cursor.execute('''
                    INSERT INTO blood_pressure (systolic, diastolic, anomaly)
                    VALUES (?, ?, ?)
                ''', (systolic, diastolic, anomaly))
            connection.commit()
            id = cursor.lastrowid
            return cls.get_by_id(id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc)
        finally:
            connection.close()

    @classmethod
    def predict(cls, systolic, diastolic):
        lecturas = np.array([[systolic, diastolic]])
        lecturas_escaladas = scaler.transform(lecturas)
        # prediccion = modelo.predict(lecturas_escaladas).tolist()
        # print(predicciones)
        # return pediccion[0][0]
        return lecturas_escaladas
