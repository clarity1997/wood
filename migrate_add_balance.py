"""
数据库迁移脚本：为现有用户添加balance字段
"""
from sqlalchemy import create_engine, text
from app.config import settings

def migrate():
    engine = create_engine(settings.DATABASE_URL)

    with engine.connect() as conn:
        # 添加balance列（如果不存在）
        try:
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS balance FLOAT NOT NULL DEFAULT 10000000.0
            """))
            conn.commit()
            print("✅ 成功添加balance列")
        except Exception as e:
            print(f"添加列时出错（可能已存在）: {e}")

        # 更新所有现有用户的余额为10000000
        try:
            result = conn.execute(text("""
                UPDATE users
                SET balance = 10000000.0
                WHERE balance IS NULL OR balance = 0
            """))
            conn.commit()
            print(f"✅ 成功更新 {result.rowcount} 个用户的余额")
        except Exception as e:
            print(f"更新余额时出错: {e}")

if __name__ == "__main__":
    migrate()
