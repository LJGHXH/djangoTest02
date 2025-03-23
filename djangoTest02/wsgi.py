"""
WSGI config for djangoTest02 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

"""
python网络编程中通常遵循WSGI标准，即由【client 《=》 server 《=》 application】组成。
server在其中负责处理http请求，实际的后端功能则由application执行（但server本身也是后端的一部分）。
并且会根据具体的工作情况分配相应进程（也可能是线程？）以方便并行处理多个任务。
于Django而言，它只提供了简单的server，其重心在application上。
成熟的server框架有：gunicorn、apache、Nginx、uWSGI、etc.
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoTest02.settings')

application = get_wsgi_application()
