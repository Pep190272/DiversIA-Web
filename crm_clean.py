
from flask import Flask, jsonify, request, session
import json
import os

# Crear app Flask independiente solo para CRM
crm_app = Flask(__name__)
crm_app.secret_key = os.environ.get("SESSION_SECRET", "crm_secret")

# Datos CRM
CRM_DATA = {
    "companies": [
        {
            "id": 1,
            "nombre_empresa": "Acelerai",
            "email_contacto": "automatizatunegocio@acelerai.eu",
            "telefono": "",
            "sector": "Tecnología",
            "ciudad": "Madrid",
            "created_at": "2024-12-15T10:00:00"
        }
    ],
    "contacts": [],
    "job_offers": [],
    "employees": [],
    "tasks": []
}

@crm_app.route("/api/companies-crm")
def get_companies():
    return jsonify(CRM_DATA.get("companies", []))

@crm_app.route("/api/contacts-crm") 
def get_contacts():
    return jsonify(CRM_DATA.get("contacts", []))

@crm_app.route("/api/offers-crm")
def get_offers():
    return jsonify(CRM_DATA.get("job_offers", []))

@crm_app.route("/api/employees-crm")
def get_employees():
    return jsonify(CRM_DATA.get("employees", []))

@crm_app.route("/api/tasks-crm")
def get_tasks():
    return jsonify(CRM_DATA.get("tasks", []))

if __name__ == "__main__":
    crm_app.run(port=5001, debug=True)
