"""
图像处理服务 - 处理图像上传和展示
"""

from flask import Response

from app.config import Config
from app.utils.file_utils import secure_save_file
from app.utils.response_utils import (
    method_error_response,
    upload_error_response,
    upload_success_response,
)


class ImageService:
    """图像处理服务类"""

    @staticmethod
    def upload_grow_image(request):
        """上传生长期图像 - 保持与原始API完全一致"""
        if request.method == "POST":
            file = request.files["file"]
            filename = secure_save_file(file, Config.IMAGE_UPLOAD_PATHS["grow"])

            if filename:
                return upload_success_response(filename)
            else:
                return upload_error_response()

        return method_error_response()

    @staticmethod
    def upload_disease_image(request):
        """上传病害图像 - 保持与原始API完全一致"""
        if request.method == "POST":
            file = request.files["file"]
            filename = secure_save_file(file, Config.IMAGE_UPLOAD_PATHS["disease"])

            if filename:
                return upload_success_response(filename)
            else:
                return upload_error_response()

        return method_error_response()

    @staticmethod
    def show_grow_image(image_id):
        """显示生长期图像 - 保持与原始API完全一致"""
        try:
            # 保持与原始代码完全一致的路径格式
            image_path = f"paddy-server/static/image/grow/{image_id}"
            with open(image_path, "rb") as f:
                image = f.read()
                return Response(image, mimetype="image/jpg")
        except Exception as e:
            print(f"显示生长期图像失败: {e}")
            return Response("Image not found", status=404)

    @staticmethod
    def show_disease_image(image_id):
        """显示病害图像 - 保持与原始API完全一致"""
        try:
            # 保持与原始代码完全一致的路径格式
            image_path = f"paddy-server/static/image/disease/{image_id}"
            with open(image_path, "rb") as f:
                image = f.read()
                return Response(image, mimetype="image/jpg")
        except Exception as e:
            print(f"显示病害图像失败: {e}")
            return Response("Image not found", status=404)

    @staticmethod
    def show_predict_grow_image(image_id):
        """显示预测后的生长期图像 - 保持与原始API完全一致"""
        try:
            # 保持与原始代码完全一致的路径格式
            image_path = f"paddy-server/static/predict_image/grow/{image_id}"
            with open(image_path, "rb") as f:
                image = f.read()
                return Response(image, mimetype="image/jpg")
        except Exception as e:
            print(f"显示预测生长期图像失败: {e}")
            return Response("Image not found", status=404)

    @staticmethod
    def show_predict_disease_image(image_id):
        """显示预测后的病害图像 - 保持与原始API完全一致"""
        try:
            # 保持与原始代码完全一致的路径格式
            image_path = f"paddy-server/static/predict_image/disease/{image_id}"
            with open(image_path, "rb") as f:
                image = f.read()
                return Response(image, mimetype="image/jpg")
        except Exception as e:
            print(f"显示预测病害图像失败: {e}")
            return Response("Image not found", status=404)

    @staticmethod
    def show_user_image(image_id):
        """显示用户头像 - 保持与原始API完全一致"""
        try:
            # 保持与原始代码完全一致的路径格式
            image_path = f"paddy-server/static/userimg/{image_id}"
            with open(image_path, "rb") as f:
                image = f.read()
                return Response(image, mimetype="image/jpg")
        except Exception as e:
            print(f"显示用户图像失败: {e}")
            return Response("Image not found", status=404)
