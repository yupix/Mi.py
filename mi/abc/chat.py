from abc import ABC, abstractmethod


class AbstractChat(ABC):
    @abstractmethod
    async def send(self) -> 'AbstractChatContent':
        pass

    @abstractmethod
    def add_file(
            self,
            path: str = None,
            name: str = None,
            force: bool = False,
            is_sensitive: bool = False,
            url: str = None,
    ):
        """
        チャットにファイルを添付します。

        Parameters
        ----------
        is_sensitive : bool
            この画像がセンシティブな物の場合Trueにする
        force : bool
            Trueの場合同じ名前のファイルがあった場合でも強制的に保存する
        path : str
            そのファイルまでのパスとそのファイル.拡張子(/home/test/test.png)
        name: str
            ファイル名(拡張子があるなら含めて)
        url : str
            URLから画像をアップロードする場合にURLを指定する

        Returns
        -------
        self: Note
        """


class AbstractChatContent(ABC):
    @abstractmethod
    async def delete(self):
        pass
