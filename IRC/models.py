#Django Imports
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
#Other Imports
from .financials import PMT
from decimal import Decimal

class Site(models.Model):
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(
		User, 
		on_delete=models.CASCADE)
	site = models.ForeignKey(
		Site,
		on_delete=models.CASCADE
	)
	
	#@receiver(post_save, sender=User)
	#def create_user_profile(sender, instance, created, **kwargs):
	#	if created:
	#		Profile.objects.create(user=instance)
	
	#@receiver(post_save, sender=User)
	#def save_user_profile(sender, instance, **kwargs):
	#	instance.profile.save()

class Unit(models.Model):
	name = models.CharField(max_length=200)
	basis = models.CharField(max_length=200)
	link = models.CharField(max_length=200)
	freq = models.DecimalField(max_digits=8, decimal_places=8)
	value = models.DecimalField(max_digits=14, decimal_places=2)
	
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('unitsDetailView', args=[str(self.pk)])

class AssessmentType(models.Model):
	type = models.CharField(max_length=200)
	
	def __str__(self):
		return self.type
		
		
class CostOfProtection(models.Model):
	name = models.CharField(max_length=200)
	type = models.ForeignKey(
		AssessmentType,
		on_delete=models.CASCADE
	)
	years = models.PositiveSmallIntegerField()
	annualInterestRate = models.DecimalField(max_digits=4, decimal_places=2)
	capEx = models.DecimalField(max_digits=14, decimal_places=2)
	areasServiced = models.PositiveSmallIntegerField()
	otherCapEx = models.DecimalField(max_digits=14, decimal_places=2)
	opEx = models.DecimalField(max_digits=14, decimal_places=2)
	otherOpEx = models.DecimalField(max_digits=14, decimal_places=2)
	
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('protectionItemsDetailView', args=[str(self.pk)])
	
	@property
	def totalCapExPerArea(self):
		return round((self.capEx/self.areasServiced),2)
	
	@property
	def annualAmortization(self):
		#(P, r, n)
		return round(PMT(self.totalCapExPerArea+self.otherCapEx, self.annualInterestRate, self.years),2)

	@property
	def annualCostOfProtection(self):
		return round((self.annualAmortization + self.opEx + self.otherOpEx),2)		
		
class CaseSetup(models.Model):
	site = models.ForeignKey(
		Site,
		on_delete=models.CASCADE,
		)
	desc = models.CharField(max_length=200)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	unit = models.ForeignKey(
		Unit,
		on_delete=models.CASCADE
	)
	type = models.ForeignKey(
		AssessmentType,
		on_delete=models.CASCADE
	)
	

	def __str__(self):
		return str(self.site)

		
	def name(self):
		return str(self.site) + " - " + str(self.unit)
		
	def get_absolute_url(self):
		return reverse('assessmentsDetailView', args=[str(self.pk)])

class ProbabilityOfLoss(models.Model):
	case = models.OneToOneField(
		CaseSetup,
		on_delete=models.CASCADE,
		primary_key=True
	)
	
	freq = models.DecimalField(max_digits=8, decimal_places=8)
	siteHistoryAndAge = models.DecimalField(max_digits=3, decimal_places=2)
	serviceAndEnvironment = models.DecimalField(max_digits=3, decimal_places=2)
	levelOfPMAndOperatorXP = models.DecimalField(max_digits=3, decimal_places=2)
	accessToERAndFirstResponse = models.DecimalField(max_digits=3, decimal_places=2)
	value = models.DecimalField(max_digits=14, decimal_places=2)
	
	protection = models.ManyToManyField(CostOfProtection)
	
	@property
	def numProtections(self):
		return self.protection.count()
	
	def __str__(self):
		return str(self.case.site)

