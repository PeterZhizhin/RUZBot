import datetime


class Lesson:
    __base_lesson_str = "{}-{}\n{} в {}-м\n{}\n{}"
    __time_format = "%H:%M"

    def __init__(self, json_dict):
        self.date = datetime.date(*map(int, json_dict['date'].split('.')))
        self.dayofweek = int(json_dict['dayOfWeek'])
        self.start = json_dict['beginLesson'].split(':')
        self.start = datetime.time(int(self.start[0]), int(self.start[1]))
        self.end = json_dict['endLesson'].split(':')
        self.end = datetime.time(int(self.end[0]), int(self.end[1]))

        self.kindOfWork = json_dict['kindOfWork']
        self.auditorium = json_dict['auditorium']
        self.lecturer = json_dict['lecturer']
        self.discipline = json_dict['discipline']
        self.building = json_dict['building']

    def __eq__(self, other):
        return self.start.__eq__(self.end)

    def __ne__(self, other):
        return self.start.__ne__(self.end)

    def __lt__(self, other):
        return self.start.__lt__(self.end)

    def __gt__(self, other):
        return self.start.__gt__(self.end)

    def __ge__(self, other):
        return self.start.__ge__(self.end)

    def __le__(self, other):
        return self.start.__le__(self.end)

    def __str__(self):
            return Lesson.__base_lesson_str.format(
                   self.start.strftime(Lesson.__time_format),
                   self.end.strftime(Lesson.__time_format),
                   self.kindOfWork,
                   self.auditorium,
                   self.lecturer,
                   self.discipline
            )

    @staticmethod
    def split_days(lessons):
        result = []
        currentDate = None
        appendingArray = None
        for lesson in lessons:
            if lesson.date != currentDate:
                currentDate = lesson.date
                appendingArray = []
                result.append(appendingArray)
            appendingArray.append(lesson)
        return result

    @staticmethod
    def get_printable_lessons(lessons):
        if not lessons:
            return None
        return "\n---------\n".join(map(str, lessons))

