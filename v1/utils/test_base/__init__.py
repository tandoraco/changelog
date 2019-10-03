from collections import namedtuple

SerializerTestData = namedtuple('TestSerializerData', 'data is_valid')
AssertionErrors = namedtuple('AssertionErrors', 'key value')
