import secrets
import json

# Generate secure keys
secret_key = secrets.token_hex(32)
redis_password = secrets.token_hex(16)
db_password = secrets.token_urlsafe(24)

print("=" * 80)
print("GENERATED PRODUCTION SECRETS")
print("=" * 80)
print(f"\nFLASK_SECRET_KEY={secret_key}")
print(f"\nREDIS_PASSWORD={redis_password}")
print(f"\nDB_PASSWORD={db_password}")
print("\n" + "=" * 80)
print("Copy these values to .env.production")
print("=" * 80)

