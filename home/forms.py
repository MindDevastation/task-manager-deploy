from django import forms
from .models import Worker


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["first_name", "last_name", "email", "position"]
