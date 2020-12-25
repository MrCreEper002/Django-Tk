from io import StringIO
import json
import random
import datetime
import re
from ipaddress import ip_address

from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.forms import TextInput
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView
from django import forms
from .const import *
from .models import Post, Comment, PlayCity, Actor, ListFilmsActor
from .forms import CommentAdd, PostForm
from django.views.generic.edit import CreateView


# Create your views here.


def index(request):
    """Начальная страница"""
    post = Post.objects.all()
    array_comments = []
    list_comments = {}
    for i in post:
        comment = Comment.objects.filter(post_id=i.id)
        a = 0
        for j in comment:
            if a == 3:
                continue
            list_comments['id'] = j.post_id
            list_comments['name'] = j.name
            if len(j.body) > 50:
                list_comments['body'] = j.body[:50] + ' ...'
            else:
                list_comments['body'] = j.body
            a += 1
            array_comments.append(list_comments)
            list_comments = {}
    post = Post.objects.order_by("-id")
    return render(request, 'main/index.html', {
        "post": post,
        "comment": array_comments})


def main(request):
    success = False
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
    model = Post.objects.all()

    date = {
        'model': model,
        'form': PostForm(),
        'success': success,
    }

    return render(request, 'main/main.html', date)


class Main(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'main/main.html'
    success_url = reverse_lazy('main_g')
    success_msg = 'Запись создана'

    def get_context_data(self, **kwargs):
        kwargs['model'] = Post.objects.all()
        return super().get_context_data(**kwargs)


class HomeTasks(ListView):
    model = Post
    template_name = 'main/home_tasks.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        task = [
            {'id': 1, 'title': 'ФОРМЫ ДЛЯ АВТОРИЗАЦИИ И ВЫХОДА'},
            {'id': 2, 'title': 'РАЗДЕЛ УПРАВЛЕНИЯ КУКАМИ, СЕССИЯМИ И Т.Д.'},
            {'id': 3, 'title': 'ИГРА НА СЕССИЯХ (БИТВА АЛКОГОЛИКОВ)'},
            {'id': 4, 'title': 'ФАЙЛОВЫЙ МЕНЕДЖЕР'},
            {'id': 5, 'title': 'СОРТИРОВКА МНОГОМЕРНОГО МАССИВА'},
            {'id': 6, 'title': 'АБСОЛЮТНО ВЕРНАЯ ОБРАБОТКА ДАННЫХ'},
            {'id': 7, 'title': 'ПОИСК ПУТИ'},
            {'id': 8, 'title': 'ДАТА БЛИЖАЙШЕЙ ДОСТАВКИ'},
            {'id': 9, 'title': 'НЕ ЛЮБЛЮ ДЛИННЫЕ СЛОВА'},
            {'id': 10, 'title': 'БЫСТРОЕ РИСОВАНИЕ'},
            {'id': 11, 'title': 'СКОЛЬКО РАЗ ПОКАЗАЛИ КАРТИНКУ'},
            {'id': 12, 'title': 'ПЕРЕХОДЫ ПО ССЫЛКАМ'},
            {'id': 13, 'title': 'ВЫВЕСТИ ПОПУЛЯРНЫХ АКТЕРОВ'},
            {'id': 14, 'title': 'БЛОКИРОВАТЬ IP ОПРЕДЕЛЁННЫХ СТРАН'},
            {'id': 15, 'title': 'ПОПУЛЯРНАЯ ЗАДАЧА ДЛЯ ТРУДОУСТРОЙСТВА'},
            {'id': 16, 'title': 'ДВА ОБНОВЛЕНИЯ В ОДНОМ'},
            {'id': 17, 'title': 'ПОДСВЕТКА КЛЮЧЕВЫХ СЛОВ'},
            {'id': 18, 'title': 'АНТИ-БОТ'},
            {'id': 19, 'title': 'ИГРА В ГОРОДА'},
            {'id': 20, 'title': 'НЕ ВЫВОДИТЬ ДУБЛИ'},
        ]
        kwargs['task'] = task
        return super().get_context_data(**kwargs)


