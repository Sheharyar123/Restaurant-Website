import os
from django.core.exceptions import ValidationError


def allow_only_images(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = [".png", ".jpg", ".jpeg"]
    if extension.lower() not in valid_extensions:
        raise ValidationError(
            f"Unsupported image extension. Valid extensions are: {str(valid_extensions)}"
        )
