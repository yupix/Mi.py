from typing import Any, ClassVar, Dict, List, Tuple

__all__ = ['Cog']

class Cog:
    __cog_name__ = ClassVar[str]
    __cog__settings__ = ClassVar[Dict[str, Any]]
    __cog_commands__: ClassVar[List]
    __cog_listeners__: ClassVar[List[Tuple[str, str]]]
    
    