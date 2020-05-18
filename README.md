# <p align="center">PyCommentAPI

<p align="center">A simple, but extensible Python implementation for the <a href="https://telegra.ph/Comments-API-11-29">comments.bot API</a>.


  * [Getting started.](#getting-started)
  * [Writing your first comments bot](#writing-your-first-comments-bot)

## Getting started.

This API is tested with Python 3.7.3
You need to put the library in the project folder.
```
$ git clone https://github.com/Feno4ka/PyCommentAPI.git
```
or install from PyPi
```
$ python -m pip install PyCommentAPI
```

## Writing your first comments bot
```python
from PyCommentAPI import Comments

postbot = Comments(token=TOKEN, owner=TELEGRAM_USER_ID)
# or postbot = Comments(TOKEN)

out = '''
<b>Hi!</b>
This is the first test of this library!
<a href="https://t.me/Fenicu">Fenicu</a>
'''

post = postbot.create_post('text', text=out, parse_mode='HTML')
# or post = postbot.create_post(owner_id=TELEGRAM_USER_ID, type='text', text=out, parse_mode='HTML')
print(post.link)
print(post.id)

out = '''
<b>Post changed!</b>
'''
post.edit_post(text=out, parse_mode='HTML')
# or post = postbot.edit_post(post.id, out, parse_mode='HTML')
post.delete_post()
# or postbot.delete_post(post.id)
```

## Or do you need an asynchronous version?

```python
import asyncio

import PyCommentAPI

bot = PyCommentAPI.AioComments(token=TOKEN, owner=TELEGRAM_USER_ID)

async def NewPost(text):
    try:
        post = await bot.create_post('text', text=text, parse_mode='HTML')
        print(post.link)
    except PyCommentAPI.apihelper.CommentsApiException as error:
        print(error)

async def ClientClose():
    await bot.close()

if __name__ == "__main__":
    out = "Hello, <b>Oak</b>!!"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(out))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ClientClose())
```

|func|argument(s)|
|:---:|---|
|create_post|`owner_id` = telegram user id, `type` = photo or text, `text` = some text, `photo_url` = photo url, `caption` = photo caption, `parse_mode` = HTML or markdown, `administrators` = list admins, disable_notifications = `true` if you want to disable notifications about new comments for all admins of the post|
|edit_post|`post_id` = your post id, `text` = some text, `photo_url` = photo url, `caption` = photo caption, `parse_mode` = HTML or markdown,|
|delete_post|`post_id` = your post id|