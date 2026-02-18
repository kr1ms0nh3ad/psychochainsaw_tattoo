from django.db import models
from django.contrib.auth.models import User

class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    name = models.CharField("Имя", max_length=100)
    specialty = models.CharField("Специализация", max_length=200, help_text="Например: традиция, реализм, киберсигилизм")
    experience = models.PositiveIntegerField("Опыт (лет)", default=1)
    phone = models.CharField("Телефон", max_length=20)
    photo = models.ImageField("Фото", upload_to='masters/', null=True, blank=True)
    is_active = models.BooleanField("Работает", default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

class Service(models.Model):
    name = models.CharField("Название услуги", max_length=150)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена (₽)", max_digits=10, decimal_places=2)
    duration = models.DurationField("Длительность", help_text="Формат ЧЧ:ММ:СС") 
    masters = models.ManyToManyField(Master, related_name='services', verbose_name="Кто выполняет")

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class Client(models.Model):
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=20, unique=True)
    email = models.EmailField("Email", blank=True, null=True)
    comment = models.TextField("Комментарий", blank=True, null=True)
    registered_at = models.DateTimeField("Дата регистрации", auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтвержден'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]

    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='appointments', verbose_name="Клиент")
    master = models.ForeignKey(Master, on_delete=models.PROTECT, related_name='appointments', verbose_name="Мастер")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='appointments', verbose_name="Услуга")
    date_time = models.DateTimeField("Дата и время")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField("Дата создания записи", auto_now_add=True)
    notes = models.TextField("Примечания", blank=True, null=True)

    def __str__(self):
        return f"{self.client.name} - {self.service.name} ({self.date_time})"

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"