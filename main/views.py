from django.shortcuts import render

def home(request):
	context = {
		'app_name': '90minutesZone',
		'nama': 'Tristan Rasheed Satria',  
		'npm': '2406358472',
		'kelas': 'PBP-C' 
	}
	return render(request, 'main/home.html', context)
