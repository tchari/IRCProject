from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from .financials import PV
from .forms import *
from .models import *

###Error Handling



# Create your views here.
def index(request):
	current_user = request.user
	context = {'user':current_user}
	return render(request, 'IRC/index.html', context)

################################
##Views related to Assessments##
################################
class AssessmentsListView(ListView):
	model = CaseSetup
	
	def get_context_data(self, **kwargs):
		current_user = self.request.user
		context = super(AssessmentsListView, self).get_context_data(**kwargs)
		if current_user.profile.site.name != 'Global':
			context['casesetup_list'] = context['casesetup_list'].filter(site = current_user.profile.site)
			context['object_list'] = context['object_list'].filter(site = current_user.profile.site)
		return context

class AssessmentsDetailView(DetailView):
	model = CaseSetup
	
	def get_context_data(self, **kwargs):
		context = super(AssessmentsDetailView, self).get_context_data(**kwargs)
		
		case = context['casesetup']
		q = ProbabilityOfLoss.objects.get(pk=case.pk)
		dmgAssessments = DamageAssessment.objects.filter(case_id=case.id)
		context['dmgAss'] = dmgAssessments
		context['probabilityLoss'] = q
		
		protections = q.protection.all()
		
		################################################
		#protections_data = q.protection.all().values()
		#newlist = []
		#for i in range(len(protections_data)):
		#	newlist.append([])

		#print("###############")
		#list_data = list(protections_data)
		#print(list_data[0])
		#zz = zip(**list_data)
		#print(list(zz))
		#i=0
		#for prot in protections_data:
		#	for prot_val in prot:
		#		print(str(prot_val)+":"+str(prot[prot_val]))
		#		newlist[i].append(prot[prot_val])
		#	print()
		#	i+=1
		#print(newlist)
		#print("###############")
		##################################################

		###Data manipulation to present the Cost of Protection Information
		label = ['Cost of Protection']
		years = ['Life Expectancy of Equipment (years)']
		annualInterestRate = ['Annual Interest Rate']
		capEx = ['Capital Cost']
		areasServiced = ['Areas Serviced by Equipment']
		totalCapExPerArea = ['Capital Cost for this Area']
		otherCapEx = ['Other Capital Costs']
		annualAmortization = ['Annual Amortized Cost']
		opEx = ['Annual Operating Cost']
		otherOpEx = ['Other Operating Costs']
		annualCostOfProtection = ['Annual Cost of Protection']
		for protection in protections:
			label.append(protection.name)
			years.append(protection.years)
			annualInterestRate.append(protection.annualInterestRate)
			capEx.append(protection.capEx)
			areasServiced.append(protection.areasServiced)
			totalCapExPerArea.append(protection.totalCapExPerArea)
			otherCapEx.append(protection.otherCapEx)
			annualAmortization.append(protection.annualAmortization)
			opEx.append(protection.opEx)
			otherOpEx.append(protection.otherOpEx)
			annualCostOfProtection.append(protection.annualCostOfProtection)			
		context['costOfProtectionList'] = [label, years, annualInterestRate, capEx, areasServiced, totalCapExPerArea, otherCapEx, annualAmortization, opEx, otherOpEx, annualCostOfProtection]

		###Data manipulation to present the Damage Assessment Information
		header = [' ']
		PDAlabel = ['pdalabel']
		valueAtRisk = ['Value At Risk']
		damageToValueRiskRatio = ['Damage to Value at Risk Ratio']
		damageEstimate = ['Total Damage Estimate']
		additionalEscalationDamages = ['Additional Escalation Equipment Damages Estimate']
		subTotalPropertyDamage = ['Sub-total Property Damage Loss']
		BIElabel = ['bielabel']
		adjustmentForSecondaryLosses = ['Adjustment Factor due to Secondary Losses']
		totalDamageCost = ['Total Damage Cost']
		annualPlantBIEValue = ['Annual Plant Business Interruption Value']
		fullProductionDaysLost = ['Full Production Days Lost']
		additionalDaysLost = ['Additional Days Lost']
		totalEquivalentDaysLost = ['Total Equivalent Days Lost']
		directBILoss = ['Direct Business Interruption Loss']
		indirectOrPartialLoss = ['Indirect or Partial Loss']
		otherBIELosses = ['Other BIE Losses']
		totalBIE = ['Total Business Interruption Estimate']
		OLlabel = ['ollabel']		
		thirdPartyPlume = ['Third Party Plume']
		disposalOfMEOH = ['Disposal of MEOH']
		shareholderPartnerRelationship = ['Shareholder and Partner Relationship']
		customerGoodwill = ['Customer Goodwill']
		managementTime = ['Management Time']
		riskToEmergPersonnel = ['Risk to Emergency Personnel']
		otherOLLosses = ['Other Losses']
		totalLosses = []
		for dmgass in dmgAssessments:
			header.append(dmgass.name)
			PDAlabel.append('pdalabel')
			BIElabel.append('bielabel')
			OLlabel.append('OLlabel')
			valueAtRisk.append(dmgass.get_valueAtRisk)
			damageToValueRiskRatio.append(dmgass.damageToValueRiskRatio)
			damageEstimate.append(dmgass.get_damageEstimate)
			additionalEscalationDamages.append(dmgass.additionalEscalationDamages)
			subTotalPropertyDamage.append(dmgass.get_subtotalProperyDmg)
			adjustmentForSecondaryLosses.append(dmgass.adjustmentForSecondaryLosses)
			totalDamageCost.append(dmgass.get_totalDamageCost)
			annualPlantBIEValue.append(dmgass.annualPlantBIEValue)
			fullProductionDaysLost.append(dmgass.fullProductionDaysLost)
			additionalDaysLost.append(dmgass.additionalDaysLost)
			totalEquivalentDaysLost.append(dmgass.get_totalEquidDaysLost)
			directBILoss.append(dmgass.get_directBILoss)
			indirectOrPartialLoss.append(dmgass.indirectOrPartialLoss)
			otherBIELosses.append(dmgass.otherBIELosses)
			totalBIE.append(dmgass.get_totalBIE)
			thirdPartyPlume.append(dmgass.thirdPartyPlume)
			disposalOfMEOH.append(dmgass.disposalOfMEOH)
			shareholderPartnerRelationship.append(dmgass.shareholderPartnerRelationship)
			customerGoodwill.append(dmgass.customerGoodwill)
			managementTime.append(dmgass.managementTime)
			riskToEmergPersonnel.append(dmgass.riskToEmergPersonnel)
			otherOLLosses.append(dmgass.otherOLLosses)
			totalLosses.append(dmgass.get_totalLosses)
		pdalist = [PDAlabel, valueAtRisk, damageToValueRiskRatio, damageEstimate, additionalEscalationDamages, subTotalPropertyDamage, adjustmentForSecondaryLosses, totalDamageCost]
		bielist = [BIElabel, annualPlantBIEValue, fullProductionDaysLost, additionalDaysLost, totalEquivalentDaysLost, directBILoss, indirectOrPartialLoss, otherBIELosses, totalBIE]
		ollist = [OLlabel, thirdPartyPlume, disposalOfMEOH, shareholderPartnerRelationship, customerGoodwill, managementTime, riskToEmergPersonnel, otherOLLosses]
		outlist = [header]
		outlist += pdalist
		outlist += bielist
		outlist += ollist
		context['dmgAssTransposed'] = outlist
		
		LIB_riskBasedLoss = q.freq*totalLosses[0]
		tags = []
		costOfProtectionRow = []
		totalLoss = []
		riskBasedLoss = []
		annLossRed = []
		PVAnnLoss = []
		sum = 0
		for index in range(len(annualCostOfProtection)):
			#print(item)
			costOfProtectionRow.append(annualCostOfProtection[index])
			totalLoss.append(totalLosses[index])
			riskBasedLoss.append(round(q.freq*totalLosses[index],2)) 
			annLossRed.append(round(LIB_riskBasedLoss - q.freq*totalLosses[index],2))
			PVAnnLoss.append(round(PV(LIB_riskBasedLoss - q.freq*totalLosses[index],annualInterestRate[1],years[1]),2))
			tags.append(label[index])
			if type(annualCostOfProtection[index]) != type('a string'):
				sum+=annualCostOfProtection[index]
		
		costOfProtectionRow.append(sum) ##Mixed value
		costOfProtectionRow.insert(1,0)
		costOfProtectionRow[3], costOfProtectionRow[2] = costOfProtectionRow[2], costOfProtectionRow[3]
		tags.append('Mixed')
		tags.insert(1,'Let it Burn')
		tags[3], tags[2] = tags[2], tags[3]
		totalLoss.append(totalLosses[-1])
		totalLoss.insert(0,'Total Losses')
		riskBasedLoss.append(round(q.freq*totalLosses[-1],2))
		riskBasedLoss.insert(0,'Risk Based Loss')
		annLossRed.append(round(LIB_riskBasedLoss - q.freq*totalLosses[-1], 2))
		annLossRed.insert(0,'Annual Loss Reduction with Protection')
		PVAnnLoss.append(round(PV(annLossRed[-1], annualInterestRate[1], years[1]),2))
		PVAnnLoss.insert(0, 'Present Value of Annual Loss Reduction')
		BCR = [1]
		for index in range(2,len(totalLoss)):
			BCR.append(round(PVAnnLoss[index]/costOfProtectionRow[index],2))
		BCR.insert(0,'Benefit-to-Cost Ratio')
		BCR_list = [tags, costOfProtectionRow, totalLoss, riskBasedLoss, annLossRed, PVAnnLoss, BCR]
		context['benefitsCostTable'] = BCR_list
		
		return context

