from pydantic import EmailStr, BaseModel

class Test(BaseModel):
    email: EmailStr

try:
    t = Test(email='test@example.com')
    print('EmailStr validation OK')
except Exception as e:
    print(f'EmailStr validation failed: {e}')
