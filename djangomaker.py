import sys
import os


def writefile(path, content):
    file = open(path, 'w')
    for string in content:
        file.write(string + '\n')
    file.close()


def readfile(path):
    file = open(path)
    content = file.read().splitlines()
    file.close()
    return content


if len(sys.argv) > 1:
    project = sys.argv[1]
else:
    project = input('Project: ')
if not os.path.exists(project):
    os.system(f'django-admin startproject {project}')
    print(f'[project] "{project}" create success')
    os.chdir(project)
    writefile('.gitignore', ['manage.py'])
    print('[file] ".gitignore" create success')
    writefile('Procfile', [f'web: gunicorn {project}.wsgi'])
    print('[file] "Procfile" create success')
    writefile('requirements.txt', [
        'gunicorn==20.1.0',
        'Django==4.0.2'
    ])
    print('[file] "requirements.txt" create success')
    os.chdir(project)
    settings = readfile('settings.py')
    for index in range(len(settings)):
        if settings[index] == 'from pathlib import Path':
            settings[index] = 'import os\nfrom pathlib import Path'
        elif settings[index] == '        \'DIRS\': [],':
            settings[index] = '        \'DIRS\': [os.path.join(BASE_DIR, \'templates\')],'
    writefile('settings.py', settings)
    print('[project] "settings.py" mpdify done')
    os.chdir('..')
else:
    os.chdir(project)

if len(sys.argv) > 2:
    app = sys.argv[2]
else:
    app = input('App: ')
if os.path.exists(app):
    print(f'[error] "{app}" already exist\n')
    os.system('pause')
    exit()

os.system(f'python manage.py startapp {app}')
print(f'[app] "{app}" create success')

if not os.path.exists('templates'):
    os.mkdir('templates')
os.chdir('templates')
os.mkdir(app)
os.chdir(app)
writefile('index.html', [
    '<!DOCTYPE html>',
    '<html>',
    '    <head>',
    '        <meta charset="utf-8">',
    '        <title>{{title}}</title>',
    '    </head>',
    '    <body>',
    '        {{body}}',
    '    </body>',
    '</html>'
])
print(f'[templates] "{app}/index.html" create success')

os.chdir(f'../../{project}')
urls = readfile('urls.py')
for index in range(len(urls)):
    if urls[index] == 'from django.urls import path':
        urls[index] += ', include'
    elif urls[index] == ']':
        urls[index] = f'    path(\'{app}/\', include(\'{app}.urls\')),\n]'
writefile('urls.py', urls)
print('[project] "urls.py" mpdify done')

os.chdir(f'../{app}')
writefile('urls.py', [
    'from django.urls import path',
    'from . import views',
    '',
    'urlpatterns = [',
    '    path(\'\', views.index),',
    ']'
])
print('[app] "urls.py" mpdify done')

views = readfile('views.py')
for index in range(len(views)):
    if views[index] == 'from django.shortcuts import render':
        views[index] += '\n'
    elif views[index] == '# Create your views here.':
        views.insert(index + 1, 'def index(request):')
        views.insert(index + 2, f'    return render(request, \'{app}/index.html\', {{')
        views.insert(index + 3, f'        \'title\': \'{project}-{app}\',')
        views.insert(index + 4, '        \'body\': \'DJANGO\',')
        views.insert(index + 5, '    })')
        break
writefile('views.py', views)
print('[app] "views.py" mpdify done')

os.chdir('..')
os.system('start cmd /k "python manage.py runserver"')
print('[server] running...')
os.system(f'start http://127.0.0.1:8000/{app}')
print()
os.system('pause')
