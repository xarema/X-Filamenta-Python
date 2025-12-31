
import os
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.src.services.cache_service import cache_service, FilesystemCache

class MockUser:
    def __init__(self, id, username):
        self.id = id
        self.username = username
    def __repr__(self):
        return f"<User {self.username}>"

def test_serialization_error():
    print("Testing FilesystemCache serialization...")
    fs_cache = FilesystemCache()
    user = MockUser(1, "testuser")

    try:
        # This should trigger the TypeError in json.dump
        # but let's see if the try-except in FilesystemCache.set handles it
        print(f"Attempting to cache object: {user}")
        fs_cache.set("test_user_key", user)
        print("Set operation completed (possibly ignored error)")

        val = fs_cache.get("test_user_key")
        print(f"Retrieved value: {val}")

    except Exception as e:
        print(f"Caught unexpected exception: {type(e).__name__}: {e}")

if __name__ == "__main__":
    os.environ["CACHE_DIR"] = "./scripts/debug/cache_test"
    test_serialization_error()
