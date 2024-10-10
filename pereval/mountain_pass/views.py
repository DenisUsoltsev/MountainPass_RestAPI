from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView

from .models import PerevalAdded
from .serializers import PerevalAddedSerializer, PerevalDetailSerializer


class PerevalCreateView(CreateAPIView):
    serializer_class = PerevalAddedSerializer

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


class PerevalDetailView(RetrieveAPIView):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalDetailSerializer

    def get(self, request, *args, **kwargs):
        pereval = self.get_object()  # Используем наш переопределенный метод
        if pereval is None:
            return Response({
                "status": 404,
                "message": "Перевал не найден.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(pereval)
        return Response({
            "status": 200,
            "message": "успех",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class PerevalUpdateView(UpdateAPIView):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer

    def patch(self, request, *args, **kwargs):
        pereval = self.get_object()

        # Проверяем статус
        if pereval.status != 'new':
            return Response({
                "state": 0,
                "message": "Редактирование доступно только для записей со статусом 'new'."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Получаем сериализатор с данными запроса
        serializer = self.get_serializer(pereval, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "state": 1,
            "message": "Запись успешно отредактирована."
        }, status=status.HTTP_200_OK)