from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
import json
from functools import wraps
import os
from django.conf import settings
from django_redis import get_redis_connection
redis_conn = get_redis_connection("default")

# Create your views here.


def home(request):
    if request.method == 'GET':
        ret = {}

        # notices = Notice.objects.filter().order_by('-create_time')[:10]
        # notice_list = [{'a_id': notice.id, 'a_title': notice.a_title} for notice in notices]
        # ret['a_list'] = notice_list

        ret['uid'] = request.session.get('uid')

        q = request.GET.get('q')
        if q in ['', None]:
            articles = Article.objects.filter(is_delete=False).order_by('-create_time')[:10]
            ret['articles'] = [{'aid': art.id, 'title': art.title} for art in articles]
            ret['q'] = False
        else:
            articles = Article.objects.filter(is_delete=False,
                                              content__contains=q).order_by('-create_time')[:10]
            ret['articles'] = [{'aid': art.id, 'title': art.title} for art in articles]
            ret['q'] = True

        replies = Reply.objects.filter().order_by('-create_time')[:10]
        ret['replies'] = [{'aid': rep.pid, 'content': rep.content} for rep in replies]

        marks = Article.objects.filter().values("mark")[:10]
        ret['kinds'] = [mark['mark'] for mark in marks]

        return render(request, 'home.html', ret)


def login_check(func):

    @wraps(func)
    def wrapped(request, *args, **kwargs):
        if request.session.get('uid') is None:
            return redirect('/login')

        return func(request, *args, **kwargs)
    return wrapped


def counter(id: int, tp):
    if tp == 'score':
        redis_conn.incr(f'{id}', amount=1)
        c_num = redis_conn.get(f"{id}")
        User.objects.filter(id=id).update(score=c_num)
    else:
        redis_conn.incr(f'article_{id}', amount=1)
        c_num = redis_conn.get(f"article_{id}")
        Article.objects.filter(id=id).update(view_n=c_num)
    return c_num


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        # 验证用户名密码是否正确，然后登陆存入session
        type = request.POST.get('type')
        response = {'msg': '', 'status': False}

        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        if type == 'login':
            user = User.objects.get(user_name=uid, password=pwd)
            if user is not None:
                # 登录成功
                response['status'] = True
                request.session['uid'] = uid
                request.session['user_id'] = user.id
                return HttpResponse(json.dumps(response))
            else:
                # 登录失败
                response['msg'] = '用户名或者密码错误'
                return HttpResponse(json.dumps(response))
        elif type == 'register':
            if uid == '' or pwd == '':
                response['msg'] = '用户名或密码不能为空'
                return HttpResponse(json.dumps(response))
            if len(User.objects.filter(user_name=uid)) != 0:
                response['msg'] = '用户名已被创建'
                return HttpResponse(json.dumps(response))
            else:
                User.objects.create(user_name=uid, password=pwd, score=0)
                response['status'] = True
                request.session['uid'] = uid
                return HttpResponse(json.dumps(response))


def logout_v(request):
    request.session.flush()
    return redirect('/login')


@login_check
def publish(request):
    if request.method == 'GET':
        marks = Article.objects.filter().values("mark")[:10]
        response = {
            'kinds': [mark['mark'] for mark in marks] if len(marks) != 0 else ['All']
        }
        return render(request, 'publish.html', response)
    elif request.method == 'POST':
        uid = request.session['uid']
        user_id = request.session['user_id']

        t_title = request.POST.get('t_title')
        t_introduce = request.POST.get('t_introduce')
        t_content = request.POST.get('t_content')
        t_kind = request.POST.get('t_kind')
        mark = request.POST.get('mark')

        article = Article.objects.create(user_id=user_id, mark=t_kind if mark in ['', None] else mark,
                                         title=t_title, content=t_content,
                                         intro=t_introduce, view_n=0, is_delete=0,
                                         )
        t_id = article.id

        # 存帖子图片
        t_photo = request.FILES.get('t_photo', None)
        t_photo_path = 'static/img/t_photo/' + str(t_id) + '_' + t_photo.name

        if t_photo:
            with open(os.path.join(settings.BASE_DIR, t_photo_path), 'wb') as f:
                for line in t_photo.chunks():
                    f.write(line)

        # 图片路径存入数据库
        Article.objects.filter(id=t_id).update(img='/'+t_photo_path)

        counter(user_id, 'score')
        return redirect('/article/' + str(t_id))


@login_check
def article(request, aid):
    if request.method == 'GET':
        viewn = counter(aid, 'article')
        # 帖子内容
        # 时间类别作者，标题，正文，图片path
        try:
            article_obj = Article.objects.get(id=aid, is_delete=False)
        except Exception as e:
            return redirect('/')

        t_time = article_obj.create_time
        t_kind = article_obj.mark
        t_title = article_obj.title
        t_content = article_obj.content
        t_photo = article_obj.img
        t_uid = article_obj.user_id
        t_introduce = article_obj.intro
        uid = request.session.get('uid')
        user_id = request.session.get('user_id')
        admin_uid = request.session.get('admin_uid')

        response = {
            'tid': aid,
            't_uid': t_uid,
            't_time': t_time,
            't_kind': t_kind,
            't_title': t_title,
            't_content': t_content,
            't_photo': t_photo,
            't_introduce': t_introduce,
            'uid': uid,
            'admin_uid': admin_uid,
            'viewn': viewn.decode('utf8'),
        }

        # 留言内容
        # 留言者，留言时间，留言内容
        replys = Reply.objects.filter(r_type=Reply.REPLY_ARTICLE, pid=aid)
        reply_list = []
        for reply in replys:
            user = User.objects.get(id=reply.user_id)
            single_reply = {
                'u_name': user.user_name,
                'r_uid': reply.user_id,
                'r_time': reply.create_time,
                'r_content': reply.content,
                'r_id': reply.id,
                'r_photo': reply.img,
            }
            reply_list.append(single_reply)
        response['reply_list'] = reply_list

        return render(request, 'single.html', response)


