from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PerevalAddedSerializer


class SubmitDataView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PerevalAddedSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pereval_added = serializer.save()
                return Response({
                    "status": 200,
                    "message": "успех",
                    "id": pereval_added.id
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "status": 500,
                    "message": f"Ошибка при выполнении операции: {str(e)}",
                    "id": None
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                "status": 400,
                "message": "Bad Request (не корректные данные)",
                "errors": serializer.errors,  # Отслеживаем ошибки сериализатора
                "id": None
            }, status=status.HTTP_400_BAD_REQUEST)
