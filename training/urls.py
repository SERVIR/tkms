from django.urls import path
from training import views

# Define app name space
app_name = 'training'

urlpatterns = [
	# Content Items
	path("", views.about, name="about"),
	path("events", views.events, name="events"),
	path("resources", views.resources, name="resources"),
	path("organizations", views.organizations, name="organizations"),
	path("trainers", views.trainers, name="trainers"),
	path("about", views.about, name="about"),
	# System Management Items
	path("upcoming", views.upcoming, name="upcoming"),
	path("addtraining", views.addtraining, name="addtraining"),
	path("get_newsreference", views.get_newsreference, name="get_newsreference"),
	path("register", views.register, name="register"),
	# path('<int:pk>/', views.DetailView.as_view(), name="detail"),
	# path('<int:pk>/calendar/', views.ResultsView.as_view(), name="calendar"),
	# path('<int:question_id>/addevent/', views.vote, name="addevent"),
]

