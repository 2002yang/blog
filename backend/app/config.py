# 导入 Pydantic Settings 核心类（v2 新版语法）
from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目配置核心类：所有配置项都在这里定义
class Settings(BaseSettings):
    # 【核心配置】指定加载 .env 文件，忽略无关环境变量
    model_config = SettingsConfigDict(
        env_file=".env",       # 自动读取项目根目录的 .env 环境变量文件
        extra="ignore"         # 忽略 .env 中多余的、未定义的变量，避免报错
    )

    # ==================== 数据库配置 ====================
    # 数据库连接地址（默认值，会被 .env 文件覆盖）
    DATABASE_URL: str = "postgresql://blog:blog@localhost:5432/blog"

    # ==================== JWT 认证配置 ====================
    # 加密密钥（生产环境必须修改！）
    SECRET_KEY: str = "change-me-in-production-use-openssl-rand-hex-32"
    # JWT 签名算法
    ALGORITHM: str = "HS256"
    # 访问令牌过期时间（15分钟）
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    # 刷新令牌过期时间（7天）
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ==================== 文件上传配置 ====================
    # 上传文件存储目录
    UPLOAD_DIR: str = "./uploads"
    # 最大上传大小（5MB）
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024

    # ==================== 跨域配置 ====================
    # 允许的前端域名（CORS）
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost"]

# 【全局单例】创建配置实例，整个项目导入这一个对象即可使用
settings = Settings()