@login_check
def article_del(request, aid):
    user_id = request.session.get('user_id')

    article_obj = Article.objects.get(id=aid, user_id=user_id, is_delete=False)
    if article_obj is None:
        return redirect('/article/' + str(aid))

    Article.objects.filter(id=aid, user_id=user_id).update(is_delete=True)

    return redirect('/')


@login_check
def article_edit(request, aid):
    user_id = request.session.get('user_id')

    article_obj = Article.objects.get(id=aid, user_id=user_id, is_delete=False)
    if article_obj is None:
        return redirect('/article/' + str(aid))

    if request.method == 'GET':
        article_obj = Article.objects.get(id=aid, is_delete=False)
        t_time = article_obj.create_time
        t_kind = article_obj.mark
        t_title = article_obj.title
        t_content = article_obj.content
        t_photo = article_obj.img
        t_uid = article_obj.user_id
        t_introduce = article_obj.intro
        uid = request.session.get('uid')
        user_id = request.session.get('user_id')
        admin_uid = request.session.get('admin_uid')

        response = {
            'tid': aid,
            't_uid': t_uid,
            't_time': t_time,
            't_kind': t_kind,
            't_title': t_title,
            't_content': t_content,
            't_photo': t_photo,
            't_introduce': t_introduce,
            'uid': uid,
            'admin_uid': admin_uid,
        }

        marks = Article.objects.filter().values("mark")[:10]
        response['kinds'] = [mark['mark'] for mark in marks] if len(marks) != 0 else ['All']
        return render(request, 'article_edit.html', response)
    elif request.method == 'POST':
        uid = request.session['uid']
        user_id = request.session['user_id']

        t_title = request.POST.get('t_title')
        t_introduce = request.POST.get('t_introduce')
        t_content = request.POST.get('t_content')
        t_kind = request.POST.get('t_kind')
        mark = request.POST.get('mark')
        e_photo = request.POST.get('e_photo')

        Article.objects.filter(id=aid, user_id=user_id).update(mark=t_kind if mark in ['', None] else mark,
                                                               title=t_title, content=t_content,
                                                               intro=t_introduce, view_n=0,
                                                               )

        t_photo = request.FILES.get('t_photo', None)
        if t_photo is not None:
            t_photo_path = 'static/img/t_photo/' + str(aid) + '_' + t_photo.name

            if t_photo:
                with open(os.path.join(settings.BASE_DIR, t_photo_path), 'wb') as f:
                    for line in t_photo.chunks():
                        f.write(line)

            Article.objects.filter(id=aid).update(img='/' + t_photo_path)

        return redirect('/article/' + str(aid))


@login_check
def reply(request, rtype, pid):
    user_id = request.session.get('user_id')

    r_content = request.POST.get('r_content')

    obj = Reply.objects.create(r_type=rtype, pid=pid, user_id=user_id, content=r_content)

    r_id = str(obj.id)
    r_photo = request.FILES.get('r_photo')
    r_photo_path = ''
    if r_photo:
        # 保存文件
        r_photo_path = 'static/img/r_photo/' + r_id + '_' + r_photo.name
        import os
        f = open(os.path.join(r_photo_path), 'wb')
        for line in r_photo.chunks():
            f.write(line)
        f.close()

    Reply.objects.filter(id=r_id).update(img='/' + r_photo_path)

    counter(user_id, 'score')
    return redirect('/article/' + pid)



@login_check
def edit_info(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        resp = {'user_name': user.user_name,
                'nick_name': user.nick_name,
                'mail': user.mail,
                'intro': user.desc}
        return render(request, 'edit_info.html', resp)
    elif request.method == 'POST':
        uid = request.session.get('uid')
        user_id = request.session.get('user_id')
        user_name = request.POST.get('user_name')
        nick_name = request.POST.get('nick_name')
        mail = request.POST.get('mail')
        intro = request.POST.get('intro')
        old = request.POST.get('old_pwd')
        new1 = request.POST.get('new_pwd1')
        new2 = request.POST.get('new_pwd2')
        if new1 == new2 and len(User.objects.filter(id=user_id, password=old)) != 0:
            # 核对成功，修改密码
            User.objects.filter(id=user_id).update(password=new1, user_name=user_name,
                                                   nick_name=nick_name, mail=mail, desc=intro)
        return redirect('/')


def admin_del(request, aid):
    admin_uid = request.session.get('admin_uid')

    article = Article.objects.filter(aid=aid)
    Article.objects.filter(aid=aid).update(is_delete=False)
    redis_conn.incr(f'{article.user_id}', amount=-2)
    c_num = redis_conn.get(f"{article.user_id}")
    User.objects.filter(id=article.user_id).update(score=c_num)

    return redirect('/')

