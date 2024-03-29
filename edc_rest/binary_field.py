from base64 import b64encode, b64decode

from django.utils.encoding import force_bytes
from django.utils.translation import gettext as _

from rest_framework.fields import Field
from rest_framework.fields import empty


class BinaryField(Field):

    default_error_messages = {
        'invalid': _('Value must be valid Binary.')
    }

    def to_internal_value(self, data):
        if isinstance(data, bytes):
            return memoryview(b64decode(force_bytes(data))).tobytes()
        return data

    def to_representation(self, value):
        if isinstance(value, bytes):
            return b64encode(force_bytes(value)).decode('ascii')
        return value

    def run_validation(self, data=empty):
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data
        value = self.to_internal_value(data)
        self.run_validators(value)
        return value
