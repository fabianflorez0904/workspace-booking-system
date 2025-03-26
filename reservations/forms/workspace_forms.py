from django import forms
from reservations.models.workspace_models import Workspace


class WorkspaceForm(forms.ModelForm):

    class Meta:
        model = Workspace
        fields = [
            'name',
            'type',
            'capacity',
            'location',
            'availability',
        ]
