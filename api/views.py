from django.shortcuts import render
from django.http import HttpResponse
from .models import Word
from django.db.models import Max
import re

def IndexView(request):
	context = {}
	return render(request,'research/indexing.html',context)

def SearchView(request):
	return render(request,'research/searching.html')

def InputTextView(request):
	if request.method == 'POST':
		global idx
		variable = Word.objects.all().aggregate(Max('document_index'))
		idx = variable['document_index__max'] if variable['document_index__max'] else 1
		text = request.POST.get('textfield')
		text = text.lower()
		clean_text = re.sub(r'[^\w\s]','', text)
		clean_text = clean_text.split('\r\n\r\n')
		for item in clean_text:
			mapping = dict()
			regex = re.compile(r'[\n\r\t]')
			item = regex.sub(" ",item)
			words = item.split(' ')
			for word in words:
				if word in mapping:
					word_freq = mapping[word]
				else:
					word_freq = 0
				mapping[word]= word_freq+1

			for word,freq in mapping.items():
				data = Word(document_index=idx,words=word,frequency=freq)
				data.save()
			idx += 1

		context = {}
		return render(request,'research/success.html',context)
	else:
		return HttpResponse("Error.")

def ShowView(request):
	if(request.method=='POST'):
		keyword1 = str(request.POST['textfield'])
		keyword1 = keyword1.lower()
		keyword = keyword1.split()
		res = []
		for item in keyword:
			temp = Word.objects.filter(words = item).order_by('-frequency')[:10]
			if temp:
				res.append(temp)
		flg = False
		if res:
			flg=True
		context = {
		'result':res,
		'flag':flg,
		'search':keyword1
		}
		return render(request,'research/results.html',context)
	else:
		return HttpResponse('Invalid Request')

def ClearView(request):
	Word.objects.all().delete()
	global idx
	idx=1
	return render(request,'research/clear.html')

def HomeView(request):
	return render(request,'research/home.html')
