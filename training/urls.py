from django.urls import path, include
from . import views

# Required for calling the REST API
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'training',views.TrainingViewSet)

# Define app name space
app_name = 'training'

urlpatterns = [
    # Content Items
    path("", views.about, name="about"),
    path("events", views.events, name="events"),
    path("event/<int:eventid>", views.event_detail, name="event_detail"),
    path("resources", views.resources, name="resources"),
    path("organizations", views.organizations, name="organizations"),
    path("trainers", views.trainers, name="trainers"),
    path("about", views.about, name="about"),
    path("charts", views.charts, name="charts"),
    # System Management Items
    path("upcoming", views.upcoming, name="upcoming"),
    path("addtraining", views.addtraining, name="addtraining"),
    path("get_newsreference", views.get_newsreference, name="get_newsreference"),
    path("register", views.register, name="register"),
    # API
    path('get_training_per_country', views.TrainingViewSet.as_view({'get': 'get_training_per_country'})),
    path('get_participant_gender_per_country', views.PartecipantViewSet.as_view({'get': 'get_participant_gender_per_country'})),
    # REST API patterns
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    # path('<int:pk>/calendar/', views.ResultsView.as_view(), name="calendar"),
    # path('<int:question_id>/addevent/', views.vote, name="addevent"),
]
