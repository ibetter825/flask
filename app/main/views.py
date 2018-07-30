from datetime import datetime
from flask import render_template, session, redirect, url_for
 
from . import main
from .forms import NameForm
from .. import db
from ..models import User
 
@main.route('/',methods = ['POST','GET'])   #请求方式不管是post还是get都执行这个视图函数
def index():
    form = NameForm()  #表单实例
    if form.validate_on_submit():   #提交按钮是否成功点击
         # 从数据库中查找和表单数据一样的数据，如果有，取第一个数据
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:   #如果数据库中没有对应的数据
            user = User(username = form.name.data)  #在数据库中对应的表中创建数据
            db.session.add(user)  #加入到用户会话，以便数据库进行提交
            session['known'] = False  #这是一个新用户
            if current_app.config['FLASKY_ADMIN']:  #如果收件人已经定义，则调用发送邮件函数
                send_email(current_app.config['FLASKY_ADMIN'],'New User','mail/new_user',user = user)
                flash('The mail has been sent out')
        else:
            session['known'] = True  #这是一个老用户
        session['name'] = form.name.data   #从表单获取数据
        return redirect(url_for('.index'))
    return render_template('index.html',current_time = datetime.utcnow(),
                           form = form,name=session.get('name'),known