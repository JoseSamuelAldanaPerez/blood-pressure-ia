import traceback
from src.database.db import get_db
from src.utils.Logger import Logger


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
                "created_at": row["created_at"]
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
                    "created_at": row["created_at"]
                })
            return rows
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc)
        finally:
            connection.close()

    @classmethod
    def create(cls, systolic, diastolic):
        id = 0
        try:
            connection = get_db()
            cursor = connection.cursor()
            cursor.execute('''
                    INSERT INTO blood_pressure (systolic, diastolic)
                    VALUES (?, ?)
                ''', (systolic, diastolic))
            connection.commit()
            id = cursor.lastrowid
            return cls.get_by_id(id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc)
        finally:
            connection.close()
