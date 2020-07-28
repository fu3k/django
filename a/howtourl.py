###########################################################################################################
#webapp
------webapp/urls.py---------------------------------------------
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static,settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('techie.urls')),
    path('acc/',include('acc.urls')),
    
]
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

-------techie/urls.py---------------------------------------------
from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('add',views.add,name='add'),
    path('tech',views.techie,name='techie'),
    ]

-------acc/urls.py---------------------------------------------
from django.urls import path
from . import views

urlpatterns=[
    
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    ]

#######################################################################################################
# mysite
------- polls/urls.py -----------------------------------
from django.urls import path
from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

------- mysite/urls.py -----------------------------------
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),]

#######################################################################################################