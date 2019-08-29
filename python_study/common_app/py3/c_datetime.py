# coding: utf-8
# 时区相关操作
from datetime import datetime
from pytz import timezone

now = datetime.now()
tz = timezone('America/Ensenada')
now_1 = now.replace(tzinfo=tz)
now.astimezone()
