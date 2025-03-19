from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        # Для проверки наличия одного и только одного основного раздела
        has_main = False
        for form in self.forms:
            # Пропускаем, если форма помечена на удаление
            if self.can_delete and self._should_delete_form(form):
                continue

            # Проверяем, заполнена ли форма
            if form.cleaned_data:
                # Если текущий тег отмечен как основной
                if form.cleaned_data.get('is_main'):
                    # Если уже был основной раздел - выдаем ошибку
                    if has_main:
                        raise ValidationError('Основным может быть только один раздел')
                    has_main = True

        # Если после обработки всех форм не нашли основной раздел - выдаем ошибку
        if not has_main and self.forms:
            raise ValidationError('Укажите основной раздел')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ['title', 'published_at']
    list_filter = ['published_at']
    search_fields = ['title', 'text']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']