from django.db import models
from datetime import date


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название жанра")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    author = models.CharField(max_length=255, verbose_name="Автор")
    isbn = models.CharField(
        max_length=13, unique=True, blank=True, null=True, verbose_name="ISBN"
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Жанр"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    publisher = models.CharField(
        max_length=255, blank=True, verbose_name="Издательство"
    )
    year = models.IntegerField(null=True, blank=True, verbose_name="Год издания")

    def __str__(self):
        return f"{self.author} – {self.title}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Invoice(models.Model):
    supplier = models.CharField(max_length=255, verbose_name="Поставщик")
    date = models.DateField(default=date.today, verbose_name="Дата")
    number = models.CharField(
        max_length=50, unique=True, verbose_name="Номер накладной"
    )

    def __str__(self):
        return f"Накладная №{self.number} от {self.date}"

    class Meta:
        verbose_name = "Накладная"
        verbose_name_plural = "Накладные"


class BookCopy(models.Model):
    STATUS_CHOICES = [
        ("available", "Доступна"),
        ("issued", "Выдана"),
        ("written_off", "Списана"),
    ]

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="copies", verbose_name="Книга"
    )
    inventory_number = models.CharField(
        max_length=20, unique=True, blank=True, verbose_name="Инвентарный номер"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available",
        verbose_name="Статус",
    )
    added_date = models.DateField(auto_now_add=True, verbose_name="Дата добавления")
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="copies",
        verbose_name="Накладная",
    )

    def save(self, *args, **kwargs):
        if not self.inventory_number:
            year = str(date.today().year)

            last_copy = (
                BookCopy.objects.filter(inventory_number__startswith=f"{year}-")
                .order_by("-inventory_number")
                .first()
            )
            if last_copy:
                # Берём число после дефиса и увеличиваем
                last_number = int(last_copy.inventory_number.split("-")[1])
                new_number = last_number + 1
            else:
                new_number = 1
            self.inventory_number = (
                f"{year}-{new_number:04d}"  # 2026-0001, 2026-0002...
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory_number} – {self.book.title}"

    class Meta:
        verbose_name = "Экземпляр книги"
        verbose_name_plural = "Экземпляры книг"
