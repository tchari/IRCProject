from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, legal, landscape 
from math import ceil
from .financials import PV
from .forms import *
from .models import *

###Error Handling
def roundList(inList):
	newList = [ceil(val) for val in inList[1:]]
	newList.insert(0,inList[0])
	return newList

def FormParsing(FormHTML):
	
	q = FormHTML.as_p().split('\n')
	out = []
	for i in q:
		if ("title" and "Site:" and "unit") not in i:
			collect = []
			if "_desc" not in i:
				collect.append(i)
				collect.append(q[q.index(i)+1])
			out.append(collect)
	return out			



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
		tags.insert(1,'Base Case')
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
				name = "Base Case"
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
				if dmgAssCounter.is_init(): #First damage assessment is Base Case
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
		print(form.errors)
		obj = form.save()
		return redirect(obj)
	else:
		form = UnitForm(instance=post)
	return render(request, 'IRC/unit_edit.html', {'form': form, 'post': post})	
#######################################
##End Views related to the Unit model##
#######################################

#################################################
##Views related to the StandardAssessment model##
#################################################

class StandardAssessmentsListView(ListView):
	model = StandardAssessment

class StandardAssessmentsDetailView(DetailView):
	model = StandardAssessment
	
	def get_context_data(self, **kwargs):
		self.request.session['pk'] = self.object.pk
		
		context = super(StandardAssessmentsDetailView, self).get_context_data(**kwargs)
		SA = context['standardassessment']
		label = [' ', 'Base Case', 'Fixed', 'Mobile', 'Fixed and Mobile']
		annCOP = ['Annual Cost of Protection', SA.L_COP_annualCOP, SA.F_COP_annualCOP, SA.M_COP_annualCOP, SA.FM_COP_annualCOP]
		L_TL = SA.L_PDA_total + SA.L_BIE_totalBIE + SA.L_OL_total
		F_TL = SA.F_PDA_total + SA.F_BIE_totalBIE + SA.F_OL_total
		M_TL = SA.M_PDA_total + SA.M_BIE_totalBIE + SA.M_OL_total
		FM_TL = SA.FM_PDA_total + SA.FM_BIE_totalBIE + SA.FM_OL_total
		totalLoss = ['Total Loss', L_TL, F_TL, M_TL, FM_TL]
		PL = ['Probability of Loss', SA.L_PL_freq, SA.F_PL_freq, SA.M_PL_freq, SA.FM_PL_freq]
		RBL = ['Risk Based Loss', SA.L_PL_freq*L_TL, SA.F_PL_freq*F_TL, SA.M_PL_freq*M_TL, SA.FM_PL_freq*FM_TL]
		ALR = ['Annual Loss Reduction with Protection', RBL[1]-RBL[1], RBL[1]-RBL[2], RBL[1]-RBL[3], RBL[1]-RBL[4]]
		BCR = ['Benefit-to-Cost Ratio', 0, round((ALR[2]/annCOP[2])*10)/10, round((ALR[3]/annCOP[3])*10)/10, round((ALR[4]/annCOP[4])*10)/10]
		context['BCR_Table'] = [label, roundList(annCOP), roundList(totalLoss), PL, roundList(RBL), roundList(ALR), BCR]
		context['Summary_Table'] = [['Case Description', SA.summary_CaseDesc],['Base Case', SA.summary_L],['Fixed', SA.summary_F],['Mobile', SA.summary_M],['Fixed and Mobile', SA.summary_FM],['Results', SA.summary_Results],['Assumptions and Options Considered', SA.summary_Ass],['Conclusions', SA.summary_Conc]]

		return context
		#print(context)

def StandardAssessments_new(request):
	if request.method == "POST":
		SAform = StandardAssessmentForm(request.POST)
		if SAform.is_valid():
			SAObj = SAform.save()
			return redirect(SAObj)
		else:
			return render(request, 'IRC/standardassessment_error.html', {'form': SAform})
	else:
		SAform = StandardAssessmentForm()
		return render(request, 'IRC/standardassessment_new.html', {'form': SAform})

def StandardAssessments_edit(request, pk):
	post = get_object_or_404(StandardAssessment, pk=pk)
	if request.method == "POST":
		form = StandardAssessmentForm(request.POST, instance=post)
		SAObj = form.save()
		return redirect(SAObj)
	else:
		form = StandardAssessmentForm(instance=post)
		return render(request, 'IRC/standardassessment_new.html', {'form': form, 'post': post})	

#################################################
##Views related to the StandardAssessment model##
#################################################

####################################
##Views related to exporting a PDF##
####################################

def splitText(text,num):
    if len(text)<num:
    	return [text]
    else:
        outlist = []
        while len(text)>num:
            val = num
            inds = [i for i, x in enumerate(text) if x == " "]
            while val not in inds:
                val -= 1
            outlist.append(text[:val])
            text = text[val+1:]

        outlist.append(text) 
        return outlist

