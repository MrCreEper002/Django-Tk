from .models import Comment, Post
from django.forms import ModelForm, TextInput


class CommentAdd(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']

        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control w',
                    'placeholder': "Имя",
                    'aria-describedby': "basic-addon2"}
            ),
            'body': TextInput(
                attrs={
                    'class': 'w-50 form-control w',
                    'placeholder': "Сообщение",
                    'aria-describedby': "basic-addon2"}
            ),
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', "Anons", "image"]

        widgets = {
            'title': TextInput(attrs={'class': 'form-control w-50', 'placeholder': "Название"}),
            'Anons': TextInput(attrs={'class': 'form-control w-50', 'placeholder': "Текс", 'for': 'customFile'}),
        }
