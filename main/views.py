from django.shortcuts import render

def home(request):
	context = {
		'app_name': '90minutesZone',
		'nama': 'Tristan Rasheed Satria',  
		'kelas': 'PBP-C' 
	}
	return render(request, 'main/home.html', context)
