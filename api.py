import datetime
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os


# Initialize the Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

# Define the database model
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    eid = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(30), nullable=False)
    pswd = db.Column(db.String(30), nullable=False)
    active_time = db.Column(db.Integer, nullable=True)
    key = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    desigination = db.Column(db.String(30), nullable=False)
    department = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)

    def __init__(self,email,pswd,dob,phno,desigination,department,name):
        self.uid,self.eid = self.__generate_unique_ids()
        self.key = self.generate_unique_hex(16)
        self.email = email
        self.pswd = pswd
        self.status = False
        self.dob=dob
        self.phone=phno
        self.desigination=desigination
        self.department=department
        self.name = name

    def __generate_unique_ids(self):
        while True:
            eid = self.generate_unique_hex(16)
            uid = self.generate_unique_hex(7)
            if not db.session.query(Employee).filter_by(eid=eid).first() and not db.session.query(Employee).filter_by(uid=uid).first():
                return eid, uid

    def generate_unique_hex(self,num):        
        byte_array = os.urandom(num)
        # Convert the byte array to a hex string
        hex_string = ''.join([format(byte, '02x') for byte in byte_array])
        return hex_string
# Create the API routes
@app.route('/api/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify({
        'employee_id': employee.id,
        'uid': employee.uid,
        'key': employee.key,
        'e-mail': employee.email,
        'pswd': employee.pswd,
        'eid': employee.eid,
        'name':employee.name
    })

@app.route('/api/employees/login', methods=['POST'])
def login_employee():
    email = request.json['email']
    pswd = request.json['pswd']
    employee = Employee.query.filter_by(email=email, pswd=pswd).first()
    if employee:
        return jsonify({
            'message': 'Login successful',
            'name': employee.name,
            'employee_id': employee.eid,
            'uid': employee.uid,
            'key': employee.key,
            'email': employee.email,
            'status': employee.status,
            'dob': employee.dob,
            'phone': employee.phone,
            'desigination': employee.desigination,
            'department': employee.department
        })
    else:
        return jsonify({'message': 'Invalid credentials'})

@app.route('/api/employees/get_key', methods=['POST'])
def update_key():
    eid=request.json['eid']
    employee = Employee.query.filter_by(eid=eid).first()
    employee.key = employee.generate_unique_hex(16)
    print(employee.key)
    if employee:
        return jsonify({'key': employee.key})
    else:
        return jsonify({'message': 'Invalid UID'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()  # Create the SQLite database and tables

        # Generate test data
        test_employees = []
        for i in range(10):
            test_employees.append(
                Employee(
                    email=f'test_email_{i}@example.com',
                    pswd='test_password',
                    dob = datetime.date(1990, 1, 1),
                    phno = 1234567890,
                    desigination='Software Engineer',
                    department='Engineering',
                    name=f'Test Employee {i}'
                )
            )

        # Add test data to the database
        for employee in test_employees:
            db.session.add(employee)
        db.session.commit()
    app.run(host='0.0.0.0', port=8080,debug=True)
