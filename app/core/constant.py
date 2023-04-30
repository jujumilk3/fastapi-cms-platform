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


class OrderType(MyStringEnumMixin):
    ASC = "asc"
    DESC = "desc"


class OrderByType(MyStringEnumMixin):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    LIKE_COUNT = "like_count"
    COMMENT_COUNT = "comment_count"


class ReactionType(MyStringEnumMixin):
    LIKE = "like"
    DISLIKE = "dislike"
