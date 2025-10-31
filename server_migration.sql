-- =============================================
-- 家具购物APP数据库迁移脚本
-- 在阿里云服务器PostgreSQL数据库上执行
-- =============================================

-- 1. 为users表添加balance字段
ALTER TABLE users
ADD COLUMN IF NOT EXISTS balance FLOAT NOT NULL DEFAULT 10000000.0;

-- 2. 更新所有现有用户的余额为10000000元
UPDATE users
SET balance = 10000000.0
WHERE balance IS NULL OR balance = 0;

-- 3. 验证用户余额字段
SELECT id, username, role, balance FROM users;

-- =============================================
-- 说明：
-- 1. balance字段：用户账户余额，默认10000000元
-- 2. 订单、订单项表已通过SQLAlchemy自动创建
-- 3. 所有其他表结构保持不变
-- =============================================