def Assessments_cancel(request):
	if request.method == "POST":
		post = request.POST
		CaseSetup.objects.filter(pk=int(post['case'])).delete()

	return redirect('assessmentsListView')
		
def Assessments_new(request):
	current_user = request.user
	if request.method == "POST": #Not the first time, could be probabilty of loss or dmgass forms.
		post = request.POST
		
		if 'site' in post: #Process the case setup form and present the probability of loss form
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
				
				context = {'present':'probLoss', 'form':probLossForm, 'case_id':caseSetupFormObj.pk}
			else:
				context = {'present': 'caseSetup', 'form': caseSetupFormRet, 'sitename': current_user.profile.site.name}
		
		elif 'freq' in post: #Process the probability of loss form and present the FIRST damage Assessment Form
			probLossFormRet = ProbabilityOfLossForm(post)
			if probLossFormRet.is_valid():
				probLossFormObj = probLossFormRet.save()
				dmgAssCounter = DamageAssessmentCounter(probLoss = probLossFormObj, init = probLossFormObj.numProtections, curVal = probLossFormObj.numProtections)
				dmgAssCounter.save()
				dmgAssForm = DamageAssessmentForm(initial={'case': probLossFormObj.case.pk})		
				name = "Let it Burn"
				context = {'present':'dmgAss', 'form': dmgAssForm, 'name': name, 'case_id':probLossFormObj.case.pk}
			else:
				context ={'present': 'probLoss', 'form': probLossFormRet, 'case_id':probLossFormObj.case.pk}
		
		else: #Process the damage assessment form and present the next damage assesssment form or end
			dmgAssFormRet = DamageAssessmentForm(post)
			if dmgAssFormRet.is_valid():
				dmgAssFormObj = dmgAssFormRet.save(commit=False)
				probLossQuery = ProbabilityOfLoss.objects.get(case = dmgAssFormObj.case.pk)
				query = probLossQuery.protection.all()
				dmgAssCounter = DamageAssessmentCounter.objects.get(probLoss = dmgAssFormObj.case.pk)
				if dmgAssCounter.is_init(): #First damage assessment is Let it Burn
					dmgAssForm = DamageAssessmentForm(initial={'case': dmgAssFormObj.case.pk, 'name': ' '})
					dmgAssFormObj.name = "Let It Burn"
					dmgAssFormObj.save()
					dmgAssCounter.decrement()
					dmgAssCounter.save()
					context = {'present':'dmgAss', 'form': dmgAssForm, 'name':query[dmgAssCounter.curVal], 'case_id':dmgAssFormObj.case.pk}
				elif dmgAssCounter.curVal > -1: #Subsequent assessment forms are given by the protection type
					dmgAssForm = DamageAssessmentForm(initial={'case': dmgAssFormObj.case.pk, 'name': ' '})
					dmgAssFormObj.name = str(query[dmgAssCounter.curVal])
					dmgAssFormObj.save()
					dmgAssCounter.decrement()
					dmgAssCounter.save()
					if dmgAssCounter.curVal < 0:
						name = 'Mixed'
					else:
						name = query[dmgAssCounter.curVal]
					context = {'present':'dmgAss', 'form': dmgAssForm, 'name':name, 'case_id':dmgAssFormObj.case.pk}
				else: #Final 
					##Create Final Report --> Don't forget to calculate MIXED too.
					dmgAssFormObj.name = "Mixed"
					dmgAssFormObj.save()
					return redirect('assessmentsListView')
			else:
				num = post.getlist('numDmgAssRemaining')
				context = {'present':'dmgAss', 'form': dmgAssFormRet, 'name':'unknown'}
	else: #First time, therefore present the user the Case Setup Form
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

