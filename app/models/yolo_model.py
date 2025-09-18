"""
YOLO模型实现
"""

import os
from typing import Any, Dict

from ultralytics import YOLO

from app.config import Config
from app.models.base_model import ImageClassificationModel
from app.utils.file_utils import get_file_extension_as_jpg, move_file


class YOLOModel(ImageClassificationModel):
    """YOLO模型实现类"""

    def __init__(self, model_path: str, model_type: str):
        super().__init__(model_path)
        self.model_type = model_type  # 'grow' or 'disease'

    def load_model(self) -> bool:
        """加载YOLO模型"""
        try:
            if not os.path.exists(self.model_path):
                print(f"模型文件不存在: {self.model_path}")
                return False

            self.model = YOLO(self.model_path)
            self.is_loaded = True
            print(f"YOLO模型加载成功: {self.model_path}")
            return True
        except Exception as e:
            print(f"YOLO模型加载失败: {e}")
            self.is_loaded = False
            return False

    def predict(self, input_data: Any, **kwargs) -> Dict[str, Any]:
        """基础预测方法"""
        return self.predict_image(input_data, **kwargs)

    def predict_image(
        self, image_path: str, save_result: bool = True
    ) -> Dict[str, Any]:
        """
        使用YOLO模型预测图像

        Args:
            image_path: 图像文件路径
            save_result: 是否保存预测结果

        Returns:
            预测结果字典
        """
        if not self.is_loaded:
            if not self.load_model():
                return {"error": "模型加载失败"}

        if not os.path.exists(image_path):
            return {"error": f"图像文件不存在: {image_path}"}

        try:
            # 执行预测
            results = self.model(image_path, save=save_result)
            result = results[0]

            # 处理保存结果文件
            if save_result:
                self._save_prediction_result(image_path, result)

            # 根据模型类型返回不同的结果格式
            if self.model_type == "grow":
                return self._process_classification_result(result)
            else:  # disease
                return self._process_detection_result(result)

        except Exception as e:
            print(f"预测失败: {e}")
            return {"error": f"预测失败: {str(e)}"}

    def _save_prediction_result(self, original_image_path: str, result):
        """保存预测结果图像"""
        try:
            # 获取原始文件名（不含扩展名）并添加.jpg
            original_filename = os.path.basename(original_image_path)
            result_filename = get_file_extension_as_jpg(original_filename)

            # 构建源文件路径（YOLO保存的结果）
            src_file = os.path.join(result.save_dir, result_filename)

            # 目标目录
            target_dir = Config.PREDICT_OUTPUT_PATHS[self.model_type]

            # 移动文件
            if os.path.exists(src_file):
                move_file(src_file, target_dir)
            else:
                print(f"预测结果文件不存在: {src_file}")
                # 列出目录中的文件以便调试
                if os.path.exists(result.save_dir):
                    files = os.listdir(result.save_dir)
                    print(f"结果目录中的文件: {files}")

        except Exception as e:
            print(f"保存预测结果失败: {e}")

    def _process_classification_result(self, result) -> Dict[str, Any]:
        """处理分类结果（生长期预测）- 与原始格式完全一致"""
        try:
            probs = result.probs.data.tolist()
            names = result.names
            max_prob_index = probs.index(max(probs))

            # 返回与原始代码完全一致的格式
            return {
                "names": names,
                "speed": result.speed,
                "result": names[max_prob_index],
            }
        except Exception as e:
            print(f"处理分类结果失败: {e}")
            return {"error": f"处理分类结果失败: {str(e)}"}

    def _process_detection_result(self, result) -> Dict[str, Any]:
        """处理检测结果（病害检测）- 提取检测到的类别名称"""
        try:
            detected_names = {}
            # 遍历检测到的边界框
            for box in result.boxes:
                # 获取类别ID（tensor）并转换为整数
                class_id = int(box.cls.item())
                # 从模型的名称列表中获取类别名称
                class_name = result.names[class_id]
                # 使用类别名称作为键，可以避免重复，或者您可以构建一个列表
                detected_names[class_id] = class_name

            # 返回检测到的名称和速度
            return {"names": detected_names, "speed": result.speed}
        except Exception as e:
            print(f"处理检测结果失败: {e}")
            return {"error": f"处理检测结果失败: {str(e)}"}

    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            "model_type": "YOLO",
            "model_path": self.model_path,
            "task_type": self.model_type,
            "is_loaded": self.is_loaded,
        }
