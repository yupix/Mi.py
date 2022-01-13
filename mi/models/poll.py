from typing import List, Optional

from mi.types.note import Poll as PollPayload


class RawPollChoices:
    def __init__(self, data):
        self.text: str = data["text"]
        self.votes: int = data["votes"]
        self.is_voted: bool = data["isVoted"]


class RawPoll:
    def __init__(self, data: PollPayload):
        self.multiple: Optional[bool] = data.get("multiple")
        self.expires_at: Optional[int] = data.get("expires_at")
        self.choices: Optional[List[RawPollChoices]] = [RawPollChoices(i) for i in data['choices']] if data.get(
            "choices") else None
        self.expired_after: Optional[int] = data.get("expired_after")
