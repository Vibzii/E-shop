from django import forms
from .models import ReviewRating, Variation


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']

class RestrictedForm(forms.ModelForm):
   def __init__(self, *args, **kwargs):
      super(RestrictedForm, self).__init__(*args, **kwargs)
      if self.instance.pk:
        self.fields['variation'].queryset = Variation.objects.filter(parent=self.instance)
