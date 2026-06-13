from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название темы")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name


class Task(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "База"),
        ("hard", "Профиль"),
    ]

    title = models.CharField(max_length=200, verbose_name="Название")
    number = models.PositiveIntegerField(verbose_name="Номер задания")
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Тема"
    )
    condition = models.TextField(verbose_name="Условие")
    answer = models.CharField(max_length=100, verbose_name="Ответ")
    explanation = models.TextField(blank=True, verbose_name="Пояснение")
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="easy",
        verbose_name="Сложность"
    )
    condition_image = models.ImageField(
        upload_to="tasks/conditions/",
        blank=True,
        null=True,
        verbose_name="Изображение к условию"
    )

    explanation_image = models.ImageField(
        upload_to="tasks/explanations/",
        blank=True,
        null=True,
        verbose_name="Изображение к пояснению"
    )

    def __str__(self):
        return f"№{self.number}. {self.title}"