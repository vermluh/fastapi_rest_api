######
Deploy
######



***************
Clone this repo
***************

::

  [ziggy@stardust ~]$ git clone https://github.com/bwiessneth/fastapi_rest_api.git fastapi_rest_api/
  [ziggy@stardust ~]$



******************************************************
Setup python environment and install required packages
******************************************************

You definitely want to create a isolated python environment. That way the required packages you are going to install with ``pip`` are encapsulated form your systemwide python installation. For more info check https://virtualenv.pypa.io/en/latest/

::

  [ziggy@stardust ~]$ cd fastapi_rest_api
  [ziggy@stardust fastapi_rest_api]$ virtualenv -p python3 ENV
  [ziggy@stardust fastapi_rest_api]$ pip install -r deploy/requirements.txt
  [ziggy@stardust fastapi_rest_api]$ 


You can activate your new python environment like this:

::

  [ziggy@stardust fastapi_rest_api]$ source ENV/bin/activate
  (ENV) [ziggy@stardust fastapi_rest_api]$

Once you're done playing with it, deactivate it with the following command:

::
  
  (ENV) [ziggy@stardust fastapi_rest_api]$ deactivate
  [ziggy@stardust fastapi_rest_api]$ 



******************************************************
Setup nginx
******************************************************

Create an endpoint where the app will be served from. I chose that my application should be served using http under ``/fastapi_rest_api`` using port ``1028``.
That way your default web endpoint ``/`` will be served by apache and display what's inside ``~/html``. 

On uberspace you'll want to use the built-in ``uberspace`` tool.

:: 

  [ziggy@stardust ~]$ uberspace web backend set /fastapi_rest_api --http --port 1028 --remove-prefix



******************************************************
Start your application 
******************************************************

You can use Uvicorn, a lightning-fast ASGI server, built on uvloop and httptools to run your app. For more info head to https://www.uvicorn.org/.

To start Werkzeug execute ``run_uvicorn.sh`` from within the application directory.
It enables the virtual python environment and executes ``fastapi_rest_api.py``.

Once its running try to access it at https://ziggy.uber.space/fastapi_rest_api/users. Stop it by pressing ``Ctrl + C``.

::

  [ziggy@stardust fastapi_rest_api]$ ./run_uvicorn.sh
  ℹ INFO:     Started server process [20785]
  ℹ INFO:     Waiting for application startup.
  ℹ INFO:     Application startup complete.
  ℹ INFO:     Uvicorn running on http://0.0.0.0:1028 (Press CTRL+C to quit)
  [ziggy@stardust fastapi_rest_api]$ ^C
  [ziggy@stardust fastapi_rest_api]$



******************************************************
Use supervisord to monitor and control your processes 
******************************************************

Supervisor is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems.
For more info head to http://supervisord.org.

Copy the configuration file somewhere supervisord can find it. After that we tell supervisord to reread and update the found configurations. After that you can use ``status``, ``start`` and ``stop`` to control your application process.

::

  [ziggy@stardust ~]$ cp fastapi_rest_api/deploy/fastapi_rest_api.ini ~/etc/services.d/
  [ziggy@stardust ~]$ supervisorctl reread
  [ziggy@stardust ~]$ supervisorctl update
  [ziggy@stardust ~]$ supervisorctl start fastapi_rest_api
  ℹ fastapi_rest_api: started
  [ziggy@stardust ~]$ supervisorctl status fastapi_rest_api  
  ℹ fastapi_rest_api             RUNNING   pid 30707, uptime 0:00:34
  [ziggy@stardust ~]$ supervisorctl stop fastapi_rest_api
  ℹ fastapi_rest_api: stopped
  [ziggy@stardust ~]$ 
