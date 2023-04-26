from django.shortcuts import render, HttpResponse, redirect
import requests
from lxml import etree
from app01.models import Department, UserInfo


# Create your views here.
def index(request):
    return HttpResponse('欢迎使用')


def user_list(request):
    # 若settings.py文件中58没有定义默认模板目录，则去app目录下的templates目录寻找html文件（根据app注册顺序逐一寻找）
    return render(request, 'user_list.html')


def user_add(request):
    return HttpResponse('添加用户')


def tpl(request):
    name = 'Tom'
    roles = ['管理员', 'CEO', '保安']
    user_info = {'name': 'Tom', 'salary': 100000, 'role': '保安'}
    data_list = [{'name': 'Tom', 'salary': 100000, 'role': '保安'},
                 {'name': 'Jerry', 'salary': 200000, 'role': 'CEO'},
                 {'name': 'Tony', 'salary': 100, 'role': 'CTO'},
                 ]

    return render(request, 'tpl.html', {'n1': name, 'n2': roles, 'n3': user_info, 'n4': data_list})


def movies(request):

    # 请求头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    # 使用列表生成式表示10个页面地址
    urls = ['https://movie.douban.com/top250?start={}&filter='.format(str(i*25)) for i in range(10)]
    count = 0
    movie_list = []

    # 获取列表第一个元素，豆瓣top250爬出来是个列表
    def get_first_text(lis):
        try:
            return lis[0].strip()
        except IndexError:
            return ""


    for url in urls:
        res = requests.get(url=url, headers=headers)  # 发起请求
        html = etree.HTML(res.text)  # 将返回的文本加工为可以解析的html
        lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li')  # 获取每个电影的li元素
        # 解析数据
        for li in lis:
            title = get_first_text(li.xpath('./div/div[2]/div[1]/a/span[1]/text()'))  # 电影标题
            src = get_first_text(li.xpath('./div/div[2]/div[1]/a/@href'))  # 电影链接
            dictor = get_first_text(li.xpath('./div/div[2]/div[2]/p[1]/text()'))  # 导演及演员
            score = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[2]/text()'))  # 评分
            comment = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[4]/text()'))  # 评分人数
            summary = get_first_text(li.xpath('./div/div[2]/div[2]/p[2]/span/text()'))  # 电影简介
            count += 1
            movie_list.append(str(count) + ' ' + str(title) + '(' + str(src) + ') ' + str(dictor) + '  评分：' + str(
                score) + ' ' + str(comment) + ' \'' + str(summary)+'\'')

    return render(request, 'movies.html', {'top250': movie_list})


def request_and_response(request):
    # request是一个对象，封装了用户发送过来的请求相关数据

    # 获取请求方式
    print(request.method)
    # 在url上传递值 /something/?n1=123&n2=999
    print(request.GET)
    # 请求体中提交数据
    print(request.POST)

    # HttpResponse('dsad'),字符串内容返回给请求者
    #return HttpResponse('返回内容')

    # 读取HTML内容 + 渲染（替换） -> 字符串，返回给用户浏览器
    #return render(request,'xxx.html',{'title':'xxx'})

    # 【响应】让浏览器重定向到其他页面,请求者自己再去访问baidu.com
    return redirect('https://www.baidu.com')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    # 如果是post请求，获取用户提交的数据
    print(request.POST)
    username = request.POST.get('user')
    password = request.POST.get('pwd')
    if username == 'root' and password == '123456':
        #return HttpResponse('登陆成功')
        return redirect('https://www.baidu.com')

    return render(request, 'login.html', {'error_msg':'登陆失败,用户名或密码错误'})


def orm(request):
    # 测试orm操作数据库表中的数据
    # 1.新建数据
    # Department.objects.create(title='销售部')
    # Department.objects.create(title='IT部门')
    # Department.objects.create(title='运营部')
    # UserInfo.objects.create(name='tom', password='123', age='12')
    # UserInfo.objects.create(name='tony', password='321', age='21')
    # UserInfo.objects.create(name='mary', password='234', age='34')

    # 2.删除数据
    # UserInfo.objects.filter(id=3).delete()  # 删除userinfo表中id等于3的数据
    # UserInfo.objects.all().delete()  # 删除userinfo表中所有数据

    # 3.获取数据
    # data_list = [（行）对象，（行）对象，...]  Queryset类型
    # data_list = UserInfo.objects.all()
    # for obj in data_list:
    #     print(obj.id, obj.name, obj.password, obj.age)
    # 获取第一条数据对象
    # row_obj = UserInfo.objects.filter(id=1).first()
    # print(row_obj.id, row_obj.name, row_obj.age, row_obj.password)

    # 4.更新数据
    #UserInfo.objects.all().update(password='999') # 更新所有password数据
    #UserInfo.objects.filter(id=1).update(password='999')
    UserInfo.objects.filter(name='tom').update(password='596')


    return HttpResponse('数据库更改成功')


def info_list(request):

    user_obj = UserInfo.objects.all()

    return render(request,'info_list.html',{'user_list':user_obj})


def add_info(request):
    if request.method == 'GET':
        return render(request,'add_info.html')
    name = request.POST.get('name')
    password = request.POST.get('password')
    age = request.POST.get('age')

    UserInfo.objects.create(name=name, password=password, age=int(age))

    return redirect('/system/list')


def del_info(request):
    nid = request.GET.get("nid")
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/system/list')
