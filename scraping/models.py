from django.db import models

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
    timestamp = models.DateField(auto_now_add=True)

    class Meta():
        verbose_name = 'Vacancy'

    def __str__(self):
        return self.title