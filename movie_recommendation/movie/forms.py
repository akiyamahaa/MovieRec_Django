from django import forms
from movie.models import ReviewRating, RATE_CHOICES

class RateForm(forms.ModelForm):
	rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

	class Meta:
		model = ReviewRating
		fields = ('rate',)