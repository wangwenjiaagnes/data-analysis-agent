"""
配置管理模块
读取环境变量（Groq API Key、Supabase 连接信息）
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# Groq LLM 配置
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Supabase 配置
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# API 服务配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))


def validate_config():
    """验证配置是否完整"""
    errors = []
    
    if not GROQ_API_KEY:
        errors.append("GROQ_API_KEY not set")
    
    if not SUPABASE_URL:
        errors.append("SUPABASE_URL not set")
    
    if not SUPABASE_KEY:
        errors.append("SUPABASE_KEY not set")
    
    if errors:
        raise ValueError("Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))
    
    return True


if __name__ == "__main__":
    # 测试配置加载
    try:
        validate_config()
        print("✅ Config loaded successfully")
        print(f"   Groq Model: {GROQ_MODEL}")
        print(f"   Supabase URL: {SUPABASE_URL[:30]}..." if SUPABASE_URL else "   Supabase URL: Not set")
    except ValueError as e:
        print(f"❌ {e}")

