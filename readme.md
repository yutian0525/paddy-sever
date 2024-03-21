数据库：mongodb  库名：paddy 集合：users（存放用户信息）
pip：pymongo pytorch ultralytics flask Flask-Cors

接口：
1、/userlogin
post，get
发送：json
username 用户名
password 密码
返回：json
message pass 通过 nouser 无用户 errorpassword 密码错误
id 用户id
imgurl 头像
username 用户名

2、/usersignup
post，get
发送：json
username 用户名
password 密码

3、/upload_grow_image
4、/upload_disease_image
返回：data 文件名

5、/predict_image
modelid 1生长期识别 2疾病识别
imageid 图片名

6、/show_grow_image/<imageId>
/show_disease_image/<imageId>
/show_predict_grow_image/<imageId>
/show_predict_disease_image/<imageId>
/user_image/<imageId>
图片链接