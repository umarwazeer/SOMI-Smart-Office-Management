from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    password_confirm = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "phone",
        ]

    def validate_email(self, value):
        value = value.strip().lower()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": "Passwords do not match."
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")

        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)

        user.role = User.Role.EMPLOYEE
        user.is_active = True
        user.is_active_account = True

        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid username or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive."
            )

        if not user.is_active_account:
            raise serializers.ValidationError(
                "This account has been disabled."
            )

        attrs["user"] = user

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "profile_picture",
            "is_active",
            "is_active_account",
            "date_joined",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "role",
            "is_active",
            "is_active_account",
            "date_joined",
            "created_at",
        ]


class UserManagementSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8
    )

    password_confirm = serializers.CharField(
        write_only=True,
        required=False
    )

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "phone",
            "profile_picture",
            "is_active",
            "is_active_account",
            "password",
            "password_confirm",
            "date_joined",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "full_name",
            "date_joined",
            "created_at",
        ]

    def get_full_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()

        return full_name or obj.username

    def validate_username(self, value):
        value = value.strip()

        queryset = User.objects.filter(
            username__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value

    def validate_email(self, value):
        value = value.strip().lower()

        queryset = User.objects.filter(
            email__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if password or password_confirm:
            if not password or not password_confirm:
                raise serializers.ValidationError({
                    "password_confirm": (
                        "Both password fields are required."
                    )
                })

            if password != password_confirm:
                raise serializers.ValidationError({
                    "password_confirm": "Passwords do not match."
                })

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm", None)

        password = validated_data.pop("password", None)

        user = User(**validated_data)

        if password:
            user.set_password(password)

        user.save()

        return user

    def update(self, instance, validated_data):
        validated_data.pop("password_confirm", None)

        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance