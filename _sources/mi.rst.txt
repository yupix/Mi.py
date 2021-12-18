.. currentmodule:: mi

API Reference
===============

このセクションではMi.pyのAPIについて説明します

.. note::
   このライブラリではloggingを用いてdebug出力が可能です。標準設定では出ないため、起動時の引数として `debug` を渡すようにしてください

イベントリファレンス
--------------------

.. function:: on_message()
   
   :class:`Note` が作成された際に呼び出されます

抽象基底クラス
----------------

[abstract base class](https://docs.python.org/ja/3/glossary.html#term-abstract-base-class)はメソッドなどの一覧を取得するために継承することが可能なクラスです。抽象基底クラスはインスタンス化することはできません。

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

UserDetails
~~~~~~~~~~~~

.. attributetable:: UserDetails

.. autoclass:: UserDetails()
   :members:


.. attributetable::  Chat

.. autoclass:: Chat()
   :members:

Drive
~~~~~

.. attributetable:: Drive

.. autoclass:: Drive()
   :members:

Emoji
~~~~~

.. attributetable:: Emoji

.. autoclass:: Emoji()
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


Low-Level API
-------------

.. autoclass:: Route()

.. autoclass:: HTTPClient()

.. autoclass:: ConnectionState()

Low-Layer API
-------------

.. autoclass:: MisskeyClientWebSocketResponse()

.. autoclass:: MisskeyWebSocket()

.. autoclass:: InstanceIterator()
