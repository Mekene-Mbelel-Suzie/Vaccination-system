from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .serializers import ParentSignupSerializer, ParentLoginSerializer

# ======================
# PARENT SIGNUP
# ======================
class ParentSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ParentSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Parent signup successful ✅"},
            status=status.HTTP_201_CREATED
        )


# ======================
# PARENT LOGIN
# ======================
@method_decorator(csrf_exempt, name='dispatch')  # allows Flutter POST without CSRF
class ParentLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ParentLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                "message": "Parent login successful ✅",
                "email": user.email,
                "id": user.id,
                "role": user.role.name
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)