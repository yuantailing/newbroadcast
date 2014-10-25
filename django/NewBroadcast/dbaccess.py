from NewBroadcast.models import *

def user_new():
    return User()

def user_get(p_id):
    return User.objects.get(id=p_id)

def user_list():
    return User.ojbects.all()

def user_del(p_id):
    User.objects.get(id=p_id).delete()

