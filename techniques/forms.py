from django import forms
from .models import Technique

class CustomTechniqueCreationForm(forms.ModelForm):
    class Meta:
        model = Technique
        fields = ['name', 'category', 'privacy_status', 'video_option', 'youtube_url', 'start_time', 'end_time']

    def clean(self):
        cleaned_data = super().clean()
        video_option = cleaned_data.get('video_option')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if video_option == 'cropped' and (start_time is None or end_time is None):
            raise forms.ValidationError("Start time and end time are required for cropped videos.")
        
        return cleaned_data