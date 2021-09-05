from rest_auth.registration.views import RegisterView
from rest_framework import generics
from users.models import CustomUser
from users.serializers import CustomSerializer, ProfileSerializer


class CustomRegisterView(RegisterView):
    serializer_class = CustomSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        custom_data = {"message": "some message", "status": "ok"}
        response.data.update(custom_data)
        return response


class ProfileView(generics.RetrieveAPIView):
    model = CustomUser
    queryset = CustomUser.objects.values('id', 'first_name')
    serializer_class = ProfileSerializer
