from django.shortcuts import render

# Create your views here.
def index(request):
	context = {}
	return render(request, 'IRC/index.html', context)
	
def newAssessment(request):
	if request.user.is_authenticated:
		#assessmentList = Assessment.objects.filter(assessor=request.user.id)
		context = {}
	else:
		context = {}

	return render(request, 'IRC/newAssessment.html', context)