def PDFWriteCell(p, num, font_size, y, label, text):
	#print(text)
	listed_text = splitText(text,num) #[text[i:i+num] for i in range(0, len(text), num)]
	p.setFont("Helvetica-Bold", font_size)
	p.drawString(inch*1, y, label)
	p.setFont("Helvetica", font_size)
	for lines in listed_text:
		#print(len(lines))
		p.drawString(inch*2, y, lines)
		y -= p._leading

	return y

def PDFWriteRow(p, y, label, value, text):
	num = 50
	listed_text = splitText(text, num)
	p.setFont("Helvetica-Bold", 8)
	p.drawString(inch*1, y, label)
	p.setFont("Helvetica", 8)
	#Set the numerical value to be printed
	if value < 0.01:
		value_str = '{:.2e}'.format(value)
	elif value > 100:
		value_str = '${:,}'.format(round(value))
	else:
		value_str = str(value)
	p.drawString(inch*3.5, y, value_str)
	z = 0
	for lines in listed_text:
		z+=1
		p.drawString(inch*4.5, y, lines)
		y -= p._leading

	return y

def newPage(p):
	p.showPage()
	p.drawString(inch*1, inch*10.5, "Name")
	p.drawString(inch*3.5, inch*10.5, "Quantity")
	p.drawString(inch*4.5, inch*10.5, "Comments")
	return inch*10

def writeHeader(p,y,fontSize, text):
	p.setFont("Helvetica", fontSize)
	p.drawString(inch*1, y, text)
	y -= inch*0.25
	p.setFont("Helvetica", 8)	
	return y

