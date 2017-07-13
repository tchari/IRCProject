from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from .forms import *
from .models import *

###Error Handling



# Create your views here.
def index(request):
	context = {}
	return render(request, 'IRC/index.html', context)

################################
##Views related to Assessments##
################################
class AssessmentsListView(ListView):
	model = CaseSetup
	
	def get_context_data(self, **kwargs):
		current_user = self.request.user
		context = super(AssessmentsListView, self).get_context_data(**kwargs)
		print("#####")
		print(context)
		context['casesetup_list'] = context['casesetup_list'].filter(site = current_user.profile.site)
		context['object_list'] = context['object_list'].filter(site = current_user.profile.site)
		print("#####")
		print(context)
		print("#####")
		return context

class AssessmentsDetailView(DetailView):
	model = CaseSetup
	
	def get_context_data(self, **kwargs):
		context = super(AssessmentsDetailView, self).get_context_data(**kwargs)
		
		case = context['casesetup']
		context['probabilityLoss'] = ProbabilityOfLoss(pk=case.pk)
		context['dmgAss'] = DamageAssessment.objects.filter(case_id=case.id)
		return context


def Assessments_new(request):
	global dmgAssCounter
	current_user = request.user
	if request.method == "POST":
		post = request.POST
		
		if 'site' in post: #Process the case setup form and prepare the probability of loss form
			caseSetupFormRet = CaseSetupForm(post)
			if caseSetupFormRet.is_valid():
				caseSetupFormObj = caseSetupFormRet.save()
				init = {
					'value': caseSetupFormObj.unit.value,
					'case': caseSetupFormObj.pk,
					'freq': caseSetupFormObj.unit.freq,
					'siteHistoryAndAge': 1.00,
					'serviceAndEnvironment': 1.00,
					'levelOfPMAndOperatorXP': 1.00, 
					'accessToERAndFirstResponse': 1.00,
				}
				probLossForm = ProbabilityOfLossForm(initial=init)
				
				context = {'present':'probLoss', 'form':probLossForm}
			else:
				context = {'present': 'caseSetup', 'form': caseSetupFormRet, 'sitename': current_user.profile.site.name}
		
		elif 'freq' in post: #ProbabilityLossForm
			probLossFormRet = ProbabilityOfLossForm(post)
			if probLossFormRet.is_valid():
				probLossFormObj = probLossFormRet.save()
				dmgAssForm = DamageAssessmentForm(initial={'case': probLossFormObj.case.pk})		
				dmgAssCounter = probLossFormObj.numProtections
				name = "Let it Burn"
				context = {'present':'dmgAss', 'form': dmgAssForm, 'name': name}
			else:
				context ={'present': 'probLoss', 'form': probLossFormRet}
		
		else: #Damage Assessments#
			dmgAssFormRet = DamageAssessmentForm(post)
			if dmgAssFormRet.is_valid():
				if dmgAssCounter > 0:
					dmgAssCounter -= 1
					dmgAssFormObj = dmgAssFormRet.save()
					dmgAssForm = DamageAssessmentForm(initial={'case': dmgAssFormObj.case.pk})
					probLossQuery = ProbabilityOfLoss.objects.get(case = dmgAssFormObj.case.pk)
					query = probLossQuery.protection.all()
					context = {'present':'dmgAss', 'form': dmgAssForm, 'name':query[dmgAssCounter]}
				else:
					##Create Final Report --> Don't forget to calculate MIXED too.
					dmgAssFormObj = dmgAssFormRet.save()
					caseObj = CaseSetup.objects.get(pk=dmgAssFormObj.case.pk)
					print(caseObj.pk)
					return redirect('assessmentsListView')
			else:
				num = post.getlist('numDmgAssRemaining')
				context = {'present':'dmgAss', 'form': dmgAssFormRet, 'name':'unknown'}
	else:
		caseSetupFormRet = CaseSetupForm(initial={'site':current_user.profile.site})
		context = {'present': 'caseSetup', 'form': caseSetupFormRet, 'sitename': current_user.profile.site.name}
	return render(request, 'IRC/assessment_new.html', context)
		
	
####################################
##End Views related to Assessments##
####################################
	
###############################################
##Views related to the CostOfProtection model##
###############################################
class ProtectionItemsListView(ListView):
	model = CostOfProtection

class ProtectionItemsDetailView(DetailView):
	model = CostOfProtection
	
def ProtectionItem_new(request):
	if request.method == "POST":
		form = CoPForm(request.POST)
		obj = form.save(commit=False)
		obj.save()
		return redirect(obj)
	else:	
		form = CoPForm()
	return render(request, 'IRC/costofprotection_newitem.html', {'form': form})
	
def ProtectionItem_edit(request, pk):
	post = get_object_or_404(CostOfProtection, pk=pk)
	if request.method == "POST":
		form = CoPForm(request.POST, instance=post)
		obj = form.save()
		return redirect(obj)
	else:
		form = CoPForm(instance=post)
	return render(request, 'IRC/costofprotection_edititem.html', {'form': form, 'post': post})
###############################################
##End Views related to CostOfProtection model##
###############################################

###################################
##Views related to the Unit model##
###################################
class UnitsListView(ListView):
	model = Unit

class UnitsDetailView(DetailView):
	model = Unit

def Units_new(request):
	if request.method == "POST":
		form = UnitForm(request.POST)
		obj = form.save(commit=False)
		obj.save()
		return redirect(obj)
	else:	
		form = UnitForm()
	return render(request, 'IRC/unit_new.html', {'form': form})	

def Units_edit(request, pk):
	post = get_object_or_404(Unit, pk=pk)
	if request.method == "POST":
		form = UnitForm(request.POST, instance=post)
		obj = form.save()
		return redirect(obj)
	else:
		form = UnitForm(instance=post)
	return render(request, 'IRC/unit_edit.html', {'form': form, 'post': post})	
#######################################
##End Views related to the Unit model##
#######################################