from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from django.http import HttpResponse
from rango.forms import CategoryForm
#from rango.forms import UserForm, UserProfileForm
from rango.forms import PageForm

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,'pages': page_list}

    return render(request, 'rango/index.html', context_dict)

#def register(request):
    # 一个布尔值，告诉模板注册是否成功
    # 一开始设为 False，注册成功后改为 True
#    registered = False
    
    # 如果是 HTTP POST 请求，处理表单数据
#    if request.method == 'POST':
        # 尝试获取原始表单数据
        # 注意，UserForm 和 UserProfileForm 中的数据都需要
#        user_form = UserForm(data=request.POST)
#        profile_form = UserProfileForm(data=request.POST)
        
        # 如果两个表单中的数据是有效的……
#        if user_form.is_valid() and profile_form.is_valid():
            # 把 UserForm 中的数据存入数据库
#            user = user_form.save()
            # 使用 set_password 方法计算密码哈希值
            # 然后更新 user 对象
#            user.set_password(user.password)
#            user.save()

            # 现在处理 UserProfile 实例
            # 因为要自行处理 user 属性，所以设定 commit=False
            # 延迟保存模型，以防出现完整性问题
#            profile = profile_form.save(commit=False)
#            profile.user = user
            # 用户提供头像了吗？
            # 如果提供了，从表单数据库中提取出来，赋给 UserProfile 模型
#            if 'picture' in request.FILES:
#                profile.picture = request.FILES['picture']
            # 保存 UserProfile 模型实例
#            profile.save()
            # 更新变量的值，告诉模板成功注册了
#            registered = True
#        else:
            # 表单数据无效，出错了？
            # 在终端打印问题
#            print(user_form.errors, profile_form.errors)
#    else:
        # 不是 HTTP POST 请求，渲染两个 ModelForm 实例
        # 表单为空，待用户填写
#        user_form = UserForm()
#        profile_form = UserProfileForm()

    # 根据上下文渲染模板
#return render(request,
#              'rango/register.html',
#              {'user_form': user_form,
#              'profile_form': profile_form,
#              'registered': registered})


def show_category(request, category_name_slug):
# 创建上下文字典，稍后传给模板渲染引擎
    context_dict = {}

    try:
        # 能通过传入的分类别名找到对应的分类吗？
        # 如果找不到，.get() 方法抛出 DoesNotExist 异常
        # 因此 .get() 方法返回一个模型实例或抛出异常
        category = Category.objects.get(slug=category_name_slug)
    
        # 检索关联的所有网页
        # 注意，filter() 返回一个网页对象列表或空列表
        pages = Page.objects.filter(category=category)
    
        # 把得到的列表赋值给模板上下文中名为 pages 的键
        context_dict['pages'] = pages
        # 也把从数据库中获取的 category 对象添加到上下文字典中
        # 我们将在模板中通过这个变量确认分类是否存在
        context_dict['category'] = category
    except Category.DoesNotExist:
        # 没找到指定的分类时执行这里
        # 什么也不做
        # 模板会显示消息，指明分类不存在
        context_dict['category'] = None
        context_dict['pages'] = None
    
    # 渲染响应，返回给客户端
    return render(request, 'rango/category.html', context_dict)



def about(request):
    # 打印请求方法，是 GET 还是 POST
    print(request.method)
    # 打印用户名，如未登录，打印“AnonymousUser”
    print(request.user)
    return render(request, 'rango/about.html', {})

def add_category(request):
    form = CategoryForm()
    # 是 HTTP POST 请求吗？
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # 表单数据有效吗？
        if form.is_valid():
            # 把新分类存入数据库
            form.save(commit=True)
            # 保存新分类后可以显示一个确认消息
            # 不过既然最受欢迎的分类在首页
            # 那就把用户带到首页吧
            return index(request)
        else:
            # 表单数据有错误
            # 直接在终端里打印出来
            print(form.errors)
    # 处理有效数据和无效数据之后
    # 渲染表单，并显示可能出现的错误消息
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form, 'category': category}

    return render(request, 'rango/add_page.html', context_dict)
