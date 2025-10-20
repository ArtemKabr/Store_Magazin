"""Пользовательские template-фильтры для работы с формами."""

from django import template

register = template.Library()


@register.filter
def add_class(field, css: str):
    """
    Добавляет CSS-класс к виджету поля формы.
    Пример: {{ form.email|add_class:"form-control" }}
    """
    return field.as_widget(attrs={"class": css})