class Auth(forms.Form):
    login = forms.CharField(label=u'Логин', max_length=100,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label=u'Пароль', max_length=100,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.CharField(label=u'Email', max_length=100,
                            widget=forms.TextInput(attrs={"class": "form-control"}))


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)


def exit_cookies(request):
    response = redirect(reverse('auth'))
    response.delete_cookie('login')
    response.delete_cookie('name')
    response.delete_cookie('name1')
    return response


def TasksOne(request):
    error = ["<b>inpost</b>", "O'Henr''y", "Vo&quot;va", "Правда 1%", "ОбычныйUserId#1", "x&*5!@#$%^*&?",
             " \ \ YE / / ", "%%%%", "\\", "////"]
    task = ''
    date = {
        'form1': True,
        'title': 'Задача №1: Форма авторизации и выхода',
        'level': 1,
        'body': 'Необходимо сделать форму для авторизации на сайте, для этого делаются 3 обязательных поля: '
                'login, password, email. Если верно ввели - записываем в куки специальный ключ, при наличии '
                'которого выводим человеку кнопку "выйти из сайта". В момент выхода - удалить созданную куку..',
        'task': task,
        'exit': False,
        'error': False,
        'errorAuth': False
    }
    if 'login' in request.COOKIES:
        value = request.COOKIES['login']
        date['exit'] = True
        date['form1'] = False

            # return redirect(reverse('auth'))
        return render(request, 'main/tasks/tasks1.html', date)
    if request.method == 'POST':
        l = request.POST.get('login')
        p = request.POST.get('password')
        if l in error:
            date['error'] = True
        try:
            var = l.split()[1]
            date['error'] = True
        except:
            if l == 'alex' and p == '1':
                response = render(request, 'main/tasks/tasks1.html', date)
                set_cookie(response, 'login', l)
                date['form1'] = False
                return response
            else:
                date['errorAuth'] = True
    date['form'] = Auth
    return render(request, 'main/tasks/tasks1.html', date)


def del_cookies(request):
    response = redirect(reverse('setting'))
    try:
        response.delete_cookie('login')
        response.delete_cookie('name')
        response.delete_cookie('name1')
    except:
        pass
    return response


def del_session(request):
    response = redirect(reverse('setting'))
    unexpired_sessions = Session.objects.all()
    [
        session.delete() for session in unexpired_sessions
    ]
    return response


def TasksTwo(request):

    task = ''
    date = {
        'title': 'Задача №2: Раздел управления куками, сессиями и т.д.',
        'level': 1,
        'body': 'Создаём скрытую страницу "module=control" , в ней выводим весь массив куки и сессии. '
                'Добавляем 2 кнопки: "очистить куки" и "очистить сессию", которая должна выполнять '
                'указанные действия по нажатию. Кроме главного подраздела по управлению куки и сессией '
                'добавляем ещё 2: страницу с выводом phpinfo и страницу с выводом $_SERVER. '
                'Данный раздел защищаем паролем. Можно воспользоваться отдельной формой для входа, '
                'можно дать доступ админу сайта..',
        'task': task,
    }

    return render(request, 'main/tasks/tasks2.html', date)


class Play(forms.Form):
    enter_user = forms.IntegerField(label=u'Введи', widget=forms.TextInput(attrs={"class": "form-control"}))


def RESET(request):
    array_hp.clear()
    array_hp.append({"ход": 0, "user_xp": 10, "bot_xp": 10})
    return redirect(reverse('game'))


