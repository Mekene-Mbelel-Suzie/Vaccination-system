from rest_framework import serializers
from .models import Users, Parent, Role, Hospital

# ======================
# PARENT SIGNUP SERIALIZER
# ======================
class ParentSignupSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    hospital_name = serializers.CharField(required=False)  # optional

    def create(self, validated_data):
        # Get or create parent role
        role, _ = Role.objects.get_or_create(name="parent")

        # Create user
        user = Users.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=role
        )

        # Look up hospital by name (case-insensitive)
        hospital_name = validated_data.get('hospital_name')
        hospital = None
        if hospital_name:
           hospital = Hospital.objects.filter(hospital_name__iexact=hospital_name).first()
        if not hospital:
          raise serializers.ValidationError(f"Hospital '{hospital_name}' does not exist")

        # Create Parent profile
        Parent.objects.create(
            users=user,
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
            hospital=hospital
        )

        return user

# ======================
# PARENT LOGIN SERIALIZER
# ======================
class ParentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Check for parent role
        try:
            role = Role.objects.get(name="parent")
        except Role.DoesNotExist:
            raise serializers.ValidationError("Parent role not found")

        # Get user
        try:
            user = Users.objects.get(email=email, role=role)
        except Users.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        # Check password
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data

# ======================
# OPTIONAL: Parent Serializer for returning info
# ======================
class ParentSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='users.email', read_only=True)
    hospital_name = serializers.CharField(source='hospital.hospital_name', read_only=True)

    class Meta:
        model = Parent
        fields = ['full_name', 'phone_number', 'address', 'hospital_name', 'email']