.. currentmodule:: mi

API Reference
===============

このセクションではMi.pyのAPIについて説明します

.. note::
   このライブラリではloggingを用いてdebug出力が可能です。標準設定では出ないため、起動時の引数として `debug` を渡すようにしてください

イベントリファレンス
--------------------

.. function:: on_ready(ws)

   botがwebsocketに接続し終えた時点で呼び出されます。

.. function:: on_message(note: Note)
   
   ノートが接続しているチャンネル内に投稿された際に呼び出されます 

.. function:: on_emoji_add(emoji: Emoji)

   絵文字がインスタンスに追加された際に呼び出されます

.. function:: on_mention(mention: Note)
   
   メンションが含まれたノートなどが投稿された際に呼び出されます

抽象基底クラス
----------------

`abstract base class <https://docs.python.org/ja/3/glossary.html#term-abstract-base-class>`_ はメソッドなどの一覧を取得するために継承することが可能なクラスです。抽象基底クラスはインスタンス化することはできません。

AbstractBotBase
~~~~~~~~~~~~~~~~

.. attributetable:: mi.abc.AbstractChat

.. autoclass:: mi.abc.AbstractChat()
   :members:

AbstractChatContent
~~~~~~~~~~~~~~~~~~~

.. attributetable:: mi.abc.AbstractChatContent

.. autoclass:: mi.abc.AbstractChatContent()
   :members:

Misskey モデル
---------------

.. danger::
   下記のクラスは、 **ユーザーによって作成されることを考慮していません** 。
   独自のインスタンスは作成するべきではなく、値を変更するべきではありません。

Note
~~~~~~~~~~~

.. attributetable:: Note

.. autoclass:: Note()
   :members:

User
~~~~~

.. attributetable:: User

.. autoclass:: User()
   :members:

Chat
~~~~

.. attributetable::  Chat

.. autoclass:: Chat()
   :members:

Emoji
~~~~~

.. attributetable:: Emoji

.. autoclass:: Emoji()
   :members:

Renote
~~~~~~

.. attributetable:: Renote

.. autoclass:: Renote()
   :members:

Follow
~~~~~~

.. attributetable:: Follow

.. autoclass:: Follow()
   :members:

Header
~~~~~~

.. attributetable:: Header

.. autoclass:: Header()
   :members:

Properties
~~~~~~~~~~

.. attributetable:: Properties

.. autoclass:: Properties()
   :members:

File
~~~~

.. attributetable:: File

.. autoclass:: File()
   :members:

Reaction
~~~~

.. attributetable:: Reaction

.. autoclass:: Reaction()
   :members:


データクラス
------------

RawNote
~~~~~~~

.. attributetable:: RawNote

.. autoclass:: RawNote()
   :members:


RawChat
~~~~~~~

.. attributetable:: RawChat

.. autoclass:: RawChat()
   :members:


RawProperties
~~~~~~~~~~~~~

.. attributetable:: RawProperties

.. autoclass:: RawProperties()
   :members:


RawFolder
~~~~~~~~~

.. attributetable:: RawFolder

.. autoclass:: RawFolder()
   :members:


RawFile
~~~~~~~~~

.. attributetable:: RawFile

.. autoclass:: RawFile()
   :members:


RawEmoji
~~~~~~~~~

.. attributetable:: RawEmoji

.. autoclass:: RawEmoji()
   :members:


RawInstance
~~~~~~~~~

.. attributetable:: RawInstance

.. autoclass:: RawInstance()
   :members:


RawRenote
~~~~~~~~~

.. attributetable:: RawRenote

.. autoclass:: RawRenote()
   :members:


RawPollChoices
~~~~~~~~~

.. attributetable:: RawPollChoices

.. autoclass:: RawPollChoices()
   :members:


RawNoteReaction
~~~~~~~~~

.. attributetable:: RawNoteReaction

.. autoclass:: RawNoteReaction()
   :members:


RawUserDetails
~~~~~~~~~

.. attributetable:: RawUserDetails

.. autoclass:: RawUserDetails()
   :members:


RawUser
~~~~~~~~~

.. attributetable:: RawUser

.. autoclass:: RawUser()
   :members:


型クラス
--------

ChatPayload
~~~~~~~~~~~

.. attributetable:: ChatPayload

.. autoclass:: ChatPayload()
   :members:


PropertiesPayload
~~~~~~~~~~~

.. attributetable:: PropertiesPayload

.. autoclass:: PropertiesPayload()
   :members:


FolderPayload
~~~~~~~~~~~

.. attributetable:: FolderPayload

.. autoclass:: FolderPayload()
   :members:


FilePayload
~~~~~~~~~~~

.. attributetable:: FilePayload

.. autoclass:: FilePayload()
   :members:


EmojiPayload
~~~~~~~~~~~

.. attributetable:: EmojiPayload

.. autoclass:: EmojiPayload()
   :members:


FeaturesPayload
~~~~~~~~~~~

.. attributetable:: FeaturesPayload

