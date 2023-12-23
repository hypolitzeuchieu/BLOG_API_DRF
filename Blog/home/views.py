from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Blog
from .serializers import BlogSerializers
from django.db.models import Q

from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication


class BlogView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))

            serializer = BlogSerializers(blogs, many=True)

            return Response({
                'data': serializer.data,
                'message': 'blogs fetched successfully'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            Response({
                'data': {},
                'message': 'invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializers(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'blog created successfully'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            Response({
                'data': {},
                'message': 'invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            blogs = Blog.objects.filter(uid=data.get('uid'))

            if not blogs.exists():
                return Response({
                    'data': {},
                    'message': 'invalid blog uid'
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blogs[0].user:
                return Response({
                    'data': {},
                    'message': ' you are not authorized to this'
                   }, status=status.HTTP_400_BAD_REQUEST)

            serializer = BlogSerializers(blogs[0], data=data, partial=True)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'
                    }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'blog updated successfully'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)
