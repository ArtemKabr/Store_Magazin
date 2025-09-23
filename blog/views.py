# blog/views.py
"""CBV для блога: список, деталь, создание, редактирование, удаление."""
from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post


class PostListView(ListView):
    """
    Список статей.
    Публично показываем только опубликованные,
    staff-пользователям — все (в т.ч. черновики).
    """
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Фильтрация по is_published для не-staff пользователей."""
        qs = Post.objects.all().order_by("-created_at")
        if not self.request.user.is_staff:
            qs = qs.filter(is_published=True)
        return qs


class PostDetailView(DetailView):
    """
    Детальная страница статьи.
    - Не даём просматривать черновики гостям/не-staff.
    - Атомарно увеличиваем счётчик просмотров.
    - (Опционально) отправляем письмо при достижении 100 просмотров.
    """
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        """Ограничиваем доступ к черновикам для не-staff."""
        qs = Post.objects.all()
        if not self.request.user.is_staff:
            qs = qs.filter(is_published=True)
        return qs

    def get_object(self, queryset=None):
        """Инкрементируем views и (опционально) шлём письмо на 100 просмотров."""
        obj = super().get_object(queryset)
        # атомарный инкремент
        Post.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        obj.refresh_from_db(fields=["views"])

        # Доп. задание: письмо при 100 просмотрах
        if obj.views == 20:
            from django.core.mail import send_mail
            send_mail(
                subject="Поздравляем! 20 просмотров",
                message=f'Статья "{obj.title}" набрала 20 просмотров.',
                from_email=None,  # возьмётся из DEFAULT_FROM_EMAIL
                recipient_list=["artemkabr7@gmail.com"],
                fail_silently=True,
            )
        return obj


class PostCreateView(CreateView):
    """
    Создание статьи. После сохранения — редирект на детальную
    (работает через get_absolute_url модели).
    """
    model = Post
    fields = ("title", "content", "preview", "is_published")
    template_name = "blog/post_form.html"


class PostUpdateView(UpdateView):
    """
    Редактирование статьи. После сохранения — редиректим на детальную.
    """
    model = Post
    fields = ("title", "content", "preview", "is_published")
    template_name = "blog/post_form.html"

    def get_success_url(self) -> str:
        """Перенаправляем на просмотр отредактированной статьи."""
        return self.object.get_absolute_url()


class PostDeleteView(DeleteView):
    """
    Удаление статьи. После удаления — в список статей.
    """
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
