from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model= Task
        fields=['title','description','important']
        widgets ={
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Digite um Título'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Digite uma Descrição'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'important': 'Importante',}
