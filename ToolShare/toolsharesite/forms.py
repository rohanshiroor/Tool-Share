from django.forms import ModelForm
from django import forms
from toolsharesite.models import ToolShareUser , CommunityShed, Tool,\
    Transaction, Feedback
from django.forms import Textarea

class RegistrationForm(ModelForm):
    confirmpass = forms.CharField(max_length=25)
    
    class Meta:
        model = ToolShareUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'address_line1', 'address_line2', 'city','state', 'zip','phone_no']
        
        
class CommunityShedForm(ModelForm):
    class Meta:
        model = CommunityShed
        fields = ['address_line1','address_line2','city','state','zip']

class CreateShedForm(ModelForm):
    zip = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = CommunityShed
        fields = ['address_line1','address_line2','city','state','zip']
        
        
class ToolRegistrationForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        no_shed = kwargs.pop('no_shed', False)
        super(ToolRegistrationForm, self).__init__(*args, **kwargs)
        if no_shed:
            self.fields['location'].choices = [('H','Home')]
        else:
            self.fields['location'].choices = (('H','Home'),('S','Community Shed')) 
    
    class Meta:
        model = Tool
        widgets = {
            'description': Textarea(),
            'special_instruction': Textarea(),
        }
    
        fields = ['name','category','description','condition','location','image','special_instruction','pick_up_preference']
        
            
class ToolBorrowForm(ModelForm):
    
    class Meta:
        model = Transaction
        fields = ['tool_lend_date','tool_return_date','borrow_message']
        widgets = {
            'borrow_message': Textarea(),
        }
        labels = {
            'tool_lend_date': ('Start Date'),
            'tool_return_date': ('End Date'),
            'borrow_message': ('Message')
        }


class UpdateProfileForm(ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    zip = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required'}))
    email = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required'}))
    address_line1 = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required'}))
    city = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required'}))
    state = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required'}))
    phone_no = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required'}))

    class Meta:
        model = ToolShareUser
        fields = ['username', 'first_name', 'last_name', 'email', 'address_line1', 'address_line2', 'city','state','zip','phone_no']
        

class ToolDetailsForm(ModelForm):
    
#     name = forms.CharField(
#         widget=forms.TextInput(attrs={'readonly':'readonly'})
#     )
#     category = forms.CharField(
#         widget=forms.TextInput(attrs={'readonly':'readonly'})
#     )
#     description = forms.CharField(
#         widget=forms.TextInput(attrs={'readonly':'readonly'})
#     )
#     condition = forms.CharField(
#         widget=forms.TextInput(attrs={'readonly':'readonly'})
#     )
#     location = forms.CharField(
#         widget=forms.TextInput(attrs={'readonly':'readonly'})
#     )
#     special_instruction = forms.CharField(
#         widget=forms.TextInput(attrs={'readonly':'readonly'})
#     )
#     pick_up_preference = forms.CharField(
#         widget=forms.TextInput(attrs={'readonly':'readonly'})
#     )
    
    class Meta:
        model = Tool
        fields = ['image','name','owner','category','description','condition','location','special_instruction','pick_up_preference']
        
        
class EditToolDetailsForm(ModelForm):
    class Meta:
        model = Tool
        fields = ['image','name','category','description','condition','location','special_instruction','pick_up_preference']
        
class FeedbackForm(ModelForm):

   class Meta:
       model = Feedback
       fields = ['comment']
       
        
