from rest_framework import generics,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.shortcuts import get_object_or_404
from cources.models import Subject,Course
from cources.api.serializers import SubjectSerializer,CourseSerializer
from cources.api.pagination import StandartPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandartPagination


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandartPagination



class CourseEnrollView(APIView):
    authentication_classes = [BasicAuthentication]
    def post(self,request,pk,format=None):
        course = get_object_or_404(Course,pk=pk)
        course.students.add(request.user)
        return Response({'enrolled':True})


