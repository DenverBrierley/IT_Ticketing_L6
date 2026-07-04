from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    #Add a comment to a ticket's thread.

    #Only the body is exposed here. Whether a comment is 'internal' is decided
    #in the view based on the author's role — never taken from the browser, so
    #an end user can't forge an internal note.
    

    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "placeholder": "Add a comment..."}),
        }

    def clean_body(self):
        body = self.cleaned_data["body"].strip()
        if not body:
            raise forms.ValidationError("Comment cannot be empty.")
        return body