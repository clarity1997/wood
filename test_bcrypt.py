from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    # Test with simple password
    password = "111"
    print(f"Testing password: '{password}'")
    print(f"Password length: {len(password)} chars, {len(password.encode('utf-8'))} bytes")

    hashed = pwd_context.hash(password)
    print(f"✓ Hash successful: {hashed}")

    # Test verification
    verified = pwd_context.verify(password, hashed)
    print(f"✓ Verification: {verified}")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
