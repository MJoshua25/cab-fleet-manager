from django import forms
from fleet_app.models import Outage


class OutageForm(forms.ModelForm):
	is_okay = forms.BooleanField(label='Est réglé?', initial=False, required=False)

	class Meta:
		model = Outage
		fields = ["tenant", "amount", "payment_method", "date_payment", "driver", "car", "reason", "location", "is_okay"]

	def clean(self):
		cleaned_data = super().clean()
		if 'is_okay' not in cleaned_data:
			cleaned_data['is_okay'] = False
