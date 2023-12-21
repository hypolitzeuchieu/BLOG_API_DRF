from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializers
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
