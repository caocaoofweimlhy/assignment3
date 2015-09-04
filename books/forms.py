from .models import Book, Author, Genre
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Hidden, Button, HTML, Div, Field, Row, Fieldset

class BookForm(forms.ModelForm):
    class Meta: 
        model = Book
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "bookform"
        
        author = Div('author', css_class="col-xs-12", style="padding:0px;") 
        self.helper.layout.pop(4) 
        self.helper.layout.insert(4,Fieldset("Select author",author, Button("createauthormodal", value="Create New Author", css_class="btn btn-primary btn-sm col-xs-12 ", data_toggle="modal", data_target="#myModal")))
        
        genre = Div('genre',css_class = "col-xs-12", style="padding:0px;") 
        oldgenreselect = self.helper.layout.pop(5) 
        self.helper.layout.insert(5, Fieldset("Select Genre",genre, Button("creategenremodal", value="Create New Genre", css_class="btn btn-primary btn-sm col-xs-12", data_toggle="modal", data_target="#myModal2")))
        
        self.helper.layout.append(Button('btn_createbook', 'Create Book', css_class='createbook', style="margin-top:15px;"))
        self.helper.layout.append(Hidden(name='btn_createbook', value="btn_createbook"))
        
    def full_clean(self):
        super(BookForm, self).full_clean()
        if 'author' in self._errors:
            self.cleaned_data['genre'] = []
            print("remove genre errors")
            del self._errors['genre']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Save', 'Save', css_class='btn-primary'))

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "authorform"
        self.helper.layout.append(Hidden(name='btn_createauthor', value="btn_createauthor"))
        self.helper.layout.append(Button('btn_createauthor', 'Create Author', css_class='createauthor', data_dismiss="modal"))
        
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(GenreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "genreform"
        self.helper.layout.append(Hidden(name='btn_creategenre', value="btn_creategenre"))
        self.helper.layout.append(Button('btn_creategenre', 'Create Genre', css_class='creategenre', data_dismiss="modal"))
        
class BookFormUpdate(forms.ModelForm):
    class Meta: 
        model = Book
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(BookFormUpdate, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "bookformupdate"
        
        self.helper.add_input(Submit('submit', 'Update'))