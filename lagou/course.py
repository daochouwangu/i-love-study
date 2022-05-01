from lagou.request import get


def get_course_info(course_id, token):
    r = get(
        'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessons',
        {'courseId': course_id},
        token
    )
    return r.json()


def get_course_lesson_info(lesson_id, token):
    r = get(
        'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessonDetail',
        {'lessonId': lesson_id},
        token
    )
    return r.json()


def get_course_meta_info(course_id, token):
    r = get(
        'https://gate.lagou.com/v1/neirong/app/getCourseBaseInfo',
        {'courseId': course_id},
        token
    )
    return r.json()
