from django import forms


class CreateCardForm(forms.Form):
	model = forms.CharField(label='Modèle', required=True, max_length=255)
	brand = forms.CharField(label='Marque', required=True, max_length=255)
	matriculation = forms.CharField(label='Immatriculation', required=True, max_length=255)
	color = forms.CharField(label='Couleur', required=True, max_length=255)
	on_service = forms.BooleanField(label='En service', required=True)
