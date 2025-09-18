"""
工具函数模块
"""

import os
import shutil

from werkzeug.utils import secure_filename

from app.config import Config


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )


def ensure_directory_exists(directory_path):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def move_file(src_file, dst_path):
    """
    移动文件到指定目录

    Args:
        src_file: 源文件路径
        dst_path: 目标目录路径

    Returns:
        bool: 移动是否成功
    """
    if not os.path.isfile(src_file):
        print(f"源文件不存在: {src_file}")
        return False

    # 分离文件名和路径
    fpath, fname = os.path.split(src_file)

    # 确保目标目录存在
    ensure_directory_exists(dst_path)

    try:
        # 移动文件
        dest_file = os.path.join(dst_path, fname)
        shutil.move(src_file, dest_file)
        print(f"文件移动成功: {src_file} -> {dest_file}")
        return True
    except Exception as e:
        print(f"文件移动失败: {e}")
        return False


def secure_save_file(file, save_path, filename=None):
    """
    安全地保存上传的文件

    Args:
        file: 上传的文件对象
        save_path: 保存路径
        filename: 可选的文件名，如果不提供则使用原文件名

    Returns:
        str: 保存的文件名，失败返回None
    """
    if not file or not allowed_file(file.filename):
        return None

    # 使用安全的文件名
    if filename is None:
        filename = secure_filename(file.filename)
    else:
        filename = secure_filename(filename)

    # 确保保存目录存在
    ensure_directory_exists(save_path)

    try:
        # 保存文件
        full_path = os.path.join(save_path, filename)
        file.save(full_path)
        return filename
    except Exception as e:
        print(f"文件保存失败: {e}")
        return None


def get_file_extension_as_jpg(filename):
    """
    获取不带扩展名的文件名并添加.jpg扩展名
    用于预测结果文件名生成
    """
    return os.path.splitext(filename)[0] + ".jpg"
