from datetime import datetime
import requests
import random
import string
from flask import Flask, jsonify
from api import app, db  # Import your Flask app and database instance
from api import Employee  # Import your model(s)

# Function to generate a random string of characters
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Function to generate a random email address
def generate_random_email():
    domain = ["gmail.com", "yahoo.com", "hotmail.com", "example.com"]
    return generate_random_string(8) + "@" + random.choice(domain)

# Function to generate random phone number
def generate_random_phone():
    return ''.join(random.choice(string.digits) for _ in range(10))

# Function to generate random date of birth
def generate_random_dob():
    start_date = datetime(1970, 1, 1)
    end_date = datetime(2000, 1, 1)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d")

# Function to generate random designation and department
def generate_random_designation_department():
    designations = ["Manager", "Developer", "Designer", "Tester"]
    departments = ["HR", "IT", "Finance", "Marketing"]
    return random.choice(designations), random.choice(departments)

# Function to generate test data and add it to the database
def generate_test_data(num_employees):
    url = 'http://localhost:8080/api/employees'
    for _ in range(num_employees):
        email = generate_random_email()
        password = generate_random_string(8)
        dob = generate_random_dob()
        phone = generate_random_phone()
        designation, department = generate_random_designation_department()
        name = generate_random_string(8)
        data = {
            'email': email,
            'pswd': password,
            'dob': dob,
            'phno': phone,
            'desigination': designation,
            'department': department,
            'name': name
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Employee added: {email}")
        else:
            print(f"Failed to add employee: {email}")

if __name__ == "__main__":
    with app.app_context():
        employees = Employee.query.all()  # Fetch all employees
        generate_test_data(10)  # Generate 10 test employees
