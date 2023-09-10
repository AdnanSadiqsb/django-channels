from django.core.exceptions import ValidationError
from PIL import Image


def validate_image_icon_size(image):
    print("image", image)
    if image:
        if image.size > 1048576:
            raise ValidationError("Image size in MB is too large")
        with Image.open(image) as img:
            if img.height > 70 or img.width > 70:
                raise ValidationError("The maximum allowed dimension is 70x70")
    else:
        True
