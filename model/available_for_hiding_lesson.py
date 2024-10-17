import dataclasses

from model.lesson_type import LessonType


@dataclasses.dataclass
class AvailableForHidingLesson:
    lesson: str
    lesson_type: LessonType
    sub_group: int | None