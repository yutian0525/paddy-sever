"""
API路由模块 - 定义所有API端点（移除登录相关功能）
"""

from flask import Blueprint

from app.services.image_service import ImageService
from app.services.prediction_service import PredictionService


def create_api_routes():
    """创建API路由蓝图"""
    api = Blueprint("api", __name__)

    # ============ 图像上传接口 ============
    @api.route("/upload_grow_image", methods=["POST", "GET"])
    def upload_grow_image():
        """上传生长期图像"""
        from flask import request

        return ImageService.upload_grow_image(request)

    @api.route("/upload_disease_image", methods=["POST", "GET"])
    def upload_disease_image():
        """上传病害图像"""
        from flask import request

        return ImageService.upload_disease_image(request)

    # ============ 模型预测接口 ============
    @api.route("/predict_image", methods=["POST", "GET"])
    def predict_image():
        """
        图像预测接口 - 与Go服务 /PredictImage 对应
        保持完全一致的请求/响应格式
        """
        from flask import request

        return PredictionService.predict_image(request)

    # ============ LSTM预测接口（预留扩展）============
    @api.route("/predict_weather_lstm", methods=["POST"])
    def predict_weather_lstm():
        """LSTM天气预测接口"""
        from flask import request

        return PredictionService.predict_weather_lstm(request)

    @api.route("/predict_growth_lstm", methods=["POST"])
    def predict_growth_lstm():
        """LSTM生长预测接口"""
        from flask import request

        return PredictionService.predict_growth_lstm(request)

    # ============ 图像展示接口 ============
    @api.route("/show_grow_image/<imageId>")
    def show_grow_image(imageId):
        """展示生长期图像"""
        return ImageService.show_grow_image(imageId)

    @api.route("/show_disease_image/<imageId>")
    def show_disease_image(imageId):
        """展示病害图像"""
        return ImageService.show_disease_image(imageId)

    @api.route("/show_predict_grow_image/<imageId>")
    def show_predict_grow_image(imageId):
        """展示预测后的生长期图像"""
        return ImageService.show_predict_grow_image(imageId)

    @api.route("/show_predict_disease_image/<imageId>")
    def show_predict_disease_image(imageId):
        """展示预测后的病害图像"""
        return ImageService.show_predict_disease_image(imageId)

    @api.route("/user_image/<imageId>")
    def show_user_image(imageId):
        """展示用户头像（保留以防前端仍在使用）"""
        return ImageService.show_user_image(imageId)

    # ============ 健康检查接口 ============
    @api.route("/health", methods=["GET"])
    def health_check():
        """健康检查接口"""
        from app.models.model_manager import model_manager

        model_status = {}
        for model_name in ["yolo_grow", "yolo_disease"]:
            model_status[model_name] = model_manager.is_model_loaded(model_name)

        return {
            "status": "healthy",
            "service": "paddy-prediction-service",
            "models": model_status,
        }

    # ============ 模型信息接口 ============
    @api.route("/model_info", methods=["GET"])
    def model_info():
        """获取模型信息"""
        from app.models.model_manager import model_manager

        return model_manager.get_model_info()

    return api
