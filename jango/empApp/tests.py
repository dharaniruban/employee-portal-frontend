from django.test import TestCase, Client
from rest_framework import status
from empApp.models import Departments, Employees
from empApp.serializer import DepartmentSerializer, EmployeeSerializer
import json
from datetime import date, timedelta

class DepartmentAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.department_data = {
            'DepartmentName': 'Engineering'
        }
        self.department = Departments.objects.create(**self.department_data)

    def test_get_all_departments(self):
        response = self.client.get('/department/')
        departments = Departments.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], serializer.data)

    def test_create_department(self):
        response = self.client.post(
            '/department/',
            data=json.dumps({'DepartmentName': 'Marketing'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['message'], 'Added Successfully')

    def test_create_duplicate_department(self):
        response = self.client.post(
            '/department/',
            data=json.dumps({'DepartmentName': 'Engineering'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('DepartmentName', response.json())

    def test_get_single_department(self):
        response = self.client.get(f'/department/{self.department.DepartmentId}/')
        serializer = DepartmentSerializer(self.department)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_update_department(self):
        response = self.client.put(
            f'/department/{self.department.DepartmentId}/',
            data=json.dumps({'DepartmentName': 'Updated Engineering'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Updated Successfully')

    def test_delete_department(self):
        response = self.client.delete(f'/department/{self.department.DepartmentId}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Deleted Successfully')

class EmployeeAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.department = Departments.objects.create(DepartmentName='Engineering')
        self.employee_data = {
            'EmployeeName': 'John Doe',
            'Email': 'john.doe@example.com',
            'Department': self.department.DepartmentId,
            'DateOfJoining': '2023-01-01',
            'PhotoFileName': 'default.png'
        }
        self.employee = Employees.objects.create(**self.employee_data)

    def test_get_all_employees(self):
        response = self.client.get('/employee/')
        employees = Employees.objects.all()
        serializer = EmployeeSerializer(employees, many=True, context={'request': None})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], serializer.data)

    def test_create_employee(self):
        response = self.client.post(
            '/employee/',
            data=json.dumps({
                'EmployeeName': 'Jane Doe',
                'Email': 'jane.doe@example.com',
                'Department': self.department.DepartmentId,
                'DateOfJoining': '2023-02-01',
                'PhotoFileName': 'jane.png'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['message'], 'Added Successfully')

    def test_create_employee_future_date(self):
        future_date = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
        response = self.client.post(
            '/employee/',
            data=json.dumps({
                'EmployeeName': 'Jane Doe',
                'Email': 'jane.doe@example.com',
                'Department': self.department.DepartmentId,
                'DateOfJoining': future_date,
                'PhotoFileName': 'jane.png'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('DateOfJoining', response.json())