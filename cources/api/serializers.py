from rest_framework import serializers
from cources.models import Subject
from django.db.models import Count

class SubjectSerializer(serializers.ModelSerializer):
    total_courses = serializers.IntegerField()
    popular_courses = serializers.SerializerMethodField()
    def get_popular_courses(self,obj):
        courses = obj.courses.annotate(total_student = Count('students')).order_by('total_student')[:3]
        return [
            f'{c.title} ({c.total_student})' for c in courses
        ]

    class Meta:
        model = Subject
        fields = ['id','title','slug','total_courses','popular_courses']