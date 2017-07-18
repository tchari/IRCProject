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



