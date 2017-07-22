from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

class CoPForm(forms.ModelForm):
	class Meta:
		model = CostOfProtection
		fields = '__all__'
		labels = {
			"name":"Protection Item Name",
			"years":"Life Expectancy of the Item",
			"annualInterestRate":"Annual Interest Rate",
			"capEx":"Capital Cost of the Item",
			"areasServiced":"Total Number of Areas Serviced",
			"otherCapEx":"Other Capital Costs",
			"opEx":"Annual Operational Costs",
			"otherOpEx":"Other Annual Operational Costs",
		}		
		

class UnitForm(forms.ModelForm):
	class Meta:
		model = Unit
		fields = '__all__'
		labels = {
			"name": "Unit Name",
			"value":"Value at Risk",
			"freq":"Frequency of Event Happening",
			"link":"Link to Equipment/Equipment Type",
			"basis":"Basis",
		}

class CaseSetupForm(forms.ModelForm):
	class Meta:
		model = CaseSetup
		fields = '__all__'
		labels = {
			"site": "Site",
			"desc": "Description",
			"numDmgAss": "Number of Assessments",
			"unit": "Unit",
			
		}
		widgets = {
			'site': forms.HiddenInput()
		}
		
class ProbabilityOfLossForm(forms.ModelForm):
	class Meta:
		model = ProbabilityOfLoss
		fields = '__all__'
		widgets = {
			'case': forms.HiddenInput()
		}
		labels = {
			"value": "Value at Risk",
			"protection": "Type of Protection",
			"freq": "Frequency of Event Happening",
			"siteHistoryAndAge": "Site History and Age",
			"serviceAndEnvironment": "Service and Environment",
			"levelOfPMAndOperatorXP": "Level of PM and Operator Experience",
			"accessToERAndFirstResponse": "Access to ER and First Response",
		}

class DamageAssessmentForm(forms.ModelForm):
	
	name = forms.CharField(widget = forms.HiddenInput(), required=False)
	
	class Meta:
		model = DamageAssessment
		fields = '__all__'
		widgets = {
			'case': forms.HiddenInput(),
			'name': forms.HiddenInput()
		}
		labels = {
			"damageToValueRiskRatio": "Ratio of Total Damage to Value at Risk",
			"additionalEscalationDamages": "Estimate Additional Escalation Equipment Damages",
			"adjustmentForSecondaryLosses": "Adjustment Factor due to Secondary Losses, Fire Fighting, \n\r Overflow, Salvage, Debris Removal, Clean-up, Installation",
			"annualPlantBIEValue": "Plant Annual Business Interruption Value",
			"fullProductionDaysLost": "Full Production Days Lost",
			"additionalDaysLost": "Additional Day Lost due to Misc.",
			"indirectOrPartialLoss": "Indirect or Partial Loss",
			"otherBIELosses": "Enter Additional BIE Losses (if any)",
			"thirdPartyPlume": "Third Party Smoke Plume Effects",
			"disposalOfMEOH": "Disposal of MEOH Contaminated Foam",
			"shareholderPartnerRelationship": "Shareholder/Partner Relations",
			"customerGoodwill": "Customer/Shipping Goodwill",
			"managementTime": "Management Time and Expense",
			"riskToEmergPersonnel": "Risk to Emergency Response Personnel",
			"otherOLLosses": "Enter Other Additional Losses (if any)"			
		}

class StandardAssessmentForm(forms.ModelForm):

	class Meta:
		model = StandardAssessment
		fields = '__all__'
