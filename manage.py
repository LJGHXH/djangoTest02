#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoTest02.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    # python manage.py runserver 0.0.0.0:80

    """
    创建一个app目录：python manage.py startapp [appname]
    创建一个sqlite数据库：python manage.py migrate， 这行代码会默认生成一个db.sqlite3文件
    定义一个数据库表：python manage.py startapp common，这将创建一个存放公共表顶一个common目录
    创建好后，需要让Django更新相应脚本：python manage.py makemigrations common。
        然后再次执行：python manage.py migrate，来更新数据库。
        日后每次更新数据库都需要执行上述两行命令
    为了创建管理员账户，可以输入：python manage.py createsuperuser，然后会让你确认用户名、邮箱、密码
    """

    """
    可以通过 python manage.py shell 命令，来直接输入并运行一些脚本，例如说现在需要添加Country表和Student表中的数据：
        from common.models import *
        c1 = Country.objects.create(name='中国')
        Student.objects.create(name='白月', grade=1, country=c1)
    而在Django ORM中，可以通过如下方式来实现通过外键表的其它信息来获得当前表所需查找的外键目标（例如学生表的国家信息是关联了自国家表id的外键，但我们又想通过国家名来更高效地过滤学生信息，则可以采取如下方式）
        Student.objects.filter(grade=1, country__name='中国').values('name','country__name')    # 注意是两条下划线
    同时可以使用 django.db.models.F() 来实现对返回信息的重命名：
        Student.objects.annotate(
            countryName=F('country__name'), 
            studentName=F('name')
        ).filter(grade=1, country__name='中国').values('studentName', 'countryName')
    可以通过外键表的部分信息查找与之关联表的信息，例如根据已有Country对象访问属于此国家的全部学生：
        Country.objects.get(name='中国').student_set.all().values()   # 将学生表小写并补上 _set 来获取所有反向外键的关联对象
    像这样的反向查找，若需要去重，可以使用 distinct()：
        Country.objects.filter(student__grade=1).values().distinct()
    如果对应的 ForeignKey 有定义反向访问字段 related_name= 则可以使用指定的反向访问名字（例如 =students ）:
        Country.objects.get(name='中国').students.all().values()
    """
