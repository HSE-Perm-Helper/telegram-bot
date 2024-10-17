import dataclasses

from model.lesson_type import LessonType


@dataclasses.dataclass
class AvailableForHidingLesson:
    lesson: str
    lesson_type: LessonType
    sub_group: int | None

    def __hash__(self):
        return hash((self.lesson, self.lesson_type, self.sub_group))
