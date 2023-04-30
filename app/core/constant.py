from enum import Enum


class MyStringEnumMixin(str, Enum):
    def __str__(self):
        return str(self.value)


class Language(MyStringEnumMixin):
    EN = "en"
    KO = "ko"


class ContentType(MyStringEnumMixin):
    POST = "post"
    COMMENT = "comment"


class Order(MyStringEnumMixin):
    ASC = "asc"
    DESC = "desc"
