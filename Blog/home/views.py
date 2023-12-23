from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializers

from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication


class BlogView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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