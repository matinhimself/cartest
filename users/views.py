from rest_auth.registration.views import RegisterView

from users.serializers import CustomSerializer


class CustomRegisterView(RegisterView):
    serializer_class = CustomSerializer
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        custom_data = {"message": "some message", "status": "ok"}
        response.data.update(custom_data)
        return response