"""
命令行入口
用于本地测试
"""
import sys
from .core import AgentCore


def main():
    """主函数"""
    agent = AgentCore()
    
    # 用户输入方式1：命令行参数
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    # 用户输入方式2：交互式输入
    else:
        user_query = input("请输入您的问题: ")
    
    try:
        response = agent.process_query(user_query)
        print(response)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

