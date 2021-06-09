from collections import namedtuple

SerializerTestData = namedtuple('TestSerializerData', 'data is_valid')
AssertionErrors = namedtuple('AssertionErrors', 'key value')


class TestResponse:

    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    @property
    def ok(self):
        return 200 <= self.status_code < 300