.. autoclass:: FeaturesPayload()
   :members:


OptionalMeta
~~~~~~~~~~~

.. attributetable:: OptionalMeta

.. autoclass:: OptionalMeta()
   :members:


MetaPayload
~~~~~~~~~~~

.. attributetable:: MetaPayload

.. autoclass:: MetaPayload()
   :members:


OptionalInstance
~~~~~~~~~~~

.. attributetable:: OptionalInstance

.. autoclass:: OptionalInstance()
   :members:


InstancePayload
~~~~~~~~~~~

.. attributetable:: InstancePayload

.. autoclass:: InstancePayload()
   :members:


GeoPayload
~~~~~~~~~~~

.. attributetable:: GeoPayload

.. autoclass:: GeoPayload()
   :members:


PollPayload
~~~~~~~~~~~

.. attributetable:: PollPayload

.. autoclass:: PollPayload()
   :members:


RenotePayload
~~~~~~~~~~~

.. attributetable:: RenotePayload

.. autoclass:: RenotePayload()
   :members:


NotePayload
~~~~~~~~~~~

.. attributetable:: NotePayload

.. autoclass:: NotePayload()
   :members:


OptionalReaction
~~~~~~~~~~~

.. attributetable:: OptionalReaction

.. autoclass:: OptionalReaction()
   :members:


ReactionPayload
~~~~~~~~~~~

.. attributetable:: ReactionPayload

.. autoclass:: ReactionPayload()
   :members:


NoteReactionPayload
~~~~~~~~~~~

.. attributetable:: NoteReactionPayload

.. autoclass:: NoteReactionPayload()
   :members:


ChannelPayload
~~~~~~~~~~~

.. attributetable:: ChannelPayload

.. autoclass:: ChannelPayload()
   :members:


PinnedNotePayload
~~~~~~~~~~~

.. attributetable:: PinnedNotePayload

.. autoclass:: PinnedNotePayload()
   :members:


PinnedPagePayload
~~~~~~~~~~~

.. attributetable:: PinnedPagePayload

.. autoclass:: PinnedPagePayload()
   :members:

FieldContentPayload
~~~~~~~~~~~

.. attributetable:: FieldContentPayload

.. autoclass:: FieldContentPayload()
   :members:

OptionalUser
~~~~~~~~~~~
.. attributetable:: OptionalUser

.. autoclass:: OptionalUser()
   :members:

UserPayload
~~~~~~~~~~~

.. attributetable:: UserPayload

.. autoclass:: UserPayload()
   :members:




例外処理
--------

NotFoundError
~~~~~~~~~~~~~
.. autoclass:: NotFoundError()

TaskNotRunningError
~~~~~~~~~~~~~~~~~~~
.. autoclass:: TaskNotRunningError()

ImAi
~~~~
.. autoclass:: ImAi()

InternalServerError
~~~~~~~~~~~~~~~~~~~
.. autoclass:: InternalServerError()

ClientError
~~~~~~~~~~~

.. autoclass:: ClientError()

AuthenticationError
~~~~~~~~~~~~~~~~~~~
.. autoclass:: AuthenticationError()

NotExistRequiredParameters
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: NotExistRequiredParameters()

InvalidParameters
~~~~~~~~~~~~~~~~~
.. autoclass:: InvalidParameters()

CredentialRequired
~~~~~~~~~~~~~~~~~~
.. autoclass:: CredentialRequired()

ContentRequired
~~~~~~~~~~~~~~~

.. autoclass:: ContentRequired()


CogNameDuplicate
~~~~~~~~~~~~~~~~
.. autoclass:: CogNameDuplicate()

ExtensionAlreadyLoaded
~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: ExtensionAlreadyLoaded()

ExtensionFailed
~~~~~~~~~~~~~~~
.. autoclass:: ExtensionFailed()

NoEntryPointError
~~~~~~~~~~~~~~~~~
.. autoclass:: NoEntryPointError()

ExtensionNotFound
~~~~~~~~~~~~~~~~~
.. autoclass:: ExtensionNotFound()

CommandRegistrationError
~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: CommandRegistrationError()

CommandError
~~~~~~~~~~~~
.. autoclass:: CommandError()

CommandInvokeError
~~~~~~~~~~~~~~~~~~
.. autoclass:: CommandInvokeError()

CheckFailure
~~~~~~~~~~~~
.. autoclass:: CheckFailure()

InvalidCogPath
~~~~~~~~~~~~~~

.. autoclass:: InvalidCogPath()

NotExistRequiredData
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: NotExistRequiredData()

Low-Level API
-------------

.. autoclass:: Route()
   :members:
   
.. autoclass:: HTTPClient()
   :members:

.. autoclass:: ConnectionState()
   :members:

Low-Layer API
-------------

.. autoclass:: MisskeyClientWebSocketResponse()
   :members:

.. autoclass:: MisskeyWebSocket()
   :members:

.. autoclass:: InstanceIterator()
   :members:
