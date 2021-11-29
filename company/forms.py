from builtins import max

from django import forms

from .models import Company, CompanyDetail


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('company_name', 'company_website')
