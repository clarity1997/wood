import sys
sys.path.insert(0, '/Users/tdudev/money/wood/backend')

from app.schemas.user import UserCreate
from app.models.user import UserRole
import json

# 模拟 Android 发送的 JSON
json_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "123456",
    "role": "user"
}

print("Testing JSON:", json.dumps(json_data, indent=2))

try:
    user_create = UserCreate(**json_data)
    print("✓ UserCreate validation passed")
    print(f"  username: {user_create.username}")
    print(f"  email: {user_create.email}")
    print(f"  role: {user_create.role} (type: {type(user_create.role)})")
except Exception as e:
    print(f"✗ UserCreate validation failed: {e}")
    import traceback
    traceback.print_exc()
