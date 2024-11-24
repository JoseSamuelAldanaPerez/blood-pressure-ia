# API Presión arterial con IA

## Instalación

Creación del entorno virtual (usar Python 3.12):

```bash
python -m venv venv
```

Activar el entorno virtual:

```bash
./venv/Scripts/activate
```

Instalar dependencias:

```bash
pip install -r requeriments.txt
```

Ejecutar:

```bash
python run.py
```

## Uso

Realizar una predicción de anomalia:
[http://127.0.0.1:5000/api/blood_pressure/predict?systolic=120&diastolic=80](http://127.0.0.1:5000/api/blood_pressure/predict?systolic=120&diastolic=80)

El resultado debería ser cercano a 1 si se considera una lectura de presión arterial anormal.