class DamageAssessment(models.Model):
	case = models.ForeignKey(
		CaseSetup,
		on_delete=models.CASCADE
	)
	name = models.CharField(max_length=200)
	#PDA
	damageToValueRiskRatio = models.DecimalField(max_digits=3, decimal_places=2)
	#Damage Estimate = valueAtRisk*damageToValueRiskRatio
	additionalEscalationDamages = models.DecimalField(max_digits=14, decimal_places=2)
	#Sub-total property damage = Damage Estimate + additionalEscalationDamages
	adjustmentForSecondaryLosses = models.DecimalField(max_digits=4, decimal_places=2)
	#Total Damage Cost = Sub-total property damage + adjustmentForSecondaryLosses
	
	#BIE
	annualPlantBIEValue = models.DecimalField(max_digits=14, decimal_places=2)
	fullProductionDaysLost = models.PositiveSmallIntegerField()
	additionalDaysLost = models.PositiveSmallIntegerField()
	#Total Equivalent Production Days Lost = fullProductionDaysLost + additionalDaysLost
	#Direct BI loss = annualPlantBIEValue*(totalProdDaysLost/365)
	indirectOrPartialLoss = models.DecimalField(max_digits=14, decimal_places=2)
	otherBIELosses = models.DecimalField(max_digits=14, decimal_places=2)
	#Total BIE = Direct BI Loss + indirectOrPartialLoss + otherLosses
	
	#OL
	thirdPartyPlume = models.DecimalField(max_digits=14, decimal_places=2)
	disposalOfMEOH = models.DecimalField(max_digits=14, decimal_places=2)
	shareholderPartnerRelationship = models.DecimalField(max_digits=14, decimal_places=2)
	customerGoodwill = models.DecimalField(max_digits=14, decimal_places=2)
	managementTime = models.DecimalField(max_digits=14, decimal_places=2)
	riskToEmergPersonnel = models.DecimalField(max_digits=14, decimal_places=2)
	otherOLLosses = models.DecimalField(max_digits=14, decimal_places=2)
	
	def __str__(self):
		return str(self.case.site)
	#PDA calcs
	@property
	def get_valueAtRisk(self):
		probLoss = ProbabilityOfLoss.objects.get(pk=self.case.pk)
		return probLoss.value
	@property
	def get_damageEstimate(self):
		return round(self.get_valueAtRisk*self.damageToValueRiskRatio,2)
	@property
	def get_subtotalProperyDmg(self):
		return self.get_damageEstimate + self.additionalEscalationDamages
	@property
	def get_totalDamageCost(self):
		return round(self.get_subtotalProperyDmg*self.adjustmentForSecondaryLosses,2)
	@property
	def get_secLossesType(self):
		print(type(self.get_subtotalProperyDmg))
		return 1
	#BIE calcs
	@property
	def get_totalEquidDaysLost(self):
		return self.fullProductionDaysLost + self.additionalDaysLost
	@property
	def get_directBILoss(self):
		return round((self.annualPlantBIEValue*(Decimal(self.get_totalEquidDaysLost)/365)),2)
	@property
	def get_totalBIE(self):
		return self.get_directBILoss + self.indirectOrPartialLoss + self.otherBIELosses

	#OL calcs
	@property
	def get_totalOL(self):
		return self.thirdPartyPlume + self.disposalOfMEOH + self.shareholderPartnerRelationship + self.customerGoodwill + self.managementTime + self.riskToEmergPersonnel + self.otherOLLosses

	@property
	def get_totalLosses(self):
		return self.get_totalDamageCost+self.get_totalBIE+self.get_totalOL
		
class DamageAssessmentCounter(models.Model):
	probLoss = models.OneToOneField(
			ProbabilityOfLoss,
			on_delete=models.CASCADE,
			editable=False,
			default=1
		)
	init = models.PositiveSmallIntegerField()
	curVal = models.SmallIntegerField()

	def decrement(self):
		self.curVal = self.curVal-1
		if self.curVal < self.init:
			return 1
		else:
			return 0

	def is_init(self):
		if self.curVal == self.init:
			return True
		else:
			return False

	def __str__(self):
		return str(self.curVal)


