## Instalação:

- Instalação do Ambiente:

1. Instalando Pacotes:

```bash
pip install -r requirements.txt
```

2. Configuracao RestFramework:
Incluir o pacote do REST e o app no settings.py

```bash
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'app'
]
```

3. Confituração Authtoken no settings.py:
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

4. Configurando Logging no settings.py:
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

5. Migrate banco:
```bash
python manage.py migrate
```

6. CreateSuperuser:
```bash
python manage.py createsuperuser
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
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teste_cedro.settings')
app = Celery('teste_cedro')

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
## Utilização:
1. Login: Utilizar o usuário criado na sessão de Instalação do ambiente para login:
```bash
{
	"username": "nome_de_usuario_aqui",
	"password": "senha_aqui"
}
```
O retorno deste endpoint será um Token que deve ser utilizado no header das outras chamadas Exemplo:
```bash
Authorization - Token Token beb29a9f63498aca75947a9ab567244d7cb18149
```

2. Credito Request: Endpoint para solicitação de crédito:
```bash
{
	"name": "Teste",
	"cpf": "22222222222",
	"birth_date": "1990-01-01",
	"credit_value": 40000.00
}
```

No retorno deste endpoint é possível resgatar o ticket_number que será utilizado para consultar o status da Proposta.

3. Status: Consulta o status da proposta através do ticket_number:
```bash
{
	"ticket_number": "202151"
}
```
## Observação:
A cada 1 min o celery vai ser acionado e processar todas as propostas com status "Proposta em analise". De acordo com as regras definidas no teste a proposta vai ser Aprovada ou Recusada.