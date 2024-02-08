from django import forms
from .models import Technique

class CustomTechniqueCreationForm(forms.ModelForm):
    class Meta:
        model = Technique
        fields = ['name', 'category', 'privacy_status', 'video_option', 'youtube_url', 'note', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TextInput(attrs={'placeholder': 'Example: 55 or 1:20'}),
            'end_time': forms.TextInput(attrs={'placeholder': 'Example: 150 or 2:30'}),
            'note': forms.Textarea(attrs={'rows': 8, 'cols': 30}),
        }

    MAX_CROPPED_VIDEO_LENGTH = 2

    def clean(self):
        cleaned_data = super().clean()
        video_option = cleaned_data.get('video_option')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if video_option == 'cropped' and (start_time is None or end_time is None):
            raise forms.ValidationError("Start time and end time are required for cropped videos.")
        
        if start_time and ':' in start_time:
            start_minutes, start_seconds = map(int, start_time.split(':'))
            start_time = start_minutes * 60 + start_seconds

        if end_time and ':' in end_time:
            end_minutes, end_seconds = map(int, end_time.split(':'))
            end_time = end_minutes * 60 + end_seconds

        if video_option == 'cropped':
            duration = end_time - start_time
            max_length_minutes = self.MAX_CROPPED_VIDEO_LENGTH
            if duration > max_length_minutes * 60:
                raise forms.ValidationError(f"Cropped videos must be no longer than {max_length_minutes} minutes.")
        
        return cleaned_data