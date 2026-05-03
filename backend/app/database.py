# 1. 导入SQLAlchemy核心工具
from sqlalchemy import create_engine       # 创建数据库连接引擎
from sqlalchemy.orm import DeclarativeBase, sessionmaker  # 基类+会话工厂
from app.config import settings  # 导入项目配置（数据库地址等）

# 2. 创建数据库引擎（核心连接管理器）
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# 3. 创建数据库会话工厂（生产数据库会话）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 定义ORM模型基类（所有数据表模型都继承它）
class Base(DeclarativeBase):
    pass

# 5. FastAPI依赖项：获取数据库会话，用完自动关闭
def get_db():
    db = SessionLocal()  # 创建一个新的数据库会话
    try:
        yield db  # 把会话返回给API使用
    finally:
        db.close()  # 无论请求成功/失败，最终关闭会话，释放资源