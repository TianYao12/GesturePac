from django.contrib import admin
from django.urls import path
from vision import views

# The `urlpatterns` list routes URLs to views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("users_pac/", views.data_pac),
    path("users_flap/", views.data_flap),
    path("users/pac/<str:name>", views.data_change_pac),
    path("users/flap/<str:name>", views.data_change_flap)
]

"""
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