from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from django.core.files.storage import default_storage
from empApp.models import Departments, Employees
from empApp.serializer import DepartmentSerializer, EmployeeSerializer
import os
import uuid
from django.core.exceptions import ValidationError
import mimetypes
import logging
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

# Set up logging
logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class DepartmentAPIView(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request, id=None):
        if id:
            try:
                department = Departments.objects.get(DepartmentId=id)
                serializer = DepartmentSerializer(department, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Departments.DoesNotExist:
                return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        departments = Departments.objects.all()  # Uses ActiveManager to filter is_active=True
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(departments, request)
        serializer = DepartmentSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data.pop('DepartmentId', None)
        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Added Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            department = Departments.objects.get(DepartmentId=id)
        except Departments.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        try:
            department = Departments.all_objects.get(DepartmentId=id)  # Use all_objects to include soft-deleted
            serializer = DepartmentSerializer(department, data={'is_active': False}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Soft Deleted Successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Departments.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

class EmployeeAPIView(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request, id=None):
        if id:
            try:
                employee = Employees.objects.get(EmployeeId=id)
                serializer = EmployeeSerializer(employee, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Employees.DoesNotExist:
                return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        employees = Employees.objects.all()  # Uses ActiveManager to filter is_active=True
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(employees, request)
        serializer = EmployeeSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Added Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            employee = Employees.objects.get(EmployeeId=id)
        except Employees.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        try:
            employee = Employees.all_objects.get(EmployeeId=id)  # Use all_objects to include soft-deleted
            serializer = EmployeeSerializer(employee, data={'is_active': False}, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Soft Deleted Successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employees.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

class EmployeeReportAPIView(APIView):
    def get(self, request):
        try:
            # Aggregate employee count by department, only for active employees
            report_data = Employees.objects.filter(is_active=True).values('Department__DepartmentName').annotate(count=Count('EmployeeId')).order_by('Department__DepartmentName')
            labels = [item['Department__DepartmentName'] for item in report_data]
            data = [item['count'] for item in report_data]
            return Response({'labels': labels, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error generating employee report: {str(e)}")
            return Response({"error": "Failed to generate report"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def SaveFile(request):
    if 'file' not in request.FILES:
        logger.error("No file provided in request")
        return JsonResponse({"error": "No file provided"}, status=400)
    
    file = request.FILES['file']
    allowed_types = ['image/jpeg', 'image/png', 'image/gif']
    mime_type, _ = mimetypes.guess_type(file.name)
    if mime_type not in allowed_types:
        logger.error(f"Invalid file type: {mime_type}")
        return JsonResponse({"error": "Invalid file type. Only JPEG, PNG, and GIF are allowed."}, status=400)
    
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        logger.error(f"File size exceeds limit: {file.size} bytes")
        return JsonResponse({"error": "File size exceeds 5MB limit."}, status=400)
    
    ext = os.path.splitext(file.name)[1]
    unique_name = f"{uuid.uuid4()}{ext}"  # Save directly to Photos/
    try:
        file_name = default_storage.save(unique_name, file)
        logger.info(f"File saved successfully: {file_name}")
        return JsonResponse({
            "file_name": file_name,
            "url": request.build_absolute_uri('/Photos/' + file_name)
        }, status=200)
    except Exception as e:
        logger.error(f"Failed to save file: {str(e)}")
        return JsonResponse({"error": f"Failed to save file: {str(e)}"}, status=500)

def home(request):
    return JsonResponse({"message": "Welcome to the Employee Management API."})