"""
模型基类和接口定义
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseModel(ABC):
    """模型基类，定义所有模型的通用接口"""

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.is_loaded = False

    @abstractmethod
    def load_model(self) -> bool:
        """加载模型"""
        pass

    @abstractmethod
    def predict(self, input_data: Any, **kwargs) -> Dict[str, Any]:
        """执行预测"""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        pass

    def is_model_loaded(self) -> bool:
        """检查模型是否已加载"""
        return self.is_loaded


class ImageClassificationModel(BaseModel):
    """图像分类模型基类"""

    @abstractmethod
    def predict_image(
        self, image_path: str, save_result: bool = True
    ) -> Dict[str, Any]:
        """
        预测图像

        Args:
            image_path: 图像文件路径
            save_result: 是否保存预测结果图像

        Returns:
            包含预测结果的字典
        """
        pass


class TimeSeriesModel(BaseModel):
    """时间序列模型基类（为LSTM预留）"""

    @abstractmethod
    def predict_sequence(self, sequence_data: Any, **kwargs) -> Dict[str, Any]:
        """
        预测时间序列

        Args:
            sequence_data: 时间序列数据

        Returns:
            包含预测结果的字典
        """
        pass
