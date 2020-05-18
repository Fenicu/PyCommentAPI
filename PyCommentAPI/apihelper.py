import requests
from six import iteritems, text_type
from json import loads
API_URL = "https://api.comments.bot/{0}"

def _make_request(token, method_name, params=None):
    """
    Make request to comments.bot
    """
    request_url = API_URL.format(method_name)
    params['api_key'] = token
    result = requests.post(request_url, params=params)

    if result.status_code != 200:
        msg = f"The server returned HTTP {result.status_code} {result.reason}. Response body:\n[{result.text.encode('utf8')}]"
        raise CommentsApiException(msg, method_name, result)
    try:
        result_json  = loads(result.text)
    except:
        msg = f"The server returned an invalid JSON response. Response body:\n[{result.text.encode('utf8')}]"
        raise CommentsApiException(msg, method_name, result)

    if not result_json['ok']:
        msg = f"Error code: {result_json['error']['code']} Description: {result_json['error']['name']}"
        raise CommentsApiException(msg, method_name, result)

    if method_name == 'createPost':
        return Comments(result_json['result']['post_id'], result_json['result']['link'], token)

    elif method_name == 'editPost':
        return Comments(params['post_id'], f"https://comments.bot/thread/{params['post_id']}", token)

    elif method_name == 'deletePost':
        return result_json['ok']
        
class Comments:
    def __init__(self, post_id, link, token):
        self.id = post_id
        self.link = link
        self.token = token

    def edit_post(self, text=None, photo_url=None, caption=None, parse_mode=None):
        method_url = r'editPost'
        payload = {'post_id': self.id}
        if text:
            payload['text'] = text
        if photo_url:
            payload['photo_url'] = photo_url
        if caption:
            payload['caption'] = caption
        if parse_mode:
            payload['parse_mode'] = parse_mode
        return _make_request(self.token, method_url, payload)

    def delete_post(self):
        method_url = r'deletePost'
        payload = {'post_id': self.id}
        return _make_request(self.token, method_url, payload)

    def __str__(self):
        d = {}
        for x, y in iteritems(self.__dict__):
            if hasattr(y, '__dict__'):
                d[x] = y.__dict__
            else:
                d[x] = y

        return text_type(d)

class CommentsApiException(Exception):
    def __init__(self, msg, function_name, result):
        super(CommentsApiException, self).__init__(f"A request to the Comments API was unsuccessful. {msg}")
        self.function_name = function_name
        self.result = result