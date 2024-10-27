# from django import forms
# from .models import User


# class UserChangeForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("email", "is_active", "is_staff","first_name","last_name")

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         # Only hash if the password has been changed
#         if "password" in self.changed_data:
#             user.set_password(self.cleaned_data["password"])  # Hash the new password
#         if commit:
#             user.save()
#         return user
