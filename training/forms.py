from django import forms

class get_newsreference(forms.Form):
	# id = forms.AutoField(primary_key=True)
	title = forms.CharField(label="Article Title", max_length=255)
	url = forms.URLField(label="Location of the article")
	