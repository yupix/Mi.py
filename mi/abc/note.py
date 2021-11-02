from abc import ABC, abstractmethod


class AbstractNote(ABC):
    @abstractmethod
    def emoji_count(self) -> int:
        """
        ノートの本文にemojiが何個含まれているかを返します

        Returns
        -------
        int
            含まれている絵文字の数
        """

    @abstractmethod
    async def delete(self, note_id: str = None) -> bool:
        """
        指定したIDのノートを削除します

        Parameters
        ----------
        note_id: str
            削除するノートのid

        returns
        -------
        bool
            成功したか否か
        """

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
        ノートにファイルを添付します。

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
