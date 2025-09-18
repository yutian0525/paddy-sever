"""
重构后的主入口文件 - 专供Go服务调用的模型预测微服务
移除了所有登录相关功能，保持与原始API完全一致的接口格式
"""

from app import create_app

# 创建Flask应用
app = create_app("development")

if __name__ == "__main__":
    # 启动服务，保持与原始代码相同的配置
    app.run(host="127.0.0.1", port=5050, debug=True)