class StandardAssessment(models.Model):

	def get_absolute_url(self):
		return reverse('SADetailView', args=[str(self.pk)])

	def __str__(self):
		return str(self.title)

	CHARFIELD_MAXLENGTH = 200
	DECIMALFIELD_BILLION = 10
	DECIMALFIELD_ONES = 1
	DECIAMLFIELD_THOUSANDS = 4
	DECIMALFIELD_TRILLION = 13
	DECIMALFIELD_NANO = 9
	DECIMALFIELD_MILLI = 3
	DECIMALFIELD_NODECIMAL = 0
	DECIMALFIELD_CENTS = 2
	DAYSINAYEAR = Decimal(365)
	title = models.TextField(max_length=CHARFIELD_MAXLENGTH)
	site = models.CharField(max_length=CHARFIELD_MAXLENGTH)
	unit = models.CharField(max_length=CHARFIELD_MAXLENGTH)

	###Probability of Loss###
	L_PL_adjCopy= models.PositiveIntegerField(verbose_name = "# of Similar Equipment")
	L_PL_adjCopy_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)	
	L_PL_baseFreq = models.DecimalField(max_digits=DECIMALFIELD_NANO, decimal_places=DECIMALFIELD_NANO, verbose_name = "Base Probability of Loss")
	L_PL_baseFreq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_PL_adjFreq= models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI), decimal_places=DECIMALFIELD_MILLI, verbose_name = "Probability Adjustment Factor")
	L_PL_adjFreq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_PL_freq = models.DecimalField(max_digits=DECIMALFIELD_NANO, decimal_places=DECIMALFIELD_NANO, verbose_name = "Adjusted Probability of Loss")
	L_PL_freq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)	
	
	F_PL_adjCopy= models.PositiveIntegerField(verbose_name = "# of Similar Equipment")
	F_PL_adjCopy_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)	
	F_PL_baseFreq = models.DecimalField(max_digits=DECIMALFIELD_NANO, decimal_places=DECIMALFIELD_NANO, verbose_name = "Base Probability of Loss")
	F_PL_baseFreq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_PL_adjFreq= models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI), decimal_places=DECIMALFIELD_MILLI, verbose_name = "Probability Adjustment Factor")
	F_PL_adjFreq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_PL_freq = models.DecimalField(max_digits=DECIMALFIELD_NANO, decimal_places=DECIMALFIELD_NANO, verbose_name = "Adjusted Probability of Loss")
	F_PL_freq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	
	M_PL_adjCopy= models.PositiveIntegerField(verbose_name = "# of Similar Equipment")
	M_PL_adjCopy_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_PL_baseFreq = models.DecimalField(max_digits=DECIMALFIELD_NANO, decimal_places=DECIMALFIELD_NANO, verbose_name = "Base Probability of Loss")
	M_PL_baseFreq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_PL_adjFreq= models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI), decimal_places=DECIMALFIELD_MILLI, verbose_name = "Probability Adjustment Factor")
	M_PL_adjFreq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_PL_freq = models.DecimalField(max_digits=DECIMALFIELD_NANO, decimal_places=DECIMALFIELD_NANO, verbose_name = "Adjusted Probability of Loss")
	M_PL_freq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)	
	
	FM_PL_adjCopy= models.PositiveIntegerField("# of Similar Equipment")
	FM_PL_adjCopy_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_PL_baseFreq = models.DecimalField(max_digits=DECIMALFIELD_NANO, decimal_places=DECIMALFIELD_NANO, verbose_name = "Base Probability of Loss")
	FM_PL_baseFreq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_PL_adjFreq= models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI), decimal_places=DECIMALFIELD_MILLI, verbose_name = "Probability Adjustment Factor")
	FM_PL_adjFreq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_PL_freq = models.DecimalField(max_digits=DECIMALFIELD_NANO, decimal_places=DECIMALFIELD_NANO, verbose_name = "Adjusted Probability of Loss")
	FM_PL_freq_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)

	###Physical Damage Assessment###
	L_PDA_valueAtRisk = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Value at Risk")
	L_PDA_valueAtRisk_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_PDA_dmgFactor = models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI), decimal_places=DECIMALFIELD_MILLI, verbose_name = "Damage Spread Factor")
	L_PDA_dmgFactor_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_PDA_addDmgs = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Additional Damage")
	L_PDA_addDmgs_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_PDA_subTotalDmgs = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Damage Subtotal")
	L_PDA_subTotalDmgs_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_PDA_adjFactor = models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI),decimal_places=DECIMALFIELD_MILLI, verbose_name = "Secondary Damage Adjustment Factor")
	L_PDA_adjFactor_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_PDA_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Other Damage Costs")
	L_PDA_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_PDA_total = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Total Damage Cost")
	L_PDA_total_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	
	F_PDA_valueAtRisk = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Value at Risk")
	F_PDA_valueAtRisk_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_PDA_dmgFactor = models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI), decimal_places=DECIMALFIELD_MILLI, verbose_name = "Damage Spread Factor")
	F_PDA_dmgFactor_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_PDA_addDmgs = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Additional Damage")
	F_PDA_addDmgs_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_PDA_subTotalDmgs = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Damage Subtotal")
	F_PDA_subTotalDmgs_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_PDA_adjFactor = models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI),decimal_places=DECIMALFIELD_MILLI, verbose_name = "Secondary Damage Adjustment Factor")
	F_PDA_adjFactor_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_PDA_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Other Damage Costs")
	F_PDA_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_PDA_total = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Total Damage Cost")
	F_PDA_total_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	
	M_PDA_valueAtRisk = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Value at Risk")
	M_PDA_valueAtRisk_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_PDA_dmgFactor = models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI), decimal_places=DECIMALFIELD_MILLI, verbose_name = "Damage Spread Factor")
	M_PDA_dmgFactor_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_PDA_addDmgs = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Additional Damage")
	M_PDA_addDmgs_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_PDA_subTotalDmgs = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Damage Subtotal")
	M_PDA_subTotalDmgs_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_PDA_adjFactor = models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI),decimal_places=DECIMALFIELD_MILLI, verbose_name = "Secondary Damage Adjustment Factor")
	M_PDA_adjFactor_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_PDA_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Other Damage Costs")
	M_PDA_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_PDA_total = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Total Damage Cost")
	M_PDA_total_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	
	FM_PDA_valueAtRisk = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Value at Risk")
	FM_PDA_valueAtRisk_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_PDA_dmgFactor = models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI), decimal_places=DECIMALFIELD_MILLI, verbose_name = "Damage Spread Factor")
	FM_PDA_dmgFactor_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_PDA_addDmgs = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Additional Damage")
	FM_PDA_addDmgs_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_PDA_subTotalDmgs = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Damage Subtotal")
	FM_PDA_subTotalDmgs_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_PDA_adjFactor = models.DecimalField(max_digits=(DECIMALFIELD_ONES+DECIMALFIELD_MILLI),decimal_places=DECIMALFIELD_MILLI, verbose_name = "Secondary Damage Adjustment Factor")
	FM_PDA_adjFactor_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_PDA_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Other Damage Costs")
	FM_PDA_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_PDA_total = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Total Damage Cost")
	FM_PDA_total_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)

	###Business Interruption Estimate###
	L_BIE_annBIEValue = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Daily Business Interruption Value")
	L_BIE_annBIEValue_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_BIE_fullProdDaysLost = models.PositiveIntegerField(verbose_name = "Full Equivalent Production Days Lost")
	L_BIE_fullProdDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_BIE_addProdDaysLost= models.PositiveIntegerField(verbose_name = "Additional Equivalent Production Days Lost")
	L_BIE_addProdDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_BIE_totalDaysLost= models.PositiveIntegerField(verbose_name = "Total Equivalent Production Days Lost")
	L_BIE_totalDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_BIE_directBILoss = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Direct Business Interruption Loss")
	L_BIE_directBILoss_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_BIE_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Other Business Interruption Losses")
	L_BIE_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_BIE_totalBIE = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Total Business Interruption Loss")
	L_BIE_totalBIE_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)	
	
	F_BIE_annBIEValue = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Daily Business Interruption Value")
	F_BIE_annBIEValue_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_BIE_fullProdDaysLost = models.PositiveIntegerField(verbose_name = "Full Equivalent Production Days Lost")
	F_BIE_fullProdDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_BIE_addProdDaysLost= models.PositiveIntegerField(verbose_name = "Additional Equivalent Production Days Lost")
	F_BIE_addProdDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_BIE_totalDaysLost= models.PositiveIntegerField(verbose_name = "Total Equivalent Production Days Lost")
	F_BIE_totalDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_BIE_directBILoss = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Direct Business Interruption Loss")
	F_BIE_directBILoss_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_BIE_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Other Business Interruption Losses")
	F_BIE_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)		
	F_BIE_totalBIE = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Total Business Interruption Loss")
	F_BIE_totalBIE_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)

	M_BIE_annBIEValue = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Daily Business Interruption Value")
	M_BIE_annBIEValue_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_BIE_fullProdDaysLost = models.PositiveIntegerField(verbose_name = "Full Equivalent Production Days Lost")
	M_BIE_fullProdDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_BIE_addProdDaysLost= models.PositiveIntegerField(verbose_name = "Additional Equivalent Production Days Lost")
	M_BIE_addProdDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_BIE_totalDaysLost= models.PositiveIntegerField(verbose_name = "Total Equivalent Production Days Lost")
	M_BIE_totalDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_BIE_directBILoss = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Direct Business Interruption Loss")
	M_BIE_directBILoss_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_BIE_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Other Business Interruption Losses")
	M_BIE_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)	
	M_BIE_totalBIE = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Total Business Interruption Loss")
	M_BIE_totalBIE_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)

	FM_BIE_annBIEValue = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Daily Business Interruption Value")
	FM_BIE_annBIEValue_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_BIE_fullProdDaysLost = models.PositiveIntegerField(verbose_name = "Full Equivalent Production Days Lost")
	FM_BIE_fullProdDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_BIE_addProdDaysLost= models.PositiveIntegerField(verbose_name = "Additional Equivalent Production Days Lost")
	FM_BIE_addProdDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_BIE_totalDaysLost= models.PositiveIntegerField(verbose_name = "Total Equivalent Production Days Lost")
	FM_BIE_totalDaysLost_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_BIE_directBILoss = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Direct Business Interruption Loss")
	FM_BIE_directBILoss_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_BIE_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Other Business Interruption Losses")
	FM_BIE_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)	
	FM_BIE_totalBIE = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name = "Total Business Interruption Loss")
	FM_BIE_totalBIE_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)

	###Other Losses###
	L_OL_smokePlume = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Third Party Smoke Plume Effects")
	L_OL_smokePlume_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_OL_MEOHDisposal = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Disposal of MEOH Contaminated Foam")
	L_OL_MEOHDisposal_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_OL_shareholderPartnerRel = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Shareholder and Partner Relations")
	L_OL_shareholderPartnerRel_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_OL_customerShippingGoodwill = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Customer Goodwill and Shipping")
	L_OL_customerShippingGoodwill_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_OL_mgmtTime = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Management Time and Expense")
	L_OL_mgmtTime_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_OL_emergPersonnelRisk = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Risk to ERP")
	L_OL_emergPersonnelRisk_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_OL_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Misc. Other Losses")
	L_OL_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_OL_total = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Total Other Losses")
	L_OL_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	
	F_OL_smokePlume = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Third Party Smoke Plume Effects")
	F_OL_smokePlume_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_OL_MEOHDisposal = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Disposal of MEOH Contaminated Foam")
	F_OL_MEOHDisposal_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_OL_shareholderPartnerRel = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Shareholder and Partner Relations")
	F_OL_shareholderPartnerRel_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_OL_customerShippingGoodwill = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Customer Goodwill and Shipping")
	F_OL_customerShippingGoodwill_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_OL_mgmtTime = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Management Time and Expense")
	F_OL_mgmtTime_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_OL_emergPersonnelRisk = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Risk to ERP")
	F_OL_emergPersonnelRisk_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_OL_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Misc. Other Losses")
	F_OL_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_OL_total = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Total Other Losses")
	F_OL_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	
	M_OL_smokePlume = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Third Party Smoke Plume Effects")
	M_OL_smokePlume_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_OL_MEOHDisposal = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Disposal of MEOH Contaminated Foam")
	M_OL_MEOHDisposal_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_OL_shareholderPartnerRel = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Shareholder and Partner Relations")
	M_OL_shareholderPartnerRel_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_OL_customerShippingGoodwill = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Customer Goodwill and Shipping")
	M_OL_customerShippingGoodwill_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_OL_mgmtTime = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Management Time and Expense")
	M_OL_mgmtTime_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_OL_emergPersonnelRisk = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Risk to ERP")
	M_OL_emergPersonnelRisk_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_OL_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Misc. Other Losses")
	M_OL_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_OL_total = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Total Other Losses")
	M_OL_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	
	FM_OL_smokePlume = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Third Party Smoke Plume Effects")
	FM_OL_smokePlume_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_OL_MEOHDisposal = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Disposal of MEOH Contaminated Foam")
	FM_OL_MEOHDisposal_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_OL_shareholderPartnerRel = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Shareholder and Partner Relations")
	FM_OL_shareholderPartnerRel_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_OL_customerShippingGoodwill = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Customer Goodwill and Shipping")
	FM_OL_customerShippingGoodwill_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_OL_mgmtTime = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Management Time and Expense")
	FM_OL_mgmtTime_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_OL_emergPersonnelRisk = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Risk to ERP")
	FM_OL_emergPersonnelRisk_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_OL_other = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Misc. Other Losses")
	FM_OL_other_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_OL_total = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Total Other Losses")
	FM_OL_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)

	###Cost of Protection###
	COP_lifeTime = models.PositiveIntegerField(verbose_name = "Equipment Life Expectency")
	COP_interestRate = models.DecimalField(max_digits=(DECIMALFIELD_MILLI+1), decimal_places=(DECIMALFIELD_MILLI+1), verbose_name="Annual Interest Rate")

	L_COP_totalCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Equipment Capital Cost")
	L_COP_totalCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_COP_areasServiced = models.PositiveIntegerField(verbose_name="Areas Serviced by Equipment")
	L_COP_areasServiced_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_COP_arealCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Equipment Capital Cost for this Area")
	L_COP_arealCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_COP_otherCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Other Capital Costs")
	L_COP_otherCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_COP_capExTotal = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Costs Subtotal")
	L_COP_capExTotal_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_COP_residual = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Equipment Residual Value")
	L_COP_residual_desc =models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_COP_residualPV = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Equipment Residual Present Value")
	L_COP_residualPV_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_COP_amortizedCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Annual Amortized Capital Costs")
	L_COP_amortizedCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_COP_opEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Operational Costs")
	L_COP_opEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_COP_otherOpEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Other Operational Costs")
	L_COP_otherOpEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	L_COP_annualCOP = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Annual Cost of Protection")
	L_COP_annualCOP_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)

	F_COP_totalCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Equipment Capital Cost")
	F_COP_totalCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_COP_areasServiced = models.PositiveIntegerField(verbose_name="Areas Serviced by Equipment")
	F_COP_areasServiced_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_COP_arealCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Equipment Capital Cost for this Area")
	F_COP_arealCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_COP_otherCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Other Capital Costs")
	F_COP_otherCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_COP_capExTotal = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Costs Subtotal")
	F_COP_capExTotal_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_COP_residual = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Equipment Residual Value")
	F_COP_residual_desc =models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_COP_residualPV = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Equipment Residual Present Value")
	F_COP_residualPV_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_COP_amortizedCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Annual Amortized Capital Costs")
	F_COP_amortizedCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_COP_opEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Operational Costs")
	F_COP_opEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_COP_otherOpEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Other Operational Costs")
	F_COP_otherOpEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	F_COP_annualCOP = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Annual Cost of Protection")
	F_COP_annualCOP_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)

	M_COP_totalCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Equipment Capital Cost")
	M_COP_totalCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_COP_areasServiced = models.PositiveIntegerField(verbose_name="Areas Serviced by Equipment")
	M_COP_areasServiced_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_COP_arealCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Equipment Capital Cost for this Area")
	M_COP_arealCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_COP_otherCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Other Capital Costs")
	M_COP_otherCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_COP_capExTotal = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Costs Subtotal")
	M_COP_capExTotal_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_COP_residual = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Equipment Residual Value")
	M_COP_residual_desc =models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_COP_residualPV = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Equipment Residual Present Value")
	M_COP_residualPV_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_COP_amortizedCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Annual Amortized Capital Costs")
	M_COP_amortizedCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_COP_opEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Operational Costs")
	M_COP_opEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_COP_otherOpEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Other Operational Costs")
	M_COP_otherOpEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	M_COP_annualCOP = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Annual Cost of Protection")
	M_COP_annualCOP_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)

	FM_COP_totalCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Equipment Capital Cost")
	FM_COP_totalCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_COP_areasServiced = models.PositiveIntegerField(verbose_name="Areas Serviced by Equipment")
	FM_COP_areasServiced_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_COP_arealCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Equipment Capital Cost for this Area")
	FM_COP_arealCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_COP_otherCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Other Capital Costs")
	FM_COP_otherCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_COP_capExTotal = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Costs Subtotal")
	FM_COP_capExTotal_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_COP_residual = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Equipment Residual Value")
	FM_COP_residual_desc =models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_COP_residualPV = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Capital Equipment Residual Present Value")
	FM_COP_residualPV_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_COP_amortizedCapEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Annual Amortized Capital Costs")
	FM_COP_amortizedCapEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_COP_opEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Operational Costs")
	FM_COP_opEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_COP_otherOpEx = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Other Operational Costs")
	FM_COP_otherOpEx_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)
	FM_COP_annualCOP = models.DecimalField(max_digits=(DECIMALFIELD_BILLION+DECIMALFIELD_CENTS), decimal_places=DECIMALFIELD_CENTS, verbose_name="Annual Cost of Protection")
	FM_COP_annualCOP_desc = models.TextField(max_length=CHARFIELD_MAXLENGTH, blank=True)

	summary_CaseDesc = models.TextField(max_length=CHARFIELD_MAXLENGTH*4, blank=False)
	summary_L = models.TextField(max_length=CHARFIELD_MAXLENGTH*4, blank=True)
	summary_F = models.TextField(max_length=CHARFIELD_MAXLENGTH*4, blank=True)
	summary_M = models.TextField(max_length=CHARFIELD_MAXLENGTH*4, blank=True)
	summary_FM = models.TextField(max_length=CHARFIELD_MAXLENGTH*4, blank=True)
	summary_Results = models.TextField(max_length=CHARFIELD_MAXLENGTH*4, blank=True)
	summary_Ass = models.TextField(max_length=CHARFIELD_MAXLENGTH*4, blank=True)
	summary_Conc = models.TextField(max_length=CHARFIELD_MAXLENGTH*4, blank=True)

