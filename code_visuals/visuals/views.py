from django.shortcuts import render, HttpResponse
from . import Debugs


def index(request):
    output = Debugs.main()
    print(output)
    return render(request, 'visuals/index.html', {})