def exportPDF(request):

	response = HttpResponse(content_type='application/pdf')
	
	pk = request.session['pk']
	SA = get_object_or_404(StandardAssessment, pk=pk)
	filename_title = str(SA.title)
	filename = "#"+str(SA.number)+": "+filename_title[:20]+".pdf"
	response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
	label = [' ', 'Base Case', 'Fixed', 'Mobile', 'Fixed and Mobile']
	annCOP = roundList(['Annual Cost of Protection', SA.L_COP_annualCOP, SA.F_COP_annualCOP, SA.M_COP_annualCOP, SA.FM_COP_annualCOP])
	L_TL = SA.L_PDA_total + SA.L_BIE_totalBIE + SA.L_OL_total
	F_TL = SA.F_PDA_total + SA.F_BIE_totalBIE + SA.F_OL_total
	M_TL = SA.M_PDA_total + SA.M_BIE_totalBIE + SA.M_OL_total
	FM_TL = SA.FM_PDA_total + SA.FM_BIE_totalBIE + SA.FM_OL_total
	totalLoss = roundList(['Total Loss', L_TL, F_TL, M_TL, FM_TL])
	PL = ['Probability of Loss', SA.L_PL_freq, SA.F_PL_freq, SA.M_PL_freq, SA.FM_PL_freq]
	RBL = roundList(['Risk Based Loss', SA.L_PL_freq*L_TL, SA.F_PL_freq*F_TL, SA.M_PL_freq*M_TL, SA.FM_PL_freq*FM_TL])
	ALR = roundList(['Annual Loss Reduction', RBL[1]-RBL[1], RBL[1]-RBL[2], RBL[1]-RBL[3], RBL[1]-RBL[4]])
	BCR = ['Benefit-to-Cost Ratio', 0, round((ALR[2]/annCOP[2])*10)/10, round((ALR[3]/annCOP[3])*10)/10, round((ALR[4]/annCOP[4])*10)/10]
	
	p = canvas.Canvas(response, pagesize=A4)

	
	titleText = ("Assessment #"+str(SA.number)+"-"+str(SA.title))
	y = PDFWriteCell(p, 50, 16, inch*10.5,'', titleText)
	#p.drawString(inch*1,inch*10.5,titleText)
	p.setFont("Helvetica", 8)
	p.drawString(inch*1,y,"Site: "+str(SA.site))
	y -= 0.2*inch
	p.drawString(inch*1,y,"Unit: "+str(SA.unit))
	y -= 0.3*inch
	y_save = y
	for i,lab in enumerate(label):
		y = y_save
		del_y = inch*0.25
		if i>0:
			p.setFont("Helvetica", 8)
			p.drawString(inch*(i+2), y, str(lab))
			y -= del_y
			p.drawString(inch*(i+2), y, '${:,}'.format(annCOP[i]))
			y -= del_y
			p.drawString(inch*(i+2), y, '${:,}'.format(totalLoss[i]))
			y -= del_y
			p.drawString(inch*(i+2), y, '{:.2e}'.format(PL[i]))
			y -= del_y
			p.drawString(inch*(i+2), y, '${:,}'.format(RBL[i]))
			y -= del_y
			p.drawString(inch*(i+2), y, '${:,}'.format(ALR[i]))
			y -= del_y
			p.drawString(inch*(i+2), y, str(BCR[i]))
			y -= del_y
		else:
			p.setFont("Helvetica-Bold", 8)
			p.drawString(inch*(i+1), y, str(lab))
			y -= del_y
			p.drawString(inch*(i+1), y, str(annCOP[i]))
			y -= del_y
			p.drawString(inch*(i+1), y, str(totalLoss[i]))
			y -= del_y
			p.drawString(inch*(i+1), y, str(PL[i]))
			y -= del_y
			p.drawString(inch*(i+1), y, str(RBL[i]))
			y -= del_y
			p.drawString(inch*(i+1), y, str(ALR[i]))
			y -= del_y
			p.drawString(inch*(i+1), y, str(BCR[i]))
			y -= del_y

	y_sectionSpacing = 0.1*inch
	y = PDFWriteCell(p, 100, 8, y-0.25*inch, 'Case Description', SA.summary_CaseDesc)-y_sectionSpacing
	y = PDFWriteCell(p, 100, 8, y, 'Base Case', SA.summary_L)-y_sectionSpacing
	y = PDFWriteCell(p, 100, 8, y, 'Fixed', SA.summary_F)-y_sectionSpacing
	y = PDFWriteCell(p, 100, 8, y, 'Mobile', SA.summary_M)-y_sectionSpacing
	y = PDFWriteCell(p, 100, 8, y, 'Fixed and Mobile', SA.summary_FM)-y_sectionSpacing
	y = PDFWriteCell(p, 100, 8, y, 'Results', SA.summary_Results)-y_sectionSpacing
	y = PDFWriteCell(p, 100, 8, y, 'Assumptions', SA.summary_Ass)-y_sectionSpacing
	y = PDFWriteCell(p, 100, 8, y, 'Conclusions', SA.summary_Conc)-y_sectionSpacing
	
	p.showPage()
	titleText = 'Detailed Report'
	y = PDFWriteCell(p, 50, 16, inch*10.5,'', titleText)
	#y = inch*10.75+y_sectionSpacing
	fields, verboseNames = zip(*[(f.name, f.verbose_name) for f in StandardAssessment._meta.get_fields()])
	ind = 5
	header = False
	subheader = False
	cur_subheader = ''
	cur_header = ''
	del_y = 0.25*inch
	spacer_multiplier = 1
	header_fontsize = 14
	subheader_fontsize = 10
	while ind < (len(fields)-8):
		name = fields[ind]
		change_header = bool(cur_header not in name) #the current field name is not part of the current header. Change the header
		change_subheader = bool(cur_subheader not in name[:2])
		if not header:
			if 'PL_' in name:
				y = writeHeader(p,y-del_y,header_fontsize,"Probability of Loss")
				cur_header = 'PL_'
			elif 'PDA_' in name:
				y = writeHeader(p,y-del_y,header_fontsize,"Physical Damage Assessment")
				cur_header = 'PDA_'
			elif 'BIE_' in name:
				y = writeHeader(p,y-del_y,header_fontsize,"Business Interruption Estimate")
				cur_header = 'BIE_'
			elif 'OL_' in name:
				y = writeHeader(p,y-del_y,header_fontsize,"Other Losses")
				cur_header = 'OL_'
			elif 'COP_' in name:
				y = writeHeader(p,y-del_y,header_fontsize,"Cost of Protection")
				y = PDFWriteRow(p, y, verboseNames[ind], getattr(SA, fields[ind]), '')-y_sectionSpacing*spacer_multiplier
				y = PDFWriteRow(p, y, verboseNames[ind+1], getattr(SA, fields[ind+1]), '')-y_sectionSpacing*spacer_multiplier
				ind += 2
				cur_header = 'COP_'
			else:
				print("Unknown header")
				cur_header = 'UNK_'
			header = True
		elif not subheader:
			if 'L_' in name[:2]:
				y = writeHeader(p,y,subheader_fontsize,"Base Case")
				cur_subheader = 'L_'
			elif 'F_' in name[:2]:
				y = writeHeader(p,y-y_sectionSpacing*1.25,subheader_fontsize,"Fixed")
				cur_subheader = 'F_'
			elif 'M_' in name[:2]:
				y = writeHeader(p,y-y_sectionSpacing*1.25,subheader_fontsize,"Mobile")
				cur_subheader = 'M_'
			elif 'FM' in name[:2]:
				y = writeHeader(p,y-y_sectionSpacing*1.25,subheader_fontsize,"Fixed and Mobile")
				cur_subheader = 'FM'
			else:
				print(fields[ind])
				ind += 2
			subheader = True
		elif change_header:
			header = False
		elif change_subheader:
			subheader = False			
		else:
			value = getattr(SA, fields[ind])
			text = getattr(SA, fields[ind+1])
			if verboseNames[ind] == 'COP lifeTime':
				ind += 1
			elif verboseNames[ind] == 'COP interestRate':
				ind += 1
			else:
				y = PDFWriteRow(p, y, verboseNames[ind], value, text)-y_sectionSpacing*spacer_multiplier
				ind +=2

			if y<inch:
				y = newPage(p)
		
	p.save()
	return response
