"""mainpage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from webpage import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.pages_login), 
    path('socialintelligence', views.socialintelligence),
    path('VCs', views.VCs),
    path('gems', views.gems),
    path('macro', views.macro), 
    path('forecasting', views.forecasting_value),
    path('pages_login', views.pages_login),
    path('pages_register', views.pages_register),
    path('pages-error-404', views.pages_error),
    path('pages_contact', views.pages_contact),
    path('portfolio_optimisation', views.portfolio_optimisation),
    path('fundamentals', views.fundamentals),
    path('correlation', views.correlation),
    path('logout', views.logout),
    re_path(r'^.*$', views.error_view)

]


