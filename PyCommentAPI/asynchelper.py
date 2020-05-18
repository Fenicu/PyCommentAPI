import aiohttp
from PyCommentAPI.apihelper import CommentsApiException
from six import iteritems, text_type
from json import loads

API_URL = "https://api.comments.bot/{0}"

async def _make_request(token: str, method_name: str, session, params=None):
    request_url = API_URL.format(method_name)
    params['api_key'] = token
    result = await session.post(request_url, params=params)
    if result.status != 200:
        msg = f"The server returned HTTP {result.status} {result.reason}. Response body:\n[{await result.text()}]"
        raise CommentsApiException(msg, method_name, result)
    
    try:
        result_json = loads(await result.text())
    except:
        msg = f"The server returned an invalid JSON response. Response body:\n[{await result.text()}]"
        raise CommentsApiException(msg, method_name, result)
    
    if not result_json['ok']:
        msg = f"Error code: {result_json['error']['code']} Description: {result_json['error']['name']}"
        raise CommentsApiException(msg, method_name, result)

    if method_name == 'createPost':
        return AioComments(result_json['result']['post_id'], result_json['result']['link'], token, session)

    elif method_name == 'editPost':
        return AioComments(params['post_id'], f"https://comments.bot/thread/{params['post_id']}", token, session)

    elif method_name == 'deletePost':
        return result_json['ok']

class AioComments:
    def __init__(self, post_id, link, token, _session):
        self.id = post_id
        self.link = link
        self.token = token
        self._session = _session

    async def edit_post(self, text=None, photo_url=None, caption=None, parse_mode=None):
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
        return await _make_request(self.token, method_url, self._session, payload)

    async def delete_post(self):
        method_url = r'deletePost'
        payload = {'post_id': self.id}
        return await _make_request(self.token, method_url, self._session, payload)

    def __str__(self):
        d = {}
        for x, y in iteritems(self.__dict__):
            if hasattr(y, '__dict__'):
                d[x] = y.__dict__
            else:
                d[x] = y

        return text_type(d)