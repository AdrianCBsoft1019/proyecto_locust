from flask import Flask, jsonify
from celery.result import AsyncResult
from tareas import procesar_pago, celery_app

app = Flask(__name__)


@app.route("/health")
def health():
    return "OK", 200


@app.route("/comprar-ticket", methods=["POST"])
def comprar_ticket():
    tarea = procesar_pago.delay()
    return jsonify({"task_id": tarea.id}), 202


@app.route("/estado-compra/<task_id>")
def estado_compra(task_id):
    r = AsyncResult(task_id, app=celery_app)
    return jsonify({"task_id": task_id, "estado": r.state})