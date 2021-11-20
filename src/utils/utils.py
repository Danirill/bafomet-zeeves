import string
from random import choice

from django.contrib.auth.hashers import make_password

from api.v1.users.serializers import UserSerializer
from api.v1.users.models import User

def get_user(request):
    user_id = UserSerializer(request.user).data['id']
    user = User.objects.get(id=user_id)
    return user

def validate_password(self, value: str) -> str:
    """
    Hash value passed by user.
    :param value: password of a user
    :return: a hashed version of the password
    """
    return make_password(value)


def get_token(length=15, only_digits=False):
    rand_str = lambda n: ''.join([choice(string.ascii_lowercase) for i in range(n)])
    if only_digits:
        rand_str = lambda n: ''.join([choice(string.digits) for i in range(n)])
    set_id = rand_str(length)
    return set_id

def parse_int(s, base=10, val=None):
    try:
        a = int(s, base)
        return a
    except:
        return val


def parse_bool(s, val=False):
    try:
        if s.lower() in ['true', '1', 't', 'y', 'yes']:
            return True
        if s.lower() in ['false', '0', 'n', 'no']:
            return False
    except:
        return val