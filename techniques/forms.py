from django import forms
from .models import Technique

class CustomTechniqueCreationForm(forms.ModelForm):
    class Meta:
        model = Technique
        fields = ['name', 'athlete', 'category', 'privacy_status', 'video_option', 'youtube_url', 'note', 'keywords', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TextInput(attrs={'placeholder': 'Example: 55 or 1:20'}),
            'end_time': forms.TextInput(attrs={'placeholder': 'Example: 150 or 2:30'}),
            'note': forms.Textarea(attrs={'rows': 8, 'cols': 30}),
            'keywords': forms.Textarea(attrs={'rows': 3, 'cols': 30}),
        }

    MAX_CROPPED_VIDEO_LENGTH = 1

    def clean(self):
        cleaned_data = super().clean()
        video_option = cleaned_data.get('video_option')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        keywords = cleaned_data.get('keywords')
        name = cleaned_data.get('name')
        category = cleaned_data.get('category')
        athlete = cleaned_data.get('athlete')
        generated_keywords = f'{name} {category} {athlete}'
        all_keywords = f'{keywords}\n{generated_keywords}' if keywords else generated_keywords

        cleaned_data['keywords'] = all_keywords

        if video_option == 'cropped' and (start_time is None or end_time is None):
            raise forms.ValidationError("Start time and end time are required for cropped videos.")
        

        if video_option == 'cropped':
            duration = end_time - start_time
            max_length_minutes = self.MAX_CROPPED_VIDEO_LENGTH
            if duration > max_length_minutes * 60:
                raise forms.ValidationError(f"Cropped videos must be no longer than {max_length_minutes} minutes.")
        
        return cleaned_data
    

class CustomTechniqueChangeForm(forms.ModelForm):
    class Meta:
        model = Technique
        fields = ['name', 'athlete', 'category', 'privacy_status', 'youtube_url', 'note', 'keywords']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 8, 'cols': 30}),
            'keywords': forms.Textarea(attrs={'rows': 3, 'cols': 30}),
        }

class CustomNoteChangeForm(forms.ModelForm):
    class Meta:
        model = Technique
        fields = ['note']