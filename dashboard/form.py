from django import forms
from authentication.models import TodoTask

class TodoTaskForm(forms.ModelForm):
    class Meta:
        model = TodoTask
        fields = ['deadline', 'description']

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(TodoTaskForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.request_user:
            self.instance.user = self.request_user
        return super(TodoTaskForm, self).save(commit=commit)
