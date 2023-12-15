import os

from wtforms.validators import DataRequired
from flask import current_app, request
from markupsafe import Markup
from wtforms import TextAreaField, ValidationError
from wtforms import FileField

from calendarapi.admin.common import (
    AdminModelView,
    get_media_path,
    custom_delete_file,
    custom_save_file,
)

ABS_MEDIA_PATH = get_media_path(__name__.split(".")[-1])


class ReviewsAdminModelView(AdminModelView):
    can_set_page_size = True

    column_labels = {
        "name": "Ім'я Прізвище",
        "position": "Посада",
        "description": "Опис",
        "photo_path": "Фото",
        "created_at": "Дата",
    }
    column_sortable_list = [
        "created_at",
    ]
    column_searchable_list = [
        "name",
    ]
    column_default_sort = [
        ("id", False),
    ]
    column_descriptions = {
        "description": """Ви можете використовувати HTML-теги, щоб зробити абзац, створити список і т. д., для покращення зручності читання."""
    }
    column_list = [
        "photo_path",
        "name",
        "position",
        "description",
        "created_at",
    ]

    def _format_description(view, context, model, name):
        return Markup(model.description)

    def _list_thumbnail(width: int = 240):
        def thumbnail_formatter(view, context, model, name):
            if not model.photo_path:
                return ""
            if current_app.config["STORAGE"] == "STATIC":
                url = os.path.join(request.host_url, model.photo_path)
            else:
                url = model.photo_path

            if model.photo_path.split(".")[-1] in current_app.config["IMAGE_FORMATS"]:
                return Markup(f"<img src={url} width={width}>")

        return thumbnail_formatter

    column_formatters = {
        "photo_path": _list_thumbnail(width=80),
        "description": _format_description,
    }

    def _custom_validate_media(form, field):
        if not form.photo_path.object_data and not form.photo_path.data:
            raise ValidationError("Це поле обов'язкове.")

    form_extra_fields = {
        "photo_path": FileField(
            "Виберіть фото для відгуку",
            validators=[_custom_validate_media],
        ),
        "description": TextAreaField(
            "Опис",
            render_kw={"class": "form-control", "rows": 5},
            validators=[DataRequired(message="Це поле обов'язкове.")],
        ),
    }

    form_args = {
        "created_at": {"validators": [DataRequired(message="Це поле обов'язкове.")]},
    }

    def on_model_delete(self, model):
        custom_delete_file(ABS_MEDIA_PATH, model.photo_path)
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        if model.photo_path:
            if form.photo_path.object_data:
                custom_delete_file(ABS_MEDIA_PATH, form.photo_path.object_data)
            model.photo_path = custom_save_file(ABS_MEDIA_PATH, model.photo_path)
        else:
            model.photo_path = form.photo_path.object_data
        return super().on_model_change(form, model, is_created)
