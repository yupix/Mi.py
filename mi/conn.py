from mi import config
from mi.utils import api


def get_user(user_id: str, username: str, host: str = None) -> dict:
    data = {'userId': user_id, 'username': username, 'host': host}
    return api(config.i.origin_uri, '/api/users/show', json_data=data).json()
