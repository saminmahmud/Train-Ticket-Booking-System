from .models import Review, AddTrain, Schedule
from django import forms

class ReviewForm(forms.ModelForm):
    class Meta: 
        model = Review
        fields = ['name', 'body']


from station.models import Station
from django import forms
    
class AddTrainForm(forms.ModelForm):
    class Meta:
        model = AddTrain
        fields = ['image','train_name', 'start_station', 'end_station', 'price', 'total_number_of_seats', 'train_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].initial = 0 
        self.fields['total_number_of_seats'].initial = 0 

class Edit_scheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['train_date']
        

# class AddScheduleForm(forms.ModelForm):	
#     class Meta:
#         model = Schedule
#         fields = ['train', 'train_date', ]

#     labels = {
#             'train_date': 'Time' 
#     }
        
class AddScheduleForm(forms.ModelForm):	
    class Meta:
        model = Schedule
        fields = [ 'train_date' ]