def TasksThree(request):
    if request.method == "POST":
        num_user = int(request.POST.get('enter_user'))
        if num_user > 4:
            num_user = random.randint(1, int(num_user))
        else:
            num_user = random.randint(1, int(num_user))
        num_bot = random.randint(1, 3)
        if num_user == num_bot:
            num = random.randint(1, 4)
            num_user = array_hp[-1]['user_xp'] - num
            num_bot = array_hp[-1]['bot_xp']
        else:
            num = random.randint(1, 4)
            num_bot = array_hp[-1]['bot_xp'] - num
            num_user = array_hp[-1]['user_xp']
        array_hp.append({"ход": array_hp[-1]['ход'] + 1, "user_xp": num_user, "bot_xp": num_bot})
    print(array_hp)
    task = ''

    date = {
        'form': Play,
        'title': 'Задача №3: Игра на сессиях (Битва алкоголиков)',
        'level': 1,
        'body': 'Мини-игра, цель которой показать, что алкоголизм - это плохо. Мы создаём страничку '
                '/index.php?page=game1 под игру. Создаются 2 персонажа, у обоих по 10хп (2 сессионных переменных), '
                'создаётся форма, где пользователь вводит число от 1 до 3 и отправляет запрос на сервер.'
                ' На сервере запустить rand(1,3), и если значение человека с значением случайным совпадает, '
                'то снимаются ХП с персонажа человека (клиента), если не совпадают - с серверного персонажа. '
                'Отнимать надо от 1 до 4хп, случайным образом). То есть вероятность 33%, что отнимутся'
                ' у клиента, и 66%, что у серверного персонажа. В момент, когда у одного из персонажей '
                'ХП становится 0 и ниже, - перебрасывать на другую страницу при помощи переадресации '
                '(header) на страницу index.php?module=games&page=game1over , и выводить текст, победил ли'
                ' игрок, или система. Не забываем, что для удобства пользователя необходимо выводить всю'
                ' известную информацию, то есть какой урон был нанесён, кто кому нанёс, сколько сейчас хп '
                'осталось у каждого игрока. Так же возможность начать игру заново. Желательно для корректировки '
                'системы использовать переменные-свойства, то есть 10hp - это $basehp , то есть изменив эту '
                'переменную скрипт будет иным.',
        'task': task,
        'xp': array_hp,
        'user_check': array_hp[-1]['user_xp'],
        'bot_check': array_hp[-1]['bot_xp'],
    }
    return render(request, 'main/tasks/tasks3.html', date)

def e(arr):
    l = '('
    for i in arr:
        l += f'{i} '
    l += ')'

    return l


def ll1():
    lvl_1_m_g = []
    lvl_1_all = []
    for i in array_fifteen:
        if i['age'] == '20':
            lvl_1_m_g.append(i['login'])
        else:
            lvl_1_all.append(i['login'])

    g_m = e(lvl_1_m_g)
    al = ' '.join(lvl_1_all[0:])
    return f'Первый уровень - {g_m} {al}'


def ll2():
    lvl_2_m = []
    lvl_2_g = []
    lvl_2_all = []
    for i in array_fifteen:
        if i['age'] == '20' and i['gender'] == 'm':
            lvl_2_m.append(i['login'])
        elif i['age'] == '20' and i['gender'] == 'g':
            lvl_2_g.append(i['login'])
        else:
            lvl_2_all.append(i['login'])

    g = e(lvl_2_g)
    m = e(lvl_2_m)
    al = ' '.join(lvl_2_all[0:])
    return f'Второй уровень - {g} {m} {al}'


