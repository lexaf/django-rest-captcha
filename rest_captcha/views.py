import uuid
import base64

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from rest_framework import views, response
from django.core.cache import caches
from .settings import api_settings
from django.conf import settings
from . import utils
from . import captcha

cache = caches[api_settings.CAPTCHA_CACHE]


class RestCaptchaView(views.APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        key = str(uuid.uuid4())
        value = utils.random_char_challenge(api_settings.CAPTCHA_LENGTH)
        cache_key = utils.get_cache_key(key)
        cache.set(cache_key, value, api_settings.CAPTCHA_TIMEOUT)

        # generate image
        image_bytes = captcha.generate_image(value)
        if api_settings.SEND_URL:
            fs = FileSystemStorage(location=api_settings.STORAGE_PATH)
            filename = fs.save('{}.png'.format(key), ContentFile(image_bytes))
            image_data = api_settings.IMAGE_URL + filename
            image_decode = 'url'
        else:
            image_data = base64.b64encode(image_bytes)
            image_decode = 'base64'

        data = {
            api_settings.CAPTCHA_KEY: key,
            api_settings.CAPTCHA_IMAGE: image_data,
            'image_type': 'image/png',
            'image_decode': image_decode
        }
        return response.Response(data)
