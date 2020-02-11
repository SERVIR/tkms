def upcoming(request):
	"""
	Controller to show upcoming trainings
	"""
	
	context = {}
	return render(request, "training/upcoming.html", context)
	