def TasksFive(request):
    task = f'{ll1()}. {ll2()}'

    date = {
        'title': 'Задача №5: Сортировка многомерного массива',
        'level': 1,
        'body': "Имеется многомерный массив, необходимо его отсортировать. Для первого уровня достаточно отсортировать "
                "по полю `age`, для продвинутого пользователя - по двум полям, при этом должна быть возможность"
                " сортировать в обратном порядке, то есть для первого уровня: ORDER BY `age` ASC, и для высокого "
                "уровня: ORDER BY `age` ASC,`gender` DESC. Сам массив: [code]$array = array( 'a1' => array('id'=>'1', "
                "'age'=>'16', 'gender'=>'m', 'login'=>'Вася'), 'a2' => array('id'=>'2', 'age'=>'18', 'gender'=>'m',"
                " 'login'=>'Петя'), 'a3' => array('id'=>'3', 'age'=>'20', 'gender'=>'g', 'login'=>'Катя'), 'a4' =>"
                " array('id'=>'4', 'age'=>'20', 'gender'=>'m', 'login'=>'Стас'), 'a5' => array('id'=>'5', 'age'=>'12',"
                " 'gender'=>'g', 'login'=>'Маша'), 'a6' => array('id'=>'6', 'age'=>'44', 'gender'=>'g',"
                " 'login'=>'Галя'), 'a7' => array('id'=>'7', 'age'=>'45', 'gender'=>'m', 'login'=>'Макс'), "
                "'a8' => array('id'=>'8', 'age'=>'20', 'gender'=>'m', 'login'=>'Илья'), 'a9' => array('id'=>'9',"
                " 'age'=>'20', 'gender'=>'g', 'login'=>'Даша'), );[/code] Верный порядок: Для первого уровня: Маша, "
                "Вася, Петя, (Катя,Стас,Илья,Даша), Галя, Макс. Для среднего уровня: Маша, Вася, Петя, (Стас,Илья),"
                "(Катя,Даша),Галя,Макс. Обратите внимание, что в скобки взял те имена, которые местами могут не "
                "совпадать то той причине, что поля для сортировки в любом случае у них одинаковые..",
        'task': task,
    }
    return render(request, 'main/tasks/tasks5.html', date)


def g(a, now_str, array, list_name):
    for i in range(int(now_str.split('-')[1]), 32):
        if f'{now_str[0]}-{i}' not in a:
            n = f'{now_str.split("-")[0]}-{i}'
            if n == now_str:
                return 'Ближайшая доставка: Завтра'
            return f'Ближайшая доставка: {i} ' \
                   f'{[l for l in list_name if list_name.index(l) + 1 == int(now_str.split("-")[0])][0]}'


def check(now, now_str, array, list_name):
    a = [i for i in array for j in range(1, 32) if
         i.split('-')[0] == now_str.split("-")[0] and i.split('-')[1] == f'{j}']
    if now.hour >= 20:
        if not a:
            return 'Ближайшая доставка: Послезавтра'
        else:
            return g(a, now_str, array, list_name)
    else:
        if not a:
            return 'Ближайшая доставка: Завтра'
        else:
            return g(a, now_str, array, list_name)


class TasksEight(ListView):
    model = Post
    template_name = 'main/tasks/tasks8.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        title = 'Задача №8: Дата ближашей доставки'
        level = 1
        body = 'Необходимо вывести дату ближайшей доставки в формате: "30 ноября". ' \
               'Алгоритм следующий: если сегодня времени меньше, чем 20-00, то доставка завтра, если более 20-00, ' \
               'то послезавтра! Если день доставки попадает на праздничный день, ' \
               'то доставка переносится на следующий день после праздника. Праздники записываются в массиве в ' \
               'формате: "месяц-день": \'01-01\' - 1 января..'

        list_name = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
                     'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']

        array = ['1-2', '1-3', '1-4', '1-5', '1-6', '1-8', '2-24', '3-9', '3-30', '3-31', '4-1', '4-2', '4-3', '4-6',
                 '4-7', '4-8', '4-9', '4-10', '4-13', '4-14', '4-15', '4-16', '4-17', '4-20', '4-21', '4-22', '4-23',
                 '4-24', '4-27', '4-28', '4-29', '4-30', '5-4', '5-5', '5-6', '5-7', '5-8', '5-11', '7-1', '1-1',
                 '1-7', '2-23', '3-8', '5-1', '5-9', '6-12', '6-24', '11-4']

        now = datetime.datetime.now()
        now_str = f'{now.month}-{now.day}'

        task = f'Сегодня: {now_str.split("-")[1]} ' \
               f'{[l for l in list_name if list_name.index(l) + 1 == int(now_str.split("-")[0])][0]}. '
        task += check(now, now_str, array, list_name)

        kwargs['title'] = title
        kwargs['level'] = level
        kwargs['body'] = body
        kwargs['task'] = task
        return super().get_context_data(**kwargs)


