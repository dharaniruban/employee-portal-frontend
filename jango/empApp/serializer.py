from rest_framework import serializers
from empApp.models import Departments, Employees
from datetime import datetime

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ('DepartmentId', 'DepartmentName', 'is_active', 'CreatedAt', 'UpdatedAt')
        read_only_fields = ('CreatedAt', 'UpdatedAt', 'DepartmentId')

class EmployeeSerializer(serializers.ModelSerializer):
    PhotoURL = serializers.SerializerMethodField()
    DepartmentName = serializers.CharField(source='Department.DepartmentName', read_only=True)
    DepartmentId = serializers.IntegerField(source='Department.DepartmentId', read_only=True)

    class Meta:
        model = Employees
        fields = (
            'EmployeeId',
            'EmployeeName',
            'Email',
            'Department',
            'DepartmentId',
            'DepartmentName',
            'DateOfJoining',
            'PhotoFileName',
            'PhotoURL',
            'is_active',
            'CreatedAt',
            'UpdatedAt'
        )
        read_only_fields = ('CreatedAt', 'UpdatedAt', 'EmployeeId')

    def get_PhotoURL(self, obj):
        request = self.context.get('request')
        photo_url = obj.PhotoFileName or 'default.png'
        if request is not None:
            return request.build_absolute_uri('/photos/' + photo_url)
        return '/photos/' + photo_url

    def to_internal_value(self, data):
        if 'DateOfJoining' in data:
            try:
                if '/' in data['DateOfJoining']:
                    day, month, year = map(int, data['DateOfJoining'].split('/'))
                    data['DateOfJoining'] = f'{year}-{month:02d}-{day:02d}'
            except:
                raise serializers.ValidationError({"DateOfJoining": "Use DD/MM/YYYY or YYYY-MM-DD format"})
        return super().to_internal_value(data)