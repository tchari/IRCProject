from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from .models import *

# Register your models here.

admin.site.register(Site)
admin.site.register(Unit)
admin.site.register(AssessmentType)
admin.site.register(CostOfProtection)
admin.site.register(CaseSetup)
admin.site.register(ProbabilityOfLoss)
admin.site.register(DamageAssessment)
admin.site.register(StandardAssessment)

class UserProfileInline(admin.TabularInline):
	model = Profile
	
class UserAdmin(DjangoUserAdmin):
	inlines = [UserProfileInline,]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)