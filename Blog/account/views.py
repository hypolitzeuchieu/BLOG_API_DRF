from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializers, LoginSerializer
from rest_framework import status


class Registerview(APIView):

    def post(self, request):
        try:
            data = request.data
            serialiser = RegisterSerializers(data=data)

            if not serialiser.is_valid():
                return Response({
                    'data': serialiser.errors,
                    'message': 'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serialiser.save()
            return Response({
                'data': {},
                'message': 'your account is created'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'invalid data'
                }, status=status.HTTP_400_BAD_REQUEST)

            response = serializer.get_jwt_token(serializer.data)
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'something went wrong'
            })
