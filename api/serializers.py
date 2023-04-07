from rest_framework import serializers
from account.models import User, Plan, ConfirmationCode, SerialNumber, Opt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'full_name',
            'phone',
        )


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    serial_number = serializers.SlugRelatedField(slug_field='number', read_only=True)

    class Meta:
        model = ConfirmationCode
        fields = (
            'id', 'serial_number', 'code',
            'expiry', 'activation_date',
        )


class SerialNumberSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='full_name', read_only=True)
    # code = serializers.SerializerMethodField()
    code = ConfirmationCodeSerializer(many=False)

    class Meta:
        model = SerialNumber
        fields = (
            'id', 'number', 'user',
            'created_at', 'days_charge', 'code'
        )

    # def create(self, validated_data):
    #     """
    #     Overriding the default create method of the Model serializer.
    #     :param validated_data: data containing all the details of student
    #     :return: returns a successfully created student record
    #     """
    #     user_data = validated_data.pop('user')
    #     user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    #     student, created = UnivStudent.objects.update_or_create(user=user,
    #                         subject_major=validated_data.pop('subject_major'))
    #     return student


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            'id', 'title', 'price', 'days',
        )