class TasksNine(ListView):
    model = Post
    template_name = 'main/tasks/tasks9.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        title = 'Задача №9: Не люблю длинные слова'
        level = 1
        body = 'Дан длинный текст, в нём встречаются слова длиннее 7 символов! ' \
               'Если слово длиннее 7 символов, то необходимо: оставить первые 6 символа и добавить звёздочку. ' \
               'Остальные символы вырезаются. Шаблон: "я купил бронетранспортер вчера" Результат: "' \
               'я купил бронет* вчера"..'
        task = ''
        num = 'я купил бронетранспортер вчера'
        for i in num.split():
            if len(i) >= 7:
                task += i[:7] + '* '
                continue
            task += i + ' '

        kwargs['title'] = title
        kwargs['level'] = level
        kwargs['body'] = body
        kwargs['task'] = task
        return super().get_context_data(**kwargs)


def Tasks11(request):

    task = ''

    date = {
        'title': 'Задача №11: Сколько раз показалась картинка',
        'level': 2,
        'body': 'Обычно используется в двух вариантах, сколько раз была показана картинка или размещается '
                'пиксель, который фиксирует показ конкретной картинки с определённым идентификатором. '
                'Необходимо сделать: выставить на странице <img src="/banner.php">, '
                'где banner.php - наш скрипт, который ведёт подсчёт показов и в конце выдаёт картинку.',
        'task': task,
    }
    r = render(request, 'main/tasks/tasks11.html', date)
    set_cookie(r, '')
    return r


class TasksTwelve(ListView):
    model = Post
    template_name = 'main/tasks/tasks12.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        title = 'Задача №12: Переходы по ссылкам'
        level = 2
        body = 'Выставить ссылку на другой сайт. Считать, сколько раз была нажата ссылка. ' \
               'Задача предлагает показать оба варианта: чистый PHP, и, отдельно, JS + PHP.'

        task = ''

        kwargs['title'] = title
        kwargs['level'] = level
        kwargs['body'] = body
        kwargs['task'] = task
        return super().get_context_data(**kwargs)


class TasksThirteen(ListView):
    model = Actor
    template_name = 'main/tasks/tasks13.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        title = 'Задача №13: Вывести популярных актеров'
        level = 1
        body = 'Составить связку многие ко многим, где хранить будем фильмы и их актеров. ' \
               'Вывести только тех актеров, у которых фильмов более двух..'
        popular = ListFilmsActor.objects.all()
        counter = {}

        for elem in popular:
            print(elem.id_actor.name)
            counter[elem.id_actor.name] = counter.get(elem.id_actor.name, 0) + 1

        task = {element: count for element, count in counter.items() if count > 1}

        kwargs['title'] = title
        kwargs['level'] = level
        kwargs['body'] = body
        kwargs['array'] = popular
        kwargs['task'] = task
        return super().get_context_data(**kwargs)


class HandlerText(forms.Form):
    text = forms.CharField(label=u'Обработка шаблона', max_length=2046,
                           widget=forms.TextInput(attrs={"class": "form-control"}))


def check_re(af):
    h = re.findall(r'{(.*?)}', af)
    h1 = re.findall(r'{.*?}', af)
    try:
        if re.findall(r'({.*?{)', h1[0]):
            p = re.findall(r'{(.*?{.*?}.*?)}', af)
            p1 = re.findall(r'{.*?{.*?}.*?}', af)
            k = re.findall(r'{(.*?)}', p[0])

            if not re.findall(r'}.(.*)', p[0]):
                r = re.findall(r'}()', p[0])[0]
            else:
                r = re.findall(r'}(.*)', p[0])[0]
            msg = f"{re.findall(r'(.*?).{', p[0])[0]} {random.choice(k[0].split('|'))}{r}"
            return [random.choice(msg.split('|')), p1[0]]

        return [random.choice(h[0].split('|')), re.findall(r'{.*?}', af)[0]]
    except:
        return 0


