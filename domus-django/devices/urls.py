from django.urls import path, re_path
from . import views
from .views import *

urlpatterns = [
    path('about/', views.about, name="about-page"),
    path('',views.landingPage, name="landingpage"),
    path('userDevices/', UserCategoriesView.as_view(), name="home"),

    path('category/<int:pk>/',DevicesCategoryView.as_view(),name="category"),
    path('category/new/',CategoryCreateView.as_view(),name='newcategory'),
    path('category/<int:pk>/update/',CategoryUpdateView.as_view(),name='updatecategory'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='deletecategory'),

    path('category/<int:catpk>/device/<int:pk>', DeviceView.as_view(), name = "device"),
    path('category/<int:catpk>/device/<int:pk>/update/',DeviceUpdateView.as_view(),name='updatedevice'),
    path('category/<int:catpk>/device/<int:pk>/delete/',DeviceDeleteView.as_view(),name='deletedevice'),
    path('category/<int:catpk>/device/<int:pk>/changecategory/<int:oldcatpk>/',ChangeCategoryView.as_view(),name='changecategory'),

    path('category/<int:catpk>/device/<int:devpk>/attribute/<int:pk>/newalert/',AlertCreateView.as_view(),name='newalert'),
    path('category/<int:catpk>/device/<int:devpk>/alerts/',AlertListView.as_view(),name='alerts'),
    path('category/<int:catpk>/device/<int:devpk>/alerts/<int:pk>/delete/',AlertDeleteView.as_view(),name='deletealert'),
    path('category/<int:catpk>/device/<int:devpk>/alerts/<int:pk>/update/',AlertUpdateView.as_view(),name='updatealert'),

    path('category/<int:catpk>/device/<int:devpk>/alert/<int:alpk>/selectfeedbackfunction/',FeedbackFunctionChoiceView.as_view(),name='selectfeedbackfunction'),
    path('category/<int:catpk>/device/<int:devpk>/alert/<int:alpk>/createfeedbackfunction/<int:pk>/',CreateFeedbackFunctionView.as_view(), name='newfeedbackfunction'),

    path('notifications/',NotificationsListView.as_view(),name='notifications'),
    path('old-notifications/',OldNotificationsListView.as_view(),name='old-notifications'),

    path('category/<int:catpk>/device/<int:devpk>/function/<int:funpk>', FunctionsView.as_view(), name="function"),
    path('registerdevice/', views.registerDevice,name='registerdevice'),
    path('poststatedata/',views.postStateData,name='poststatedata')
] 