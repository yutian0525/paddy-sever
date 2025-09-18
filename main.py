from flask import Flask, request, Response
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
import shutil
from glob import glob
import json
from flask_cors import CORS
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017")
db = myclient['paddy']
userscollection = db['users']

users = {
    "Nilei" : {
        "id" : 100000,
        "password" : "123456abc"
    }
}
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)  # 添加跨域支持

# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']

model_grow = YOLO('models/paddy-grow.pt')  # load a custom model
model_disease = YOLO('models/paddy-disease.pt')

def mymovefile(srcfile,dstpath):                       # 移动函数
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)                       # 创建路径
        shutil.move(srcfile, dstpath + fname)          # 移动文件
        print ("move %s -> %s"%(srcfile, dstpath + fname))

def allowed_file(filename):
    # 判断文件后缀是否在列表中
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS


@app.route("/userlogin", methods=['POST', "GET"])
def login():
    return_dict = {"code": '200', "id": "","imgurl": "", "message": "",}
    if request.args is None:
        return_dict['code'] = '5004'
        return_dict['message'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    get_data = request.get_json()
    username = get_data.get("username")
    password = get_data.get("password")
    print(username,password)
    rets = userscollection.find_one({"username":username})
    if rets == None:
        return_dict["message"] = "nouser"
    else:
        if password == rets["password"]:
            return_dict["message"] = "pass"
            return_dict["id"] = rets["id"]
            return_dict["imgurl"] = "http://localhost:5000/user_image/" + str(rets["imgurl"])
            return_dict["username"] = rets["username"]
        else:
            return_dict["message"] = "errorpassword"
        
    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/usersignup", methods=['POST', "GET"])
def usersignup():
    return_dict = {"code": '200', "id": "","imgurl": "", "message": "",}
    if request.args is None:
        return_dict['code'] = '5004'
        return_dict['message'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    get_data = request.get_json()
    username = get_data.get("username")
    password = get_data.get("password")
    rets = userscollection.find_one({"username":username})
    if rets == None:
        userscollection.insert_one({"username":username,'password':str(password),'id':str(100000 + userscollection.count_documents({})), 'imgurl':'no.png'})
        return_dict["message"] = "success"
    else:
        return_dict["message"] = "The user already exists"
        
    return json.dumps(return_dict, ensure_ascii=False)

# 上传图片
@app.route("/upload_grow_image", methods=['POST', "GET"])
def uploads():
    if request.method == 'POST':
        file = request.files['file']
        # 检测文件格式
        if file and allowed_file(file.filename):
            # secure_filename方法会去掉文件名中的中文
            file_name = secure_filename(file.filename)
            # 保存图片
            file.save(os.path.join('paddy-server/static/image/grow', file_name))
            return {"code": '200', "data": file_name, "message": "上传成功"}
        else:
            return {"code": '503', "message": "格式错误，仅支持jpg、png、jpeg格式文件"}
    return {"code": '503', "message": "仅支持post方法"}

@app.route("/upload_disease_image", methods=['POST', "GET"])
def uploads_d():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file.save(os.path.join("paddy-server/static/image/disease", file_name))
            return {"code": '200', "data": file_name, "message": "上传成功"}
        else:
            return {"code": '503', "message": "格式错误，仅支持jpg、png、jpeg格式文件"}
    return {"code": '503', "data": "", "message": "仅支持post方法"}

@app.route("/predict_image", methods=['POST', "GET"])
def predict_img():
    print("--- Request Headers ---")
    print(request.headers)
    print("--- Request Data ---")
    print(request.data) # raw request body
    print("--- End Request Info ---")
    return_dict = {"code": '200', "data": "", "message": "",}
    if request.args is None:
        return_dict['code'] = '5004'
        return_dict['message'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    get_data = request.get_json()
    pic_name = get_data.get("imageid")
    modelid = get_data.get("modelid")
    print(modelid)
    if modelid == "1":
        pic_path = os.path.join("static/image/grow/", pic_name) # Corrected path
        print(f"Constructed pic_path: {pic_path}")
        if not os.path.exists(pic_path):
            print(f"Error: File not found at {pic_path}")
            return_dict['code'] = '500'
            return_dict['message'] = f"File not found at {pic_path}"
            return json.dumps(return_dict, ensure_ascii=False)
        results = model_grow(pic_path, save=True)  # predict on an image
        print(f"results[0].save_dir: {results[0].save_dir}") # Log save_dir
        # List files in save_dir to see the actual saved file name
        try:
            saved_files = os.listdir(results[0].save_dir)
            print(f"Files in save_dir ({results[0].save_dir}): {saved_files}")
        except Exception as e:
            print(f"Error listing files in save_dir: {e}")

        # Use the actual saved file name with .jpg extension
        saved_file_name = os.path.splitext(pic_name)[0] + ".jpg"
        mymovefile(os.path.join(results[0].save_dir, saved_file_name),"paddy-server/static/predict_image/grow/")
        xx = results[0].probs.data.tolist()
        print(results[0].names)
        return_dict['data'] = {"names":results[0].names,"speed":results[0].speed,"result":results[0].names[xx.index(max(xx))]}
    else:
        pic_path = os.path.join("static/image/disease/", pic_name) # Corrected path
        print(f"Constructed pic_path for disease: {pic_path}") # Add log
        if not os.path.exists(pic_path): # Add file existence check
            print(f"Error: File not found at {pic_path}")
            return_dict['code'] = '500'
            return_dict['message'] = f"File not found at {pic_path}"
            return json.dumps(return_dict, ensure_ascii=False)

        results = model_disease(pic_path, save=True)  # predict on an image
        print(f"results[0].save_dir for disease: {results[0].save_dir}") # Log save_dir
        # List files in save_dir to see the actual saved file name
        try:
            saved_files = os.listdir(results[0].save_dir)
            print(f"Files in save_dir ({results[0].save_dir}) for disease: {saved_files}")
        except Exception as e:
            print(f"Error listing files in save_dir for disease: {e}")

        # Use the actual saved file name with .jpg extension (assuming it saves as jpg)
        saved_file_name = os.path.splitext(pic_name)[0] + ".jpg"
        mymovefile(os.path.join(results[0].save_dir, saved_file_name),"paddy-server/static/predict_image/disease/")
        print(results[0].boxes)
        return_dict['data'] = {"names":results[0].names,"speed":results[0].speed}
    return_dict['message'] = '预测完成'
    print(f"Returning to Go: {return_dict}") # Log the return dictionary
    return json.dumps(return_dict, ensure_ascii=False)



# 查看图片
@app.route("/show_grow_image/<imageId>")
def get_frame(imageId):
    # 图片上传保存的路径
    with open(r'paddy-server/static/image/grow/{}'.format(imageId), 'rb') as f:
        image = f.read()
        result = Response(image, mimetype="image/jpg")
        return result

@app.route("/show_disease_image/<imageId>")
def get_dframe(imageId):
    # 图片上传保存的路径
    with open(r'paddy-server/static/image/disease/{}'.format(imageId), 'rb') as f:
        image = f.read()
        result = Response(image, mimetype="image/jpg")
        return result

# 查看预测完图片
@app.route("/show_predict_grow_image/<imageId>")
def get_predict_frame(imageId):
    # 图片上传保存的路径
    with open(r'paddy-server/static/predict_image/grow/{}'.format(imageId), 'rb') as f:
        image = f.read()
        result = Response(image, mimetype="image/jpg")
        return result
# 查看预测完图片
@app.route("/show_predict_disease_image/<imageId>")
def get_predict_dframe(imageId):
    # 图片上传保存的路径
    with open(r'paddy-server/static/predict_image/disease/{}'.format(imageId), 'rb') as f:
        image = f.read()
        result = Response(image, mimetype="image/jpg")
        return result
@app.route("/user_image/<imageId>")
def userimg(imageId):
    # 图片上传保存的路径
    with open(r'paddy-server/static/userimg/{}'.format(imageId), 'rb') as f:
        image = f.read()
        result = Response(image, mimetype="image/jpg")
        return result
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5050, debug=True)