import pygsheets
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.parsers import JSONParser


TABLE_NAME = 'sfhh_test'
RECIPIENT_EMAIL = 'geterodyn@gmail.com'
EDITED_FLAG = 'Edited'  # Название поля в таблице, по которому проверяем правку 
PERIOD = 30             # Количество новых регистраций, после которого список отправляется на почту

def mail_body(data):
    '''Генерация тела письма для отпправки'''
    body = ''
    if isinstance(data, dict):
        for key, value in data.items():
            body += f"{key}: {value}\n"
    elif isinstance(data, list):
        for record in data:
            if record[EDITED_FLAG] == "TRUE":
                for key, value in record.items():
                    body += f"{key}: {value}\n"
                body += "################################\n"
    return body

@csrf_exempt
def post_to_googlesheet(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)  # Python dict
        client = pygsheets.authorize()      # Авторизация в Google API, файл client_secret.json должен лежать в корневой папке
        sh = client.open(TABLE_NAME)        # Объект таблицы
        wks = sh.sheet1                     # Объект вкладки, по умолчанию первая
        wks.append_table(list(data.values()))
        send_mail(
            'Новая регистрация',
            mail_body(data), 
            settings.EMAIL_HOST_USER, 
            [RECIPIENT_EMAIL], 
            fail_silently=False)
        all_records = wks.get_all_records() # list of dicts
        if len(all_records) % PERIOD == 0:
            send_mail(
                'Список регистраций с правкой резюме',
                mail_body(all_records[-PERIOD:]),
                settings.EMAIL_HOST_USER, 
                [RECIPIENT_EMAIL], 
                fail_silently=False)
        return HttpResponse('OK')
        