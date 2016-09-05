# supernado

Create, run and manage microservices with tornado and supervisor.

The goal is to orchestrate many services with python so that each service has it's own
threads an dependency stack.

We use [supervisor](http://supervisord.org) to monitor and control the running services.

We use [conda](https://github.com/conda/conda) to virtualize and manage the different environments.

We use [tornado](http://www.tornadoweb.org) as the default web framework, though this could easily be changed.


## Requirements

You need to be on a unix-like system (to take advantage of bash scripts), and to have miniconda installed that way:

    wget http://bit.ly/miniconda -O miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda
    export PATH="$HOME/miniconda/bin:$PATH"
    conda update --yes --all


## Hello world

To create your first project, you need to clone the repository:

    git clone https://github.com/bibmartin/supernado
    cd supernado

Now create the conda *virtual* environment for supervisor:

    conda env create -f supervisor.yml

Install your first service:

    ./installService.sh template

Run supervisor and your service:

    source activate supervisor
    supervisord
    supervisorctl start all

Your server should be running ; in typing `supervisorctl status`, you should get something like:

    > template                         RUNNING   pid 13135, uptime 0:00:07

You can test your service with:

    curl http://localhost:8001/foo/bar

    > Hello from service template. You've asked for uri foo/bar

## Create a new service

To create a new service, you need to create a new folder in `./services` with the appropriate files.
The simplest way to do it is to copy it from `./template_service` and tune it.

    cp -R template_service ./services/myOwnService

Edit `_config.yml` and change at least the `port` value (Each service has to listen to a different port ; you can increment 8002, 8003, etc). Or you can do it in one line:

    sed -i 's/port: 8001/port: 8002/g' ./services/myOwnService/_config.yml

Edit `_supervisord.conf` and replace `template` by `myOwnService`. Or do it with `sed`:

    sed -i 's/template/myOwnService/g' ./services/myOwnService/_supervisord.conf

You're almost done. Now you have to install the conda *virtual* environment and reload supervisor:

    ./installService.sh myOwnService
    source activate supervisor
    supervisorctl reload
    supervisorctl start all

It's running:

    supervisorctl status

    > myOwnService                     RUNNING   pid 13375, uptime 0:03:05
    > template                         RUNNING   pid 13374, uptime 0:03:05

    curl http://localhost:8002/foo/bar

    > Hello from service myOwnService. You've asked for uri foo/bar
