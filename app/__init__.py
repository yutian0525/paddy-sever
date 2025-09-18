"""
应用工厂函数 - 创建Flask应用
"""

from flask import Flask
from flask_cors import CORS

from app.api.routes import create_api_routes
from app.config import config


def create_app(config_name="development"):
    """
    应用工厂函数

    Args:
        config_name: 配置名称，默认为development

    Returns:
        Flask应用实例
    """
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config[config_name])

    # 设置JSON响应不转义ASCII
    app.config["JSON_AS_ASCII"] = False

    # 配置CORS - 允许Go服务调用
    CORS(
        app,
        origins=config[config_name].CORS_ORIGINS,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # 注册API路由
    api_routes = create_api_routes()
    app.register_blueprint(api_routes)

    # 预加载模型（可选，也可以在首次调用时加载）
    with app.app_context():
        _initialize_models()

    return app


def _initialize_models():
    """初始化模型"""
    try:
        from app.models.model_manager import model_manager

        # 只加载YOLO模型，LSTM模型在需要时再加载
        print("正在加载YOLO模型...")
        yolo_results = {
            "yolo_grow": model_manager.load_model("yolo_grow"),
            "yolo_disease": model_manager.load_model("yolo_disease"),
        }

        for model_name, success in yolo_results.items():
            if success:
                print(f"✓ {model_name} 加载成功")
            else:
                print(f"✗ {model_name} 加载失败")

        print("模型初始化完成")

    except Exception as e:
        print(f"模型初始化失败: {e}")
        # 不阻止应用启动，允许运行时加载
