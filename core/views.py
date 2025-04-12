from django.shortcuts import render

def home(request):
    return render(request, 'core/index.html')

#def home(request):
#    return render(request, 'core/contact.html')

#def home(request):
#    return render(request, 'core/about.html')
