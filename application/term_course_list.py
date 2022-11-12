from application.models import Course

def term_courses(term):
    course_list = list(Course.objects.aggregate(*[
        {
            '$lookup': {
                'from': 'course',
                'localField': 'year',
                'foreignField': 'year',
                'as': 'r1'
            }
        }, {
            '$match': {
                'year': term
            }
        }, {
            '$sort': {
                'courseID': 1
            }
        }
    ]))
    return course_list