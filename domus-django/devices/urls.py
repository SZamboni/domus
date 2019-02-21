from django.urls import path, re_path
from . import views
from .views import (UserCategoriesView, DevicesCategoryView, DeviceView, FunctionsView, 
        registerDevice,CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
        DeviceUpdateView,DeviceDeleteView,ChangeCategoryView)

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

    path('category/<int:catpk>/device/<int:devpk>/function/<int:funpk>', FunctionsView.as_view(), name="function"),
    path('registerdevice/', views.registerDevice,name='registerdevice'),
    path('poststatedata/',views.postStateData,name='poststatedata')
] 