QuickStart
==========

このページでは Mi.pyの簡単な使い方をご紹介します

.. tip::
    Mi.pyはリリースが遅いため、githubからインストールすることを推奨します


.. code-block:: bash

    pip install mi.py # stable
    pip install git+git+https://github.com/yupix/Mi.py.git # unstable


簡単なコードを書いてみると以下のようになります

.. code-block:: python

    import asyncio

    from mi.ext import commands
    from mi.note import Note
    from mi.router import Router

    class MyBot(commands.Bot):
        def __init__(self):
            super().__init__('tu!')
        
        async def on_ready(self, ws):
            print(f'Connecting {self.i.username}')
            await Router(ws).connect_channel(['global', 'main'])
        
        
        async def on_message(self, note: Note):
            print(f'{note.author.username}: {note.content}')

    if __name__ == '__main__':
        bot = MyBot()
        asyncio.run(bot.start('wss:example.com/streaming', 'your token'))
