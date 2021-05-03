## Instalação

- Instalação do Ambiente:

1. Instalando Pacotes:

```bash
pip install -r requirements.txt
```


2. Confituração Authtoken no settings.py:
```bash
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
               'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':(
                'rest_framework.permissions.IsAuthenticated',
    ),

}
```

3. Configurando Logging no settings.py:
```bash
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
    },
}
```

4. Migrate banco:
```bash
python manage.py migrate
```


- Instalação Celery (Linux):

1. Instalando o RabbitMQ:
```bash
sudo apt-get install rabbitmq-server
```
2. Criar um usuário, um virtual host e dar permissões para esse usuário no virtualhost:
```bash
sudo rabbitmqctl add_user myuser mypassword
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
```
3. Instalando Pacote e suas dependencias no projeto:
```bash
pip install celery
```
4. Adicionar configuração no settings.py:
```bash
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```
5. Na pasta do projeto (a mesma pasta do settings.py) crie um arquivo chamado celery.py:
```bash
rom __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nome_do_proj.settings')
app = Celery('nome_do_proj')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
```
6. Nessa mesma pasta do settings.py, você vai modificar o arquivo de pacote __init__.py:
```bash
from __future__ import absolute_import
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
```