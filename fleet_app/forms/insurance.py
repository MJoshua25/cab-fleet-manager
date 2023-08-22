from django import forms


class CreateInsuranceForm(forms.Form):
    car = forms.CharField(label="voitureAssurance", required=True, max_length=255)
    insurance_company = forms.CharField(label='Compagnie_assurance', required=True, max_length=255)
    due_date = forms.DateField(label='Date échéance', required=True)
    monthly_amount = forms.CharField(label='Paiement_mensuel', required=True, max_length=255)
    last_payment = forms.IntegerField(label='Dernier paiement', required=True)
    next_date = forms.DateField(label='Date de prochain paiement', required=True)
