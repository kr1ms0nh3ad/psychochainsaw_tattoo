from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    name = models.CharField("Имя", max_length=100)
    specialty = models.CharField("Специализация", max_length=200, help_text="Например: традиция, реализм, киберсигилизм")
    experience = models.PositiveIntegerField("Опыт (лет)", default=1)
    phone = models.CharField("Телефон", max_length=20)
    photo = models.ImageField("Фото", upload_to='masters/', null=True, blank=True)
    is_active = models.BooleanField("Работает в салоне", default=True)

    def current_vacation(self):
        today = datetime.now()

        return self.vacations.filter(
            start_date__lte=today,
            end_date__gte=today
        ).first()
    
    def is_on_vacation(self):
        return self.current_vacation() is not None
    
    def vacation_until(self):
        vacation = self.current_vacation()
        return vacation.end_date if vacation else None

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
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    phone = models.CharField("Телефон", max_length=20, unique=True)
    email = models.EmailField("Email", blank=True, null=True)
    comment = models.TextField("Комментарий", blank=True, null=True)
    registered_at = models.DateTimeField("Дата регистрации", auto_now_add=True)
    parental_consent = models.FileField(
        "cогласие родителей",
        upload_to='consents/',
        null=True,
        blank=True,
        help_text="cкан или фото согласия (для клиентов до 18 лет)"
    )

    def age(self):
        """dозвращает возраст клиента"""
        if not self.birth_date:
            return None
        today = datetime.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    def needs_consent(self):
        """проверяет, нужно ли согласие"""
        age = self.age()
        return age is not None and age < 18

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
    photo = models.ImageField("Желаемый эскиз", upload_to='sketches/', null=False, blank=True)
    notes = models.TextField("Примечания", blank=True, null=True)

    def __str__(self):
        return f"{self.client.name} - {self.service.name} ({self.date_time})"

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

class MasterWork(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='portfolio', verbose_name="Мастер")
    title = models.CharField("Название работы", max_length=200)
    description = models.TextField("Описание", blank=True, null=True)
    image = models.ImageField("Фото работы", upload_to='portfolio/')
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    category = models.CharField("Категория", max_length=100, blank=True, null=True, 
                                help_text="Например: реализм, традиция, графика")
    body_part = models.CharField("Часть тела", max_length=100, blank=True, null=True,
                                help_text="Например: рука, нога, спина")
    
    def __str__(self):
        return f"{self.title} - {self.master.name}"
    
    class Meta:
        verbose_name = "Работа мастера"
        verbose_name_plural = "Портфолио мастеров"
        ordering = ['-created_at']

class Vacation(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='vacations', verbose_name="Мастер")
    start_date = models.DateField("Начало отпуска")
    end_date = models.DateField("Конец отпуска")
    reason = models.CharField("Причина", max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.master.name}: {self.start_date} - {self.end_date}"

    class Meta:
        verbose_name = "Отпуск"
        verbose_name_plural = "Отпуска"