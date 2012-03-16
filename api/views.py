from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotAllowed
from django.shortcuts import redirect, get_object_or_404, render

import urllib2

import webnotepad.settings as settings

def open(request):
	if not request.POST:
		return HttpResponseNotAllowed(['POST'])
    if 'url' not in request.POST and 'contents' not in request.POST:
        return HttpResponseBadRequest()

	contents = ""
	if 'url' in request.POST:
		page = urllib2.urlopen(request.POST['url'])
		contents = page.read()
	elif 'contents' in request.POST:
		contents = request.POST['contents']
	return render(request, 'editor.html', {'saveback':False,'contents':contents})
