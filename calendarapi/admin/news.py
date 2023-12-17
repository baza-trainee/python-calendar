from wtforms.validators import DataRequired
from wtforms import TextAreaField, FileField

from calendarapi.admin.base_admin import AdminModelView
from calendarapi.admin.commons.formatters import ThumbnailFormatter, format_as_markup
from calendarapi.admin.commons.validators import ImageValidator
from calendarapi.commons.exeptions import DATA_REQUIRED
from calendarapi.commons.utils import custom_delete_file, custom_update_file


class NewsModelView(AdminModelView):
    can_set_page_size = True

    column_labels = {
        "name": "Новина",
        "description": "Опис",
        "created_at": "Дата",
        "photo_path": "Фото",
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
        "description",
        "created_at",
    ]

    column_formatters = {
        "description": format_as_markup,
        "photo_path": ThumbnailFormatter(),
    }

    form_extra_fields = {
        "photo_path": FileField(
            label="Виберіть фото для новини",
            validators=[ImageValidator()],
        ),
        "description": TextAreaField(
            label="Опис",
            render_kw={"class": "form-control", "rows": 5},
            validators=[DataRequired(message=DATA_REQUIRED)],
        ),
    }

    form_args = {
        "created_at": {
            "validators": [DataRequired(message=DATA_REQUIRED)],
        },
    }

    def on_model_delete(self, model):
        custom_delete_file(model, field_name="photo_path")
        return super().on_model_delete(model)

    def on_model_change(self, form, model, is_created):
        custom_update_file(model, form, field_name="photo_path")
        return super().on_model_change(form, model, is_created)
