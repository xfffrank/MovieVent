from django.contrib.auth.models import User

class EmailBackend(object):

    def authenticate(self, request, **credentials):
        email = credentials.get('email', credentials.get('username'))
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                return user

    def get_user(self, user_id):
        # 该方法是必须的吗
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None