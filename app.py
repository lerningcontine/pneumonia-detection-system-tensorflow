from flask import Flask, render_template, request,  redirect, session
from config.Config import db
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)
app.secret_key = '123456'

@app.route('/', methods=['GET', 'POST'])
def index(name=None):
    return render_template('indextt.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # global user_sco
        user_sco = request.form.get('user_name')
        user_passwd = request.form.get('user_passwd')

        if db.check_login(user_sco, user_passwd):
            session['user_sco'] = user_sco
            return redirect('dashboard')
    return render_template('login.html')

@app.route('/res', methods=["GET", "POST"])
def res():
    if request.method == 'POST':
        user_sco = request.form.get('user_name')
        user_passwd = request.form.get('user_passwd')
        user_passwd_q = request.form.get('user_passwd_to')
        name = request.form.get('name')
        address = request.form.get('address')
        sex = request.form.get('sex')
        number = request.form.get('number')
        information = {"user_sco": user_sco, "user_passwd": user_passwd, "name": name, "sex": sex, "address": address, "number": number}
        # print(information)
        if user_passwd_q != user_passwd:
            text = '密码不一致！请重新输入！'
            return render_template('res.html', text=text)

        if user_sco:
            res_result = db.insert(information)

            if res_result:
                return redirect('login')
            else:
                text = '用户已存在！！！'
                return render_template('res.html', text=text)
        else:
            text = '用户名输入为空！！！'
            return render_template('res.html', text=text)


    return render_template('res.html')


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    cates = db.all_cate()
    time_list = []
    for item in cates:
        year = str(item[3].year) + '-' + str(item[3].month) + '-' + str(item[3].day)
        time_list.append(year)

    from collections import Counter
    date_count = Counter(time_list)

    # 去重后的日期列表
    unique_dates = list(set(time_list))
    count_list = []
    for date in unique_dates:
        count_list.append({"date":date,"count":date_count[date]})

    sorted_dict_list = sorted(count_list, key=lambda x: x['date'])
    # print(count_list)
    return render_template('dashboard.html', user=session['user_sco'], count_list=sorted_dict_list, user_length = len(db.all_user()), cate_length = len(db.all_cate()))
#

@app.route('/user_information_control', methods=["GET", "POST"])
def user_information_control():
    user_name = session['user_sco']
    users = db.all_user()
    number = len(users)
    return render_template('table-data-table.html', users=users, number=number, user_name=user_name)

@app.route('/delete_user', methods=["GET", "POST"])
def delete_user():
    if request.method == 'GET':
        user_sco = request.args.get('user_sco')
        result = db.delete(user_sco)
        if result:
            return redirect('user_information_control')
        
        
@app.route('/change_current_user', methods=["GET", "POST"])
def change_current_user():
    users = db.all_user()
    user_sco = session['user_sco']
    if request.method == 'POST':
        # user_sco = request.form.get('user_name')
        user_passwd = request.form.get('user_passwd')
        user_passwd_q = request.form.get('password_confirm')
        name = request.form.get('name')
        address = request.form.get('address')
        sex = request.form.get('sex')
        number = request.form.get('number')
        # print(name)
        # print(user_passwd_q)
        # 用户名是固定的，不能修改
        information = {"user_sco": session['user_sco'], "user_passwd": user_passwd, "name": name, "sex": sex, "address": address,
                       "number": number}
        # print(user_passwd)
        if user_passwd_q != user_passwd:
            text = '密码不一致！请重新输入！'
            for user in users:
                if session['user_sco'] == user[0]:
                    return render_template('form-components.html', text=text, user=user,admin=session['user_sco'])

        result = db.change_user(information)
        if result:
            return redirect('change_current_user')
    # # 先要将信息显示到界面
    users = db.all_user()
    for user in users:
        if session['user_sco'] == user[0]:
            # print(user)
            return render_template('form-components.html', user=user,admin=session['user_sco'])


@app.route('/change_user_information', methods=["GET", "POST"])
def change_user_information():
    user_sco = request.args.get('user_sco')
    if request.method == 'POST':
        user_sco = request.form.get('user_name')
        user_passwd = request.form.get('user_passwd')
        user_passwd_q = request.form.get('user_passwd_to')
        name = request.form.get('name')
        address = request.form.get('address')
        sex = request.form.get('sex')
        number = request.form.get('number')
        # 学号是固定的，不能修改
        information = {"user_sco": user_sco, "user_passwd": user_passwd, "name": name, "sex": sex, "address": address,
                       "number": number}
        print(information)
        if user_passwd_q != user_passwd:
            text = '密码不一致！请重新输入！'
            return render_template('change_user.html', text=text)

        result = db.change_user(information)
        
        if result:
            return redirect('user_information_control')
        return render_template('change_user.html')
    # 先要将信息显示到界面
    users = db.all_user()
    for user in users:
        if user_sco == user[0]:
            return render_template('change_user.html', user=user)


@app.route('/add_user', methods=["GET", "POST"])
def add_user():
    if request.method == 'POST':
        user_sco = request.form.get('user_name')
        user_passwd = request.form.get('user_passwd')
        user_passwd_q = request.form.get('user_passwd_to')
        name = request.form.get('name')
        address = request.form.get('address')
        sex = request.form.get('sex')
        number = request.form.get('number')
        information = {"user_sco": user_sco, "user_passwd": user_passwd, "name": name, "sex": sex, "address": address, "number": number}

        if not user_sco:
            text = '用户已存在！！！'
            return render_template('add_user.html', text=text)

        if user_passwd_q != user_passwd:
            text = '密码不一致！请重新输入！'
            return render_template('add_user.html', text=text)

        if user_sco:
            res_result = db.insert(information)

            if res_result:
                return redirect('user_information_control')
            else:
                text = '用户已存在！！！'
                return render_template('add_user.html', text=text)
        else:
            text = '用户名输入为空！！！'
            return render_template('add_user.html', text=text)
    return render_template('add_user.html')

import os
from werkzeug.utils import secure_filename
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
@app.route('/show_img', methods=["GET", "POST"])
def show_img():
    if 'image' in request.files:
        image = request.files['image']
        filename = secure_filename(image.filename)

        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # 在界面上展示上传的图片
        uploaded_image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        session['images'] = uploaded_image
        
        return render_template('bootstrap-components.html',path=uploaded_image)
    
    return render_template('bootstrap-components.html')


def predict_img(img_path):
    class_names = ['covid', 'normal', 'virus']
    model = tf.keras.models.load_model("models/mobilenet_fv.h5")

    # 加载图像并调整大小
    img_init = cv2.imread(img_path)
    resized_img = cv2.resize(img_init, (224, 224))

    # 将图像数据转换为期望的形状
    img_reshaped = np.reshape(resized_img, (1, 224, 224, 3))

    outputs = model.predict(img_reshaped)  # 将图片输入模型得到结果
    result_index = int(np.argmax(outputs))
    result = class_names[result_index]  # 获得对应的水果名称
    return result

import cv2
@app.route('/detection', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        # 在这里添加图片检测的代码，假设检测结果为result
        # print(session['images'])

        img_init = cv2.imread(session['images'])
        resized_img = cv2.resize(img_init, (224, 224))

        # 保存 resize 后的图像
        cv2.imwrite(session['images'], resized_img)
        result = predict_img(session['images'])
        # print(result)
        information = {'user_sco': session['user_sco'], 'path': session['images'], 'result': result}
        resu = db.insert_cate(information)
        return render_template('bootstrap-components.html', result=result,path=session['images'], user=session['user_sco'])


@app.route('/identify', methods=['GET', 'POST'])
def identify():

    return render_template('bootstrap-components.html', user=session['user_sco'])


@app.route('/show_cate', methods=['GET', 'POST'])
def show_cate():
    all_cate_data = db.all_cate()
    cate_list = []
    for  item in all_cate_data:
        if item[0] == session['user_sco']:
            cate_list.append(item)
    number = len(cate_list)
    # print(cate_list)
    user = session['user_sco']
    return render_template('table-basic.html', data=cate_list,  number=number, user=user)


@app.route('/delete_cate', methods=["GET", "POST"])
def delete_cate():
    if request.method == 'GET':
        user_path = request.args.get('user_path')
        result = db.delect_cate(user_path)
        if result:
            return redirect('show_cate')



@app.route('/change_cate', methods=["GET", "POST"])
def change_cate():
    user_path = request.args.get('user_path')
    if request.method == 'POST':
        user_sco = request.form.get('user_name')
        class_ = request.form.get('class')
        path = request.form.get('path')
        # 学号和路径是固定的，不能修改
        information = {"user_sco": user_sco, "class_": class_, "path": path, "old_path": user_path}
        result = db.change_cate(information)
        if result:
            return redirect('show_cate')
    # # 先要将信息显示到界面
    cates = db.all_cate()
    for cate in cates:
        if user_path == cate[2]:
            return render_template('change_cate.html', cate=cate)
        
if __name__ == '__main__':
    app.debug=True
    app.run()

