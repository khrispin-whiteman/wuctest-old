import arrow

def generateStudentNumber():
    student_number = arrow.now().format('YYMM')

    num_from_db = 0
    lenth = 4
    num = num_from_db + 1
    txt = str(num)
    x = txt.zfill(lenth)
    print('LEADING ZERO: ', x)

    # str(int(0000) + 1).zfill(len(4))
    # print(student_number)
    return student_number


import string
import random
def generateRandomNumber():
    length = 4
    random_str = ''.join(
        random.choice(string.digits) for _ in range(4)
    )
    print(random_str)
    return random_str

def generateStudentNumberRandomDigits(request):
    student_number = arrow.now().format('YYMM')
    length = 4
    random_str = ''.join(
        random.choice(string.digits) for _ in range(length)
    )

    random_str = int(random_str) + 1
    txt = str(random_str)
    x = txt.zfill(length)

    student_number = student_number + x
    # print('STUDENT NO: ', student_number + str(type(student_number)))
    # check if number already taken
    if StudentNumber.objects.filter(full_student_no__exact=student_number):
        print('Number Already Taken!')
        generateStudentNumberRandomDigits(request)
    else:
        return HttpResponse(student_number)

generateRandomNumber()
# generateStudentNumber()