def TasksFifteen(request):
    r = ''
    task = ''
    if request.method == "POST":
        r = request.POST.get('text')
        task = request.POST.get('text')
        while True:
            g = check_re(r)
            if not g:
                break
            elif g[1] != "":
                r = r.replace(g[1], g[0])
            else:
                break

    date = {
        'form': HandlerText(),
        'title': 'Задача №15: Попоулярная задача для трудоустройства',
        'level': 2.5,
        'body': open('tasks15.txt').read(),
        'task': r,
        'enter': task
    }
    return render(request, 'main/tasks/tasks15.html', date)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_REAL_IP')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def TasksFourteen(request):
    from ipaddress import ip_network
    task = get_client_ip(request)
    print(task)
    print(ip_address('49.12.0.1') in ip_network('49.12.0.0/14'))

    date = {
        'title': 'Задача №16: Блокировка ip определенных стран',
        'level': 1,
        'body': 'Есть диапазон IP: 49.05.0.0/20 , надо сравнить имеющийся ip: 49.05.100.152 с данным диапазоном, '
                'результат: true\\false. Если усложнить, то имеем сразу несколько диапазонов, которые вот в таком '
                'виде лежат в файле india.txt: '
                '49.12.0.0/14 49.32.0.0/12 49.50.64.0/18 49.128.108.0/22 49.128.160.0/20 49.136.0.0/14',
        'task': task,
    }
    return render(request, 'main/tasks/tasks14.html', date)


class Text(forms.Form):
    text = forms.CharField(label=u'Подсветка текста', max_length=2046,
                           widget=forms.TextInput(attrs={"class": "form-control"}))


def TasksSaventeen(request):
    task = ''
    # /((?:^|>)[^<]*)(".$search.")
    date = {
        'form': Text,
        'title': 'Задача №17: Подсветка ключевых слов',
        'level': 2.5,
        'body': 'Есть длинный текст и есть форма поиска по этому тексту. При вводе слова в форму поиска необходимо'
                ' найти все упоминания этого слова в тексте и выделить (подсветить) цветом, жирным или другим '
                'настраивающим способом. В случае, если указываются 2 слова, то каждое должно искаться индивидуально, '
                'если словосочетание указывается в кавычках,то ищется как единое словосочетание. Помимо грубого '
                'поиска так же должно находить слова с разными окончаниями: пиво, пива, пивом..',
        'task': task,
    }
    return render(request, 'main/tasks/tasks17.html', date)


class Captcha(forms.Form):
    text = forms.CharField(label=u'Введите капчу', max_length=2046,
                           widget=forms.TextInput(attrs={"class": "form-control"}))


def captcha_image():
    from PIL import Image, ImageDraw, ImageFont
    from random import randint, choice

    # key = ''.join([choice('QWERTYUIOPLKJHGFDSAZXCVBNM1234567890') for i in range(5)])
    key = '1T345'

    img = Image.new('RGB', (100, 50), 0xffffff)
    draw = ImageDraw.Draw(img)

    for i in range(40):
        draw.line([(randint(0, 100), randint(0, 50)), (randint(0, 100), randint(0, 50))], randint(0, 0xffffff), 1)

    font = ImageFont.truetype('font.ttf', 32)
    draw.text((0, 0), key, 0, font)

    f = StringIO()

    img.save('main/static/main/img/test.jpg', "JPEG")
    raw = f.getvalue()

    return key, raw


def Tasks18(request):
    captcha_image1 = captcha_image()[0]
    h = True
    a = 10
    b = 9

    if request.method == "POST":

        try:
            e = int(request.POST.get('text'))
            num = a + b
            if num == e:
                h = False
        except:
            e = request.POST.get('text')
            if e == captcha_image1:
                h = False


    task = f'{a}+{b}='

    date = {
        'form': Captcha,
        'title': 'Задача №18: Анти-Бот',
        'level': 2,
        'body': 'Создать 2 собственных капчи, первая - текстовая, вторая - графическая..',
        'task': task,
        'h': h
    }
    return render(request, 'main/tasks/tasks18.html', date)


