from rest_framework import generics
from django.db.models import Count
from cources.models import Subject
from cources.api.serializers import SubjectSerializer
from cources.api.pagination import StandartPagination


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandartPagination
        


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer




