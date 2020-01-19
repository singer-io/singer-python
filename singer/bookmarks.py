import json
import sys
from typing import Any, Dict, Optional, Sequence, Union
from .logger import get_logger


LOGGER = get_logger()


def write_state(state):
    json.dump(state.to_dict(), sys.stdout, indent=2)


class State:
    def __init__(
        self, bookmarks: Optional[Dict] = None, currently_syncing: Optional[str] = None  # pylint: disable=bad-continuation
    ) -> None:
        self._bookmarks = bookmarks or {}
        self._currently_syncing = currently_syncing

    def __str__(self) -> str:
        return str(self.__dict__)

    def __eq__(self, other: Any) -> bool:
        return self.__dict__ == other.__dict__

    @property
    def bookmarks(self) -> Dict:
        return self._bookmarks

    @classmethod
    def load(cls, filename: str) -> "State":
        with open(filename) as fp:  # pylint: disable=invalid-name
            return State.from_dict(json.load(fp))

    @classmethod
    def from_dict(cls, data: Dict) -> "State":
        return State(
            bookmarks=data.get("bookmarks"),
            currently_syncing=data.get("currently_syncing"),
        )

    def to_dict(self) -> Dict:
        state = {"bookmarks": self.bookmarks}  # type: Dict[str, Any]
        if self.get_currently_syncing():
            state["currently_syncing"] = self.get_currently_syncing()
        return state

    def dump(self) -> None:
        json.dump(self.to_dict(), sys.stdout, indent=2)

    def _ensure_bookmark_path(self, path: Sequence) -> None:
        submap = self.bookmarks
        for path_component in path:
            if submap.get(path_component) is None:
                submap[path_component] = {}

            submap = submap[path_component]

    def write_bookmark(self, tap_stream_id: str, key: str, val: Any) -> None:
        self._ensure_bookmark_path((tap_stream_id,))
        self.bookmarks[tap_stream_id][key] = val

    def clear_bookmark(self, tap_stream_id: str, key: str) -> None:
        self._ensure_bookmark_path((tap_stream_id,))
        self.bookmarks[tap_stream_id].pop(key, None)

    def reset_stream(self, tap_stream_id: str) -> None:
        self._ensure_bookmark_path((tap_stream_id,))
        self.bookmarks[tap_stream_id] = {}

    def get_bookmark(self, tap_stream_id: str, key: str, default: Any = None) -> Any:
        return self.bookmarks.get(tap_stream_id, {}).get(key, default)

    def set_offset(
        self, tap_stream_id: str, offset_key: str, offset_value: Any  # pylint: disable=bad-continuation
    ) -> None:
        self._ensure_bookmark_path((tap_stream_id, "offset", offset_key))
        self.bookmarks[tap_stream_id]["offset"][offset_key] = offset_value

    def clear_offset(self, tap_stream_id: str) -> None:
        self._ensure_bookmark_path((tap_stream_id, "offset"))
        self.bookmarks[tap_stream_id]["offset"] = {}

    def get_offset(
        self, tap_stream_id: str, offset_key: str, default: Any = None  # pylint: disable=bad-continuation
    ) -> Any:
        return (
            self.bookmarks.get(tap_stream_id, {})
            .get("offset", {})
            .get(offset_key, default)
        )

    def get_currently_syncing(self, default: Optional[str] = None) -> Optional[str]:
        return self._currently_syncing or default

    def set_currently_syncing(self, value: Union[str, None]) -> None:
        self._currently_syncing = value
