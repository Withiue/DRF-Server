from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets

from .models import Post
from .serializers import PostSerializer

#CRUD 구현하기
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        order = request.query_params.get('order')
        if order == 'user':
            queryset = self.filter_queryset(self.get_queryset().order_by('user__email'))
        elif order == 'updated':
            queryset = self.filter_queryset(self.get_queryset().order_by('-updated_at'))
        else:
            queryset = self.filter_queryset(self.get_queryset())
            
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)