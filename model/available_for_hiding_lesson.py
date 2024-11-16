import dataclasses

from model.lesson_type import LessonType


@dataclasses.dataclass
class AvailableForHidingLesson:
    lesson: str
    lesson_type: LessonType
    sub_group: int | None

    def __hash__(self):
        return hash((self.lesson, self.lesson_type, self.sub_group))

    @staticmethod
    def from_dict(d: dict[str, str | None]):
        return AvailableForHidingLesson(
            lesson=d["lesson"],
            lesson_type=LessonType[d["lesson_type"]],
            sub_group=d["sub_group"]
        )


    def to_dict(self) -> dict:
        return {
            "lesson": self.lesson,
            "lesson_type": self.lesson_type.name,
            "sub_group": self.sub_group
        }

