from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .serializers import SerialNumberSerializer, ConfirmationCodeSerializer, UserSerializer, PlanSerializer
from account.models import User, Plan, ConfirmationCode, SerialNumber, Opt


class SerialNumbersView(APIView):
    def get(self, request):
        serial_numbers = SerialNumber.objects.all()
        ser = SerialNumberSerializer(instance=serial_numbers, many=True)
        return Response(data=ser.data)


class ConfirmationCodesView(APIView):
    def get(self, request):
        confirmation_code = ConfirmationCode.objects.all()
        ser = ConfirmationCodeSerializer(instance=confirmation_code, many=True)
        return Response(data=ser.data)
