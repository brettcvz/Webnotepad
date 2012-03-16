from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotAllowed
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

import random,string
import urllib
import base64

from models import *

def index(request):
	doc = Document()
	doc.contents = """This is a document -- you can type whatever you want here!

When you save, the file will be stored on this server and available to anyone with the link. Note that this editor isn't built for collaboration, so be careful if someone else is editing this file at the same time!

Enjoy. Webnotepad was created in December 2011 by Brett van Zuiden"""
	doc.contents = base64.b64encode(doc.contents)

	doc.docid = getDocId()
	doc.save()

	return redirect("/webnotepad/open/?docid=%s" % (doc.docid))

def getDocId():
	docid = ''.join(random.choice(string.letters+string.digits) for i in xrange(32))
	#in case of collisions
	while Document.objects.filter(docid=docid).count() > 0:
		docid = ''.join(random.choice(string.letters+string.digits) for i in xrange(32))
	return docid

def open(request):
	if not request.GET:
		return HttpResponseNotAllowed(['GET'])
	if 'docid' not in request.GET:
		return HttpResponseBadRequest()
	doc = get_object_or_404(Document,docid=request.GET['docid'])

	contents = base64.b64decode(doc.contents)
	return render(request, 'editor.html', {'contents':contents, 'docid': doc.docid, 'filename': doc.filename})

@csrf_exempt
def save(request):
	if not request.POST:
		return HttpResponseNotAllowed(['POST'])
	if 'docid' not in request.POST or 'contents' not in request.POST:
		return HttpResponseBadRequest()

	doc = get_object_or_404(Document,docid=request.POST['docid'])

	contents = request.POST['contents']
	doc.contents = base64.b64encode(contents)
	doc.save()

	if doc.saveback_url:
		data = {'saveback_id': doc.saveback_id,
				'contents': contents}
		data = urllib.urlencode(data)
		response = urllib.urlopen(doc.saveback_url, data)
		return HttpResponse(response.read())
	else:
		return HttpResponse("Saved Successfully")

@csrf_exempt
def import_file(request):
	if not request.POST:
		return HttpResponseNotAllowed(['POST'])
	if 'url' not in request.POST and 'contents' not in request.POST:
		return HttpResponseBadRequest()

	doc = Document()
	doc.docid = getDocId()
	if 'url' in request.POST:
		page = urllib.urlopen(request.POST['url'])
		doc.contents = page.read()
	elif 'contents' in request.POST:
		doc.contents = request.POST['contents']
	#because we might have binary data
	doc.contents = base64.b64encode(doc.contents)
	
	if 'saveback_url' in request.POST:
		doc.saveback_url = request.POST['saveback_url']
	if 'saveback_id' in request.POST:
		doc.saveback_id = request.POST['saveback_id']

	if 'filename' in request.POST:
		doc.filename = request.POST['filename']

	doc.save()

	return HttpResponse('http://triple-t.mit.edu/webnotepad/open?docid=%s' % (doc.docid))
