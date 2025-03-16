from flask import Flask, jsonify
from api import app, db  # Import your Flask app and database instance
from api import Employee  # Import your model(s)

with app.app_context():
    employees = Employee.query.all()  # Fetch all employees

    # Print database entries
    for employee in employees:
        print(employee.id, employee.uid, employee.eid, employee.email, employee.pswd, employee.key)

