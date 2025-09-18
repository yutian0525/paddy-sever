"""
预测服务 - 处理模型预测逻辑
"""

import os

from app.models.model_manager import model_manager
from app.utils.response_utils import (
    file_not_found_response,
    prediction_error_response,
    prediction_success_response,
)


class PredictionService:
    """预测服务类"""

    @staticmethod
    def predict_image(request):
        """
        图像预测服务 - 保持与原始API完全一致的返回格式
        与Go服务 /PredictImage 接口对应
        """
        # 打印请求信息（保持与原始代码一致）
        print("--- Request Headers ---")
        print(request.headers)
        print("--- Request Data ---")
        print(request.data)  # raw request body
        print("--- End Request Info ---")

        # 检查请求参数
        if request.args is None:
            return prediction_error_response("请求参数为空", "5004")

        try:
            get_data = request.get_json()
            pic_name = get_data.get("imageid")
            model_id = get_data.get("modelid")

            print(f"收到预测请求: imageid={pic_name}, modelid={model_id}")

            if model_id == "1":
                # 生长期预测
                return PredictionService._predict_grow_image(pic_name)
            else:
                # 病害检测
                return PredictionService._predict_disease_image(pic_name)

        except Exception as e:
            print(f"预测请求处理失败: {e}")
            return prediction_error_response(f"请求处理失败: {str(e)}")

    @staticmethod
    def _predict_grow_image(pic_name):
        """生长期图像预测 - 保持与原始逻辑完全一致"""
        # 保持与原始代码完全一致的路径构建
        pic_path = os.path.join("static/image/grow/", pic_name)
        print(f"Constructed pic_path: {pic_path}")

        if not os.path.exists(pic_path):
            print(f"Error: File not found at {pic_path}")
            return file_not_found_response(pic_path)

        try:
            # 使用模型管理器进行预测
            result = model_manager.predict_image("grow", pic_path, save_result=True)

            if "error" in result:
                return prediction_error_response(result["error"])

            # 返回与原始代码完全一致的格式
            return_dict = {"data": result}
            print(f"Returning to Go: {return_dict}")
            return prediction_success_response(result)

        except Exception as e:
            print(f"生长期预测失败: {e}")
            return prediction_error_response(f"预测失败: {str(e)}")

    @staticmethod
    def _predict_disease_image(pic_name):
        """病害图像预测 - 保持与原始逻辑完全一致"""
        # 保持与原始代码完全一致的路径构建
        pic_path = os.path.join("static/image/disease/", pic_name)
        print(f"Constructed pic_path for disease: {pic_path}")

        if not os.path.exists(pic_path):
            print(f"Error: File not found at {pic_path}")
            return file_not_found_response(pic_path)

        try:
            # 使用模型管理器进行预测
            result = model_manager.predict_image("disease", pic_path, save_result=True)

            if "error" in result:
                return prediction_error_response(result["error"])

            # 返回与原始代码完全一致的格式
            return_dict = {"data": result}
            print(f"Returning to Go: {return_dict}")
            return prediction_success_response(result)

        except Exception as e:
            print(f"病害预测失败: {e}")
            return prediction_error_response(f"预测失败: {str(e)}")

    @staticmethod
    def predict_weather_lstm(request):
        """
        LSTM天气预测服务 - 为未来扩展预留
        """
        try:
            get_data = request.get_json()
            sequence_data = get_data.get("sequence_data")
            prediction_days = get_data.get("prediction_days", 7)

            result = model_manager.predict_weather(
                sequence_data, prediction_days=prediction_days
            )

            if "error" in result:
                return prediction_error_response(result["error"])

            return prediction_success_response(result, "LSTM天气预测完成")

        except Exception as e:
            print(f"LSTM天气预测失败: {e}")
            return prediction_error_response(f"LSTM天气预测失败: {str(e)}")

    @staticmethod
    def predict_growth_lstm(request):
        """
        LSTM生长预测服务 - 为未来扩展预留
        """
        try:
            get_data = request.get_json()
            sequence_data = get_data.get("sequence_data")

            result = model_manager.predict_growth(sequence_data)

            if "error" in result:
                return prediction_error_response(result["error"])

            return prediction_success_response(result, "LSTM生长预测完成")

        except Exception as e:
            print(f"LSTM生长预测失败: {e}")
            return prediction_error_response(f"LSTM生长预测失败: {str(e)}")
