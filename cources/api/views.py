from rest_framework import generics,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.shortcuts import get_object_or_404
from cources.models import Subject,Course
from cources.api.serializers import SubjectSerializer,CourseSerializer,CourseWithContentsSerializer
from cources.api.pagination import StandartPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action





class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandartPagination


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandartPagination
    @action(
        detail=True,
        methods=['post'],
        authentication_classes = [BasicAuthentication],
        permission_classes = [IsAuthenticated]
    )
    def enroll(self,request,pk,format=None):
        course = get_object_or_404(Course,pk=pk)
        course.students.add(request.user)
        return Response({'enrolled':True})

    @action(
        detail = True,
        methods=['get'],
        serializer_class = CourseWithContentsSerializer,
        authentication_classes = [BasicAuthentication],
        permission_classes = [IsAuthenticated] )
    def contents(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

# class CourseEnrollView(APIView):
#     authentication_classes = [BasicAuthentication]
#     def post(self,request,pk,format=None):
#         course = get_object_or_404(Course,pk=pk)
#         course.students.add(request.user)
#         return Response({'enrolled':True})


