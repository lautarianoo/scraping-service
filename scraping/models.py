from django.db import models
import json
from django.core.serializers.json import DjangoJSONEncoder

def default_urls():
    return {"hh": "", "hh2": "", "hh3": "", "hh4": ""}

class JSONField1(models.TextField):
    """
    JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly.
    Django snippet #1478

    example:
        class Page(models.Model):
            data = JSONField(blank=True, null=True)


        page = Page.objects.get(pk=5)
        page.data = {'title': 'test', 'type': 3}
        page.save()
    """

    def to_python(self, value):
        if value == "":
            return None

        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def from_db_value(self, value, *args):
        return self.to_python(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)
        return value

class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)
    class Meta():
        verbose_name = 'City'
        verbose_name_plural = "City's"
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name
        super().save(*args, **kwargs)

class NameProf(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Специализация или профессия')
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta():
        verbose_name = 'Specialization/Profession'
        verbose_name_plural = 'Names Specializations'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name
        super().save(*args, **kwargs)

class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    prof = models.ForeignKey('NameProf', on_delete=models.CASCADE)
    earning = models.CharField(max_length=200, verbose_name='Зарплата')
    timestamp = models.DateField(auto_now_add=True)

    class Meta():
        verbose_name = 'Vacancy'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

class Errors(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = JSONField1(default={})

    def __str__(self):
        return str(self.timestamp)

class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    prof = models.ForeignKey('NameProf', on_delete=models.CASCADE)
    url_data = JSONField1(default=default_urls)
    class Meta():
        unique_together = ('city', 'prof')

