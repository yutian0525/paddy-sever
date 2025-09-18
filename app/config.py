"""
应用配置文件
"""

import os


class Config:
    """基础配置类"""

    # Flask配置
    JSON_AS_ASCII = False

    # 文件上传配置
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # 静态文件路径配置 - 保持与原始代码完全一致
    STATIC_BASE_PATH = "paddy-server/static"
    IMAGE_UPLOAD_PATHS = {
        "grow": os.path.join(STATIC_BASE_PATH, "image/grow"),
        "disease": os.path.join(STATIC_BASE_PATH, "image/disease"),
        "user": os.path.join(STATIC_BASE_PATH, "userimg"),
    }
    PREDICT_OUTPUT_PATHS = {
        "grow": os.path.join(STATIC_BASE_PATH, "predict_image/grow"),
        "disease": os.path.join(STATIC_BASE_PATH, "predict_image/disease"),
    }

    # 模型配置
    MODEL_PATHS = {
        "yolo_grow": "models/paddy-grow.pt",
        "yolo_disease": "models/paddy-disease.pt",
        "lstm_weather": "models/lstm_weather.pt",  # 为LSTM预留
        "lstm_growth": "models/lstm_growth.pt",  # 为LSTM预留
    }

    # API配置
    HOST = "127.0.0.1"
    PORT = 5050
    DEBUG = True

    # CORS配置
    CORS_ORIGINS = [
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:3000",
    ]


class DevelopmentConfig(Config):
    """开发环境配置"""

    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""

    DEBUG = False


# 根据环境变量选择配置
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
