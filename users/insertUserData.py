#coding=utf-8
def insert():
    from django.contrib.auth.models import User
    from random import choice
    import string
    def GenPassword(length=8, chars=string.ascii_letters + string.digits):
        return ''.join([choice(chars) for i in range(length)])

    with open('users/usernames.txt', encoding='utf-8') as f:

        for line in f:
            name = line.strip()

            pw = GenPassword(8)

            try:
                User.objects.create_user(username=name, password=pw)
            except Exception as e:
                print(e)
                print('插入错误的用户名', name)


insert()
