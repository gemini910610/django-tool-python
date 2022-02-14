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
    print(f'[error] "{project}" does not exist')
    print()
    os.system('pause')
    exit()

if len(sys.argv) > 2:
    herokuApp = sys.argv[2]
else:
    herokuApp = input('HerokuApp: ')

if len(sys.argv) > 3:
    commit = sys.argv[3]
else:
    commit = input('Commit message: ')

os.chdir(project)
if not os.path.exists('.git'):
    print('[git] start git init')
    os.system('git init')
    print()
os.chdir(project)
settings = readfile('settings.py')
for index in range(len(settings)):
    if settings[index] == 'DEBUG = True':
        settings[index] = 'DEBUG = False'
    elif settings[index] == 'ALLOWED_HOSTS = []':
        settings[index] = f'ALLOWED_HOSTS = [\'{herokuApp}.herokuapp.com\']'
writefile('settings.py', settings)
print('[file] "settings.py" modify done')
print()
os.chdir('..')

print('[git] start git remote')
os.system(f'heroku git:remote -a {herokuApp}')
print()
print('[git] start git add')
os.system('git add .')
print()
print('[git] start git commit')
os.system(f'git commit -m {commit}')
print()
print('[git] start git push')
os.system('git push heroku master')
print()
os.system('heroku ps:scale web=1')
os.system('heroku open')
print()

os.chdir(project)
settings = readfile('settings.py')
for index in range(len(settings)):
    if settings[index] == 'DEBUG = False':
        settings[index] = 'DEBUG = True'
    elif settings[index] == f'ALLOWED_HOSTS = [\'{herokuApp}.herokuapp.com\']':
        settings[index] = 'ALLOWED_HOSTS = []'
writefile('settings.py', settings)
print('[file] "settings.py" modify done')
print()
os.system('pause')
