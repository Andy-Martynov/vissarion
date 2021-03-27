from django.db import models

from django.contrib.auth.models import User

import os
from mysite.settings import MEDIA_ROOT
from . import tools

LANG_CHOICES = [('RUS', 'Русский'), ('ENG', 'Английский'), ('FRA', 'Французский'),]
GENRE_CHOICES = [('1', 'Проза'), ('2', 'Поэзия'), ('3', 'Неизвестно'),]

WRITINGS_ROOT = 'writings'

def writing_dir_path(instance, filename):
    author = instance.author.name
    author = author.replace(' ', '_')
    title = filename.replace(' ', '_')
    path = os.path.join(MEDIA_ROOT, WRITINGS_ROOT, author, title)
    return path


class Author(models.Model) :
    name = models.CharField(max_length=200, blank=True, null=True)
    lang = models.CharField(max_length=3, choices=LANG_CHOICES, default='RUS')
    active = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        name = self.name
        name = name.replace('_', ' ')
        return f"{name}"

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lang': self.lang,
            'active': self.active,
            'hidden': self.hidden,
        }

    def label(self):
        return self.name

    def writings_dir(self):
        author = self.name
        author = author.replace(' ', '_')
        return os.path.join(MEDIA_ROOT, WRITINGS_ROOT, author)

    def text(self):
        strings = ' '
        writings = Writing.objects.filter(author=self, active=True)
        for writing in writings:
            strings += ' ' + writing.text()
        return strings

    def save_stats(self):
        fn = os.path.join(MEDIA_ROOT, 'stats', 'authors', f'a{self.id}.stats')
        text = self.text()
        stats = tools.stats(text)
        ok = tools.save_obj(fn, stats)
        return ok

    def stats(self):
        fn = os.path.join(MEDIA_ROOT, 'stats', 'authors', f'a{self.id}.stats')
        stats = tools.load_obj(fn)
        return stats


class Writing(models.Model) :
    title = models.CharField(max_length=200, blank=True, null=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, default='3')
    lang = models.CharField(max_length=3, choices=LANG_CHOICES, default='RUS')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="writings")
    file = models.FileField(upload_to=writing_dir_path, blank=True, null=True, )
    active = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    is_sample = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            'author': self.author.serialize(),
            'lang': self.lang,
            'genre': self.genre,
            'active': self.active,
            'hidden': self.hidden,
            'is_sample': self.is_sample,
        }

    def label(self):
        return f'{self.author}, {self.title}'

    def text(self):
        strings = []
        fn = str(self.file)
        if os.path.exists(fn):
            with open(fn) as f:
                strings.append(f.read())
        return ' '.join(strings)

    def save_stats(self):
        fn = os.path.join(MEDIA_ROOT, 'stats', 'writings', f'w{self.id}.stats')
        text = self.text()
        stats = tools.stats(text)
        ok = tools.save_obj(fn, stats)
        return ok

    def stats(self):
        fn = os.path.join(MEDIA_ROOT, 'stats', 'writings', f'w{self.id}.stats')
        stats = tools.load_obj(fn)
        return stats




class Sample(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="samples")
    writing = models.ForeignKey(Writing, on_delete=models.CASCADE, related_name="samples", blank=True, null=True)

    def __str__(self):
        return f"{self.writing.title}"

    def label(self):
        return self.writing.title

    def text(self):
        return self.writing.text()






