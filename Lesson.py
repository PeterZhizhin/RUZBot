import datetime
import unittest


class Lesson():
    __base_lesson_str = "{}-{}\n{}\n{} в аудитории {}\n{}"
    __window_lesson_str = "Окно {}-{}\nДлительностью {}"
    __time_format = "%H:%M"
    one_hour_seconds = datetime.timedelta(hours=1)

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
                   self.discipline,
                   self.kindOfWork,
                   self.auditorium,
                   self.lecturer,
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
        res_list = []
        for i in range(len(lessons)-1):
            res_list.append(lessons[i])
            start = datetime.datetime.combine(datetime.date.today(), lessons[i+1].start)
            end = datetime.datetime.combine(datetime.date.today(), lessons[i].end)
            delta = start - end
            if delta > Lesson.one_hour_seconds:
                res_list.append(Lesson.__window_lesson_str.format(
                    lessons[i].end.strftime(Lesson.__time_format),
                    lessons[i+1].start.strftime(Lesson.__time_format),
                    str(delta)[:-3]
                ))
        res_list.append(lessons[len(lessons)-1])

        return "\n---------\n".join(map(str, res_list))


class TestLessons(unittest.TestCase):

    def test_print_lessons(self):
        from simplejson import loads
        vals = loads("""[
    {
        "auditorium": "401",
        "auditoriumOid": 253,
        "beginLesson": "9:00",
        "building": "М. Трехсвятительский пер., д. 8/2 стр.1",
        "date": "2015.10.05",
        "dayOfWeek": 1,
        "discipline": "Интегрированные коммуникации",
        "endLesson": "10:30",
        "group": "МИК151",
        "groupOid": 4850,
        "kindOfWork": "Лекция",
        "lecturer": "Евстафьев Д.Г.",
        "lecturerOid": 7105,
        "stream": null,
        "streamOid": 0,
        "subGroup": null,
        "subGroupOid": 0
    },
    {
        "auditorium": "401",
        "auditoriumOid": 253,
        "beginLesson": "16:40",
        "building": "М. Трехсвятительский пер., д. 8/2 стр.1",
        "date": "2015.10.05",
        "dayOfWeek": 1,
        "discipline": "Интегрированные коммуникации",
        "endLesson": "18:00",
        "group": "МИК151",
        "groupOid": 4850,
        "kindOfWork": "Лекция",
        "lecturer": "Евстафьев Д.Г.",
        "lecturerOid": 7105,
        "stream": null,
        "streamOid": 0,
        "subGroup": null,
        "subGroupOid": 0
    }
]        """)
        lessons = [Lesson(l) for l in vals]
        res = Lesson.get_printable_lessons(lessons)
        self.assertIsNotNone(res)
        print(res)

