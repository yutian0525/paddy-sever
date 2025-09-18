"""
响应格式化工具 - 保持与原始API完全一致的返回格式
"""

import json


def upload_success_response(filename):
    """文件上传成功响应 - 与原始格式一致"""
    return {"code": "200", "data": filename, "message": "上传成功"}


def upload_error_response(message="格式错误，仅支持jpg、png、jpeg格式文件"):
    """文件上传失败响应 - 与原始格式一致"""
    return {"code": "503", "message": message}


def method_error_response():
    """方法错误响应 - 与原始格式一致"""
    return {"code": "503", "message": "仅支持post方法"}


def prediction_success_response(data, message="预测完成"):
    """预测成功响应 - 与原始格式完全一致"""
    return_dict = {"code": "200", "data": data, "message": message}
    return json.dumps(return_dict, ensure_ascii=False)


def prediction_error_response(message, code="500"):
    """预测失败响应 - 与原始格式一致"""
    return_dict = {"code": code, "data": "", "message": message}
    return json.dumps(return_dict, ensure_ascii=False)


def file_not_found_response(file_path):
    """文件未找到响应 - 与原始格式一致"""
    return_dict = {
        "code": "500",
        "message": f"File not found at {file_path}",
        "data": "",
    }
    return json.dumps(return_dict, ensure_ascii=False)
