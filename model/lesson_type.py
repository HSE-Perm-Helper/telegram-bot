import enum


class LessonType(enum.Enum):
    def __new__(cls, display_name: str, short_name: str):
        obj = object.__new__(cls)
        obj._value_ = display_name
        obj.display_name = display_name
        obj.short_name = short_name
        return obj

    LECTURE = ('лекция 😴', "лек.")
    SEMINAR = ('семинар 📗', "сем.")
    # SEMINAR = ('семинар 📓', "сем.") # halloween
    COMMON_MINOR = ('Майнор Ⓜ', "майнор")
    ENGLISH = ('английский 🆎', "англ.")
    EXAM = ('экзамен ☠️', "экз.")
    INDEPENDENT_EXAM = ('независимый экзамен ☠️☠️', "независим. экз.")
    TEST = ('зачёт ☠️', "зачёт")
    PRACTICE = ('практика 💼', "практ.")
    MINOR = ('Майнор Ⓜ', "майнор")
    COMMON_ENGLISH = ('английский 🆎', "англ.")
    STATEMENT = ('ведомость 📜', "ведомость")
    ICC = ('МКД 📙', "МКД")
    UNDEFINED_AED = ('ДОЦ по выбору 📕', "ДОЦ")
    AED = ('ДОЦ 📕', "ДОЦ")
    CONSULT = ('консультация 🗿', "консулт.")
    EVENT = ('мероприятие', "мероприятие")

    @classmethod
    def _missing_(cls, value):
        return None
