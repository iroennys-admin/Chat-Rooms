from django.forms import ModelForm
from .models import Room, Topic


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

    def clean(self):
        cleaned_data = super().clean()
        topic_name = self.data.get('topic_input', '').strip()
        if topic_name:
            topic, _ = Topic.objects.get_or_create(name=topic_name)
            cleaned_data['topic'] = topic
        return cleaned_data
