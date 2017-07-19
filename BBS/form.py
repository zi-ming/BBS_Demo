from django.forms import ModelForm
from BBS import models

class ArticlePostForm(ModelForm):
    class Meta:
        model = models.Article
        exclude = ("author","priority")

    def __init__(self, *args, **kargs):
        super(ArticlePostForm, self).__init__(*args, **kargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class": "form-control"})

