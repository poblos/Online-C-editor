from django import forms
from .models import CompilationSettings, Optimization, DependantOption


class DirectoryForm(forms.Form):
    name = forms.CharField(label="Directory name", max_length=200)
    desc = forms.CharField(label="Directory description", max_length=200, required=False)


class FileForm(forms.Form):
    name = forms.CharField(label="File name", max_length=200)
    desc = forms.CharField(label="File description", max_length=200, required=False)
    text = forms.CharField(label="File text", max_length=10000, widget=forms.Textarea(
        attrs={'name': 'text', 'rows': 10, 'cols': 40}), required=False)


class EditorForm(forms.Form):
    text = forms.CharField(max_length=10000, widget=forms.Textarea(
        attrs={'name': 'text', 'rows': 20, 'cols': 60}), required=False, label='')


class OptimizationsForm(forms.Form):
    options = forms.MultipleChoiceField(
        choices=[(o.name, str(o)) for o in Optimization.objects.all()], label='', required=False)


class DependantForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DependantForm, self).__init__(*args, **kwargs)
        if CompilationSettings.objects.all().count() > 0:
            self.fields['options'] = forms.MultipleChoiceField(choices=[(o.name, str(o)) for o in DependantOption.objects.filter(
            processor=CompilationSettings.objects.order_by("id")[0].processor)], label='', required=False)
        else:
            self.fields['options'] = forms.MultipleChoiceField(choices=[(o.name, str(o)) for o in DependantOption.objects.all()], label='', required=False)
    
    if CompilationSettings.objects.all().count() > 0:
        options = forms.MultipleChoiceField(choices=[(o.name, str(o)) for o in DependantOption.objects.filter(
            processor=CompilationSettings.objects.order_by("id")[0].processor)], label='', required=False)
    else:
         options = forms.MultipleChoiceField(choices=[(o.name, str(o)) for o in DependantOption.objects.all()], label='', required=False)