class SomeForm(forms.Form):
    city = forms.CharField(label=u'Введите город', max_length=25,
                           widget=forms.TextInput(attrs={"class": "form-control"}))


def word_enter(word, msg_user, user_word, bot_word):
    word.user_word = msg_user
    if msg_user[-1].lower() in a_city:
        msg = [w for w in array_city if w.startswith(msg_user[-2].upper())]
    else:
        msg = [w for w in array_city if w.startswith(msg_user[-1].upper())]
    word.user_word = msg_user
    bot_enter = random.choice(msg)
    word.bot_word = bot_enter
    word.count_word = len(array_city) - len(user_word) - len(bot_word)


def taskNineteen(request):
    task = ''
    city = PlayCity.objects.all()

    user_word = [i.user_word for i in city if i.user_word]
    bot_word = [i.bot_word for i in city if i.bot_word]

    if request.method == "POST":
        word = PlayCity()
        msg_user = request.POST.get('city').split()[0].lower().title()
        if msg_user not in user_word:
            if msg_user not in array_city:
                word.error_user_word = msg_user
            else:
                if bot_word:
                    if msg_user[0] == bot_word[-1][-1].upper():
                        word_enter(word, msg_user, user_word, bot_word)

                    elif bot_word[-1][-1].lower() in a_city:
                        if msg_user[0] == bot_word[-1][-2].upper():
                            word_enter(word, msg_user, user_word, bot_word)
                        else:
                            word.error_start_word = msg_user
                    else:
                        word.error_start_word = msg_user
                else:
                    word_enter(word, msg_user, user_word, bot_word)

        else:
            task = 'Уже был этот город'
        word.save()

    date = {
        'form': SomeForm(),
        'title': 'Задача №19: Игра в города',
        'level': 1,
        'body': 'Создать базу городов. Далее участвуют человек и компьютер. Необходимо назвать город, дальше '
                'получаем ответ от компьютера с вероятностью в 97.4% название города, чьё название начинается '
                'на последнюю букву названного игроком города. Далее ситуация повторяется, игрок должен назвать '
                'город у которого название начинается с последней буквы названным опонентом города. Имена не могут '
                'повторяться..',
        'task': task,
        'words': PlayCity.objects.all(),
    }
    return render(request, 'main/tasks/tasks19.html', date)


def reset_game(request):
    PlayCity.objects.all().delete()
    return redirect(reverse('game_city'))


class TasksTwenty(ListView):
    model = Post
    template_name = 'main/tasks/tasks20.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        title = 'Задача №20: Не выводить дубли'
        level = 1
        body = 'У нас есть массив $array = array(1,1,1,2,2,2,2,3), необходимо вывести 1,2,3, то есть вывести' \
               ' без дублей при помощи лишь одного цикла foreach без использования функций группировки ' \
               'элементов массива и не нарушая данный массив..'
        num = [1, 1, 1, 2, 2, 2, 2, 3]
        task = []
        for i in num:
            if i not in task:
                task.append(i)
        kwargs['title'] = title
        kwargs['level'] = level
        kwargs['body'] = body
        kwargs['task'] = task

        return super().get_context_data(**kwargs)


def comments(request, pk):
    """Страница коментариев"""
    error = ''
    if request.method == "POST":

        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return ()  # обработка ошибки пост не найден

        person = Comment()
        person.name = request.POST.get("name")
        person.body = request.POST.get("body")
        person.post = post
        person.save()

    comment = Comment.objects.all()
    img = Post.objects.filter(id=pk)
    form = CommentAdd()
    date = {'form': form, "error": error, 'comment': comment, 'post_id': pk, 'img': img[0].image.url}
    return render(request, 'main/comments.html', date)


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'main/postadd.html'
    success_url = '/'
