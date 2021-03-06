import os

from celery import Celery
import redis
import docker, django
from main.models import Project
from datetime import datetime
import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils import timezone
import subprocess
from main import additional, nginx_build
from prominformatics.settings import SERVER_NAME
django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prominformatics.settings")

app = Celery("prominformatics")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, kill_switch.s(), name='kill_switch')

@app.task(name='kill_switch')
def kill_switch(emergency=False):
    r = redis.StrictRedis(host='redis', port=6379, db=0)
    active_containers = json.loads(r.get('active_containers').decode('UTF-8'))

    clientAPI = docker.APIClient(base_url='unix://var/run/docker.sock')
    client = docker.from_env()

    for i in list(active_containers):
        tmp_date = clientAPI.inspect_container(i)['Created']
        if not emergency:
            if (int(str(datetime.now() - datetime.strptime(
                    '-'.join(tmp_date.split('T')[0].split(':')[0].split('-')) + ' ' + ':'.join(
                            tmp_date.split('T')[1].split(':'))[:8], '%Y-%m-%d %H:%M:%S')).split(':')[1])) >= 10:
                port = list(clientAPI.inspect_container(i)['NetworkSettings']['Ports'].keys())[0].split('/')[0]
                print(list(clientAPI.inspect_container(i)['NetworkSettings']['Ports'].keys())[0].split('/')[0])
                client.containers.get(i).remove(force=True)
                del active_containers[i]
                nginx_update.delay()
                additional.push_port(
                    port=port)
        else:
            port = list(clientAPI.inspect_container(i)['NetworkSettings']['Ports'].keys())[0].split('/')[0]
            print(list(clientAPI.inspect_container(i)['NetworkSettings']['Ports'].keys())[0].split('/')[0])
            client.containers.get(i).remove(force=True)
            del active_containers[i]
            nginx_update.delay()
            additional.push_port(
                port=port)
    r.set('active_containers', json.dumps(active_containers))

    print('task completed')

@app.task(name='project_clone')
def project_clone(element, personal_access_token):
    print()
    print(element)
    if not os.path.exists(f'/prominf/mediafiles/{element.split("/")[-1][0:-4]}/'):
        os.makedirs(f'/prominf/mediafiles/{element.split("/")[-1][0:-4]}/')
        clone_file = f'#!/bin/bash\ngit clone https://oauth2:{personal_access_token}@{"/".join(element.split("/")[2:])} /prominf/mediafiles/{element.split("/")[-1][0:-4]}'
        with open(f'/prominf/clone.sh', 'w') as file:
            file.write(clone_file)
        os.chmod(f'/prominf/clone.sh', 777)
        exit_code = subprocess.call(f'/prominf/clone.sh')

@app.task(name='element_build')
def element_build(element, id):
    print('building')
    project = Project.objects.get(id = id)
    project.status = 'on build'
    project.save(update_fields=["status"])
    image_name=element.split("/")[-1][0:-4]
    client = docker.from_env()
    client.images.build(path= f'/prominf/mediafiles/{element.split("/")[-1][0:-4]}', tag=image_name)
    project.status = 'approved'
    project.docker_status = 'approved'
    project.save(update_fields=["status", "docker_status"])

@app.task(name='update_nginx')
def nginx_update():
    nu = nginx_build.NginxConfFile(server_name=SERVER_NAME)
    _file = nu.create_nginx_config_file()
    print(_file)
    with open(f'/prominf/nginx_dynamically_build_files/nginx_build.sh', 'w') as file:
        file.write(f'''#!/bin/sh\ndocker exec -i prominformatics_nginx touch /nginx.conf\ndocker exec -i prominformatics_nginx chmod 666 /nginx.conf\ndocker exec -i prominformatics_nginx bash -c "echo '{_file}' > /nginx.conf"\ndocker exec -i prominformatics_nginx cp /nginx.conf /etc/nginx\ndocker exec -i prominformatics_nginx nginx -s reload''')
        os.chmod(f'/prominf/nginx_dynamically_build_files/nginx_build.sh', 666)
    exit_code = subprocess.call(f'/prominf/nginx_dynamically_build_files/nginx_build.sh')