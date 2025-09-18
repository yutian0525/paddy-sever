"""
模型管理器 - 统一管理所有模型
"""

from typing import Any, Dict

from app.config import Config
from app.models.lstm_model import LSTMGrowthModel, LSTMWeatherModel
from app.models.yolo_model import YOLOModel


class ModelManager:
    """模型管理器，负责加载和管理所有模型"""

    def __init__(self):
        self.models: Dict[str, Any] = {}
        self._initialize_models()

    def _initialize_models(self):
        """初始化所有模型"""
        try:
            # 初始化YOLO模型
            self.models["yolo_grow"] = YOLOModel(
                Config.MODEL_PATHS["yolo_grow"], "grow"
            )
            self.models["yolo_disease"] = YOLOModel(
                Config.MODEL_PATHS["yolo_disease"], "disease"
            )

            # 初始化LSTM模型（预留）
            self.models["lstm_weather"] = LSTMWeatherModel(
                Config.MODEL_PATHS["lstm_weather"]
            )
            self.models["lstm_growth"] = LSTMGrowthModel(
                Config.MODEL_PATHS["lstm_growth"]
            )

            print("模型管理器初始化完成")

        except Exception as e:
            print(f"模型管理器初始化失败: {e}")

    def get_model(self, model_name: str):
        """获取指定模型"""
        return self.models.get(model_name)

    def load_model(self, model_name: str) -> bool:
        """加载指定模型"""
        model = self.get_model(model_name)
        if model:
            return model.load_model()
        else:
            print(f"模型不存在: {model_name}")
            return False

    def load_all_models(self) -> Dict[str, bool]:
        """加载所有模型"""
        results = {}
        for model_name, model in self.models.items():
            try:
                results[model_name] = model.load_model()
            except Exception as e:
                print(f"加载模型 {model_name} 失败: {e}")
                results[model_name] = False

        return results

    def predict_image(
        self, model_type: str, image_path: str, save_result: bool = True
    ) -> Dict[str, Any]:
        """
        使用指定模型预测图像

        Args:
            model_type: 模型类型 ('grow' 或 'disease')
            image_path: 图像路径
            save_result: 是否保存结果

        Returns:
            预测结果
        """
        model_name = f"yolo_{model_type}"
        model = self.get_model(model_name)

        if not model:
            return {"error": f"模型不存在: {model_name}"}

        return model.predict_image(image_path, save_result)

    def predict_weather(self, sequence_data: Any, **kwargs) -> Dict[str, Any]:
        """
        使用LSTM模型预测天气

        Args:
            sequence_data: 时间序列数据
            **kwargs: 其他参数

        Returns:
            预测结果
        """
        model = self.get_model("lstm_weather")
        if not model:
            return {"error": "LSTM天气模型不可用"}

        return model.predict_sequence(sequence_data, **kwargs)

    def predict_growth(self, sequence_data: Any, **kwargs) -> Dict[str, Any]:
        """
        使用LSTM模型预测作物生长

        Args:
            sequence_data: 时间序列数据
            **kwargs: 其他参数

        Returns:
            预测结果
        """
        model = self.get_model("lstm_growth")
        if not model:
            return {"error": "LSTM生长模型不可用"}

        return model.predict_sequence(sequence_data, **kwargs)

    def get_model_info(self, model_name: str = None) -> Dict[str, Any]:
        """
        获取模型信息

        Args:
            model_name: 指定模型名，如果为None则返回所有模型信息

        Returns:
            模型信息
        """
        if model_name:
            model = self.get_model(model_name)
            if model:
                return model.get_model_info()
            else:
                return {"error": f"模型不存在: {model_name}"}
        else:
            # 返回所有模型信息
            info = {}
            for name, model in self.models.items():
                info[name] = model.get_model_info()
            return info

    def is_model_loaded(self, model_name: str) -> bool:
        """检查模型是否已加载"""
        model = self.get_model(model_name)
        return model.is_model_loaded() if model else False


# 全局模型管理器实例
model_manager = ModelManager()
