

from django.shortcuts import render

# Create your views here.

def index(request):
    # 构建一个字典，作为上下文传给模板引擎
    # 注意，boldmessage 键对应于模板中的 {{ boldmessage }}
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    # 返回一个渲染后的响应发给客户端
    # 为了方便，我们使用的是 render 函数的简短形式
    # 注意，第二个参数是我们想使用的模板
    return render(request, 'rango/index.html', context=context_dict)