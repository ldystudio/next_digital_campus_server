from rest_framework.throttling import SimpleRateThrottle


class ImageCaptchaThrottle(SimpleRateThrottle):
    scope = 'image_captcha'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request),
        }


class EmailCaptchaThrottle(SimpleRateThrottle):
    scope = 'email_captcha'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request),
        }
