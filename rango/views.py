

#from django.shortcuts import render
#from rango.models import Category


#def index(request):


 #   category_list = Category.objects.order_by('-likes')[:5]
 #   context_dict = {'categories': category_list}

 #   return render(request, 'rango/index.html', context=context_dict)


from django.http import HttpResponse
	

def index(request):
	    return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>") 

def about(request):
        return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")