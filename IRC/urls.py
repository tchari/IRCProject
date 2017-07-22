#IRC APP URL Configuration

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
]

protectionItems = [
	url(r'^ProtectionItems/$', views.ProtectionItemsListView.as_view(), name='protectionItemsListView'),
	url(r'^ProtectionItems/(?P<pk>\d+)$', views.ProtectionItemsDetailView.as_view(), name='protectionItemsDetailView'),
	url(r'^ProtectionItems/(?P<pk>\d+)/edit/$', views.ProtectionItem_edit, name='protectionItem_edit'),
	url(r'^ProtectionItems/new/', views.ProtectionItem_new, name='protectionItem_new'),
]

assessments = [
	url(r'^Assessments/$', views.AssessmentsListView.as_view(), name='assessmentsListView'),
	url(r'^Assessments/(?P<pk>\d+)$', views.AssessmentsDetailView.as_view(), name='assessmentsDetailView'),
#	url(r'^Assessments/(?P<pk>\d+)/edit/$', views.Assessments_edit, name='assessment_edit'),
	url(r'Assessments/new/', views.Assessments_new, name='assessment_new'),
	url(r'Assessments/cancel/', views.Assessments_cancel, name='assessment_cancel'),
]

units = [
	url(r'^Units/$', views.UnitsListView.as_view(), name='unitsListView'),
	url(r'^Units/(?P<pk>\d+)$', views.UnitsDetailView.as_view(), name='unitsDetailView'),
	url(r'^Units/(?P<pk>\d+)/edit/$', views.Units_edit, name='unit_edit'),
	url(r'Units/new/', views.Units_new, name='unit_new'),
]

SA = [
	url(r'^formonday/$', views.StandardAssessmentsListView.as_view(), name='SAListView'),
	url(r'^formonday/(?P<pk>\d+)$', views.StandardAssessmentsDetailView.as_view(), name='SADetailView'),
	url(r'^formonday/(?P<pk>\d+)/edit/$', views.StandardAssessments_edit, name='SA_edit'),
	url(r'formonday/new/', views.StandardAssessments_new, name='SA_new'),
]

exportPDF = [
	url(r'^exportPDF/$', views.exportPDF, name='exportPDF')
]
urlpatterns += protectionItems
urlpatterns += assessments
urlpatterns += units
urlpatterns += SA
urlpatterns += exportPDF