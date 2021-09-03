from uuid import uuid4

import aiohttp

from . import base


class Handler(base.Handler):
    def __init__(self, homeserver_url, access_token, room_id, **kwargs):
        super().__init__(**kwargs)
        self.access_token = access_token
        self.url = "%s/_matrix/client/r0/rooms/%s/send/m.room.message" % (
            homeserver_url, room_id,
        )

    async def store(self, entries):
        async with aiohttp.ClientSession() as session:
            data = {
                'msgtype': 'm.notice',
                'body': '{}'.format('\n'.join(entries)),
                'format': 'org.matrix.custom.html',
                'formatted_body': '{}'.format('<br>'.join(entries)),
            }
            # TODO support ratelimits
            async with session.put(
                "%s/%s" % (self.url, str(uuid4())),
                json=data,
                headers={
                    'Authorization': 'Bearer %s' % self.access_token,
                },
            ):
                pass
