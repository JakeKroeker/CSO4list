from django import forms

#I don't really user these to do anything, should reformat this
class AddToDoItem(forms.Form):
    item_name = forms.CharField(help_text = "Item Name.", max_length = 64, required = True)
    item_description = forms.CharField(help_text = "Item Description.",  max_length = 500, required = False)
    due_date = forms.CharField(help_text = "Item Due Date.", required = False)
    complete = forms.BooleanField(help_text = "Item Is Complete", required = False)


class LoginCreate(forms.Form):
    username = forms.CharField(help_text = "Username.", max_length = 50, required = True)
    password = forms.CharField(help_text = "Password.", max_length = 50, required = True)