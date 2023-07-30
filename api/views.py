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


class SerialNumberDetailView(APIView):
    def get(self, request, number):
        serial_number = SerialNumber.objects.get(number=number)
        ser = SerialNumberSerializer(instance=serial_number, context={'request': request})
        return Response(ser.data)


class ConfirmationCodesView(APIView):
    def get(self, request):
        confirmation_code = ConfirmationCode.objects.all()
        ser = ConfirmationCodeSerializer(instance=confirmation_code, many=True)
        return Response(data=ser.data)


# class CreateCodeView(APIView):
#     # permission_classes = [IsAuthenticated, IsAdminUser]
#     def get(self, request, number):
#         serial_num_code = SerialNumber.objects.get(number=number).code
#         serializer = ConfirmationCodeSerializer(instance=serial_num_code, many=False)
#         return Response(serializer.data)
#
#     def post(self, request, number):
#         serial_number = SerialNumber.objects.get(number=number)
#         serializer = ConfirmationCodeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data['serial_number'] = serial_number
#             serializer.save()
#             return Response({"response": "created"}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateCodeView(APIView):
    def post(self, request):
        try:
            serial_number = SerialNumber.objects.get(number=request.data['serial_number'])
            if serial_number.payed:
                return Response({"response": "the serial number has an code"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = ConfirmationCodeSerializer(data=request.data)
                if serializer.is_valid():
                    confirmation_code = serializer.save(serial_number=serial_number)
                    return Response(ConfirmationCodeSerializer(confirmation_code).data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SerialNumber.DoesNotExist:
            return Response({"response": "serial number does not exist"}, status=status.HTTP_400_BAD_REQUEST)
