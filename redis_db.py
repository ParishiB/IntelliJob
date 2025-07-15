import redis

r = redis.Redis(host='localhost', port=6379, db=0)


def set_user_id(user_id):
    r.set('user_id', user_id)

def get_user_id():
    return r.get('user_id')

def clear_user_id():
    r.delete('user_id')