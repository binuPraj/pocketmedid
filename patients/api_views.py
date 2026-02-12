from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Patient
from .api_serializers import PatientSerializer

class PatientDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, token):
        # Only allow doctors to access
        if not request.user.groups.filter(name='Doctors').exists():
            return Response({'detail': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        try:
            patient = Patient.objects.get(access_token=token)
        except Patient.DoesNotExist:
            return Response({'detail': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
