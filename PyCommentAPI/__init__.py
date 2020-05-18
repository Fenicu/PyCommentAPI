from PyCommentAPI import apihelper, asynchelper
import aiohttp, asyncio

class Comments:
    def __init__(self, token, owner=None):
        self.token = token
        self.owner = owner

    def create_post(self, type, owner_id=None, text=None, photo_url=None,
            caption=None, parse_mode=None, administrators=None, disable_notifications=None):
        method_url = r'createPost'
        if not owner_id:
            owner_id = self.owner
        payload = {'owner_id': str(owner_id), 'type': type}
        if text:
            payload['text'] = text
        if photo_url:
            payload['photo_url'] = photo_url
        if caption:
            payload['caption'] = caption
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if administrators:
            payload['administrators'] = administrators
        if disable_notifications:
            payload['disable_notifications'] = disable_notifications
        return apihelper._make_request(self.token, method_url, payload)

    def edit_post(self, post_id, text=None, photo_url=None, caption=None, parse_mode=None):
        method_url = r'editPost'
        payload = {'post_id': post_id}
        if text:
            payload['text'] = text
        if photo_url:
            payload['photo_url'] = photo_url
        if caption:
            payload['caption'] = caption
        if parse_mode:
            payload['parse_mode'] = parse_mode
        return apihelper._make_request(self.token, method_url, payload)

    def delete_post(self, post_id):
        method_url = r'deletePost'
        payload = {'post_id': post_id}
        return apihelper._make_request(self.token, method_url, payload)

class AioComments:
    def __init__(self, token, owner=None):
        self.token = token
        self.owner = owner
        self.session = aiohttp.ClientSession()

    async def create_post(self, type, owner_id=None, text=None, photo_url=None,
            caption=None, parse_mode=None, administrators=None, disable_notifications=None):
        method_url = r'createPost'
        if not owner_id:
            owner_id = self.owner
        payload = {'owner_id': str(owner_id), 'type': type}
        if text:
            payload['text'] = text
        if photo_url:
            payload['photo_url'] = photo_url
        if caption:
            payload['caption'] = caption
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if administrators:
            payload['administrators'] = administrators
        if disable_notifications:
            payload['disable_notifications'] = disable_notifications
        return await asynchelper._make_request(self.token, method_url, self.session, payload)

    async def edit_post(self, post_id, text=None, photo_url=None, caption=None, parse_mode=None):
        method_url = r'editPost'
        payload = {'post_id': post_id}
        if text:
            payload['text'] = text
        if photo_url:
            payload['photo_url'] = photo_url
        if caption:
            payload['caption'] = caption
        if parse_mode:
            payload['parse_mode'] = parse_mode
        return await asynchelper._make_request(self.token, method_url, self.session, payload)

    async def delete_post(self, post_id):
        method_url = r'deletePost'
        payload = {'post_id': post_id}
        return await asynchelper._make_request(self.token, method_url, self.session, payload)

    async def close(self):
        await self.session.close()
