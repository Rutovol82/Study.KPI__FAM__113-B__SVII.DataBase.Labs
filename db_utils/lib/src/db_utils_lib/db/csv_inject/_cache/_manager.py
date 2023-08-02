from collections.abc import Iterable
from typing import Any


class CacheManager:

    def get_loader(self):
        pass

    def get_writer(self, config, data: Iterable[dict[str, Any]]):
        pass

    def list_all(self):
        pass

    def list_valid(self):
        pass

    def list_prune(self):
        pass

    def clear(self):
        pass

    def prune(self):
        pass

    def delete(self):
        pass

    def validate(self):
        pass
    