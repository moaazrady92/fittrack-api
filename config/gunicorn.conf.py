#gunicor = python wsgi production server

bind = '0.0.0.0:8000'
workers = 4 # each worker has a separate python process if one crashs other still serve (common formula = {2 x cpu cores} + 1)
threads = 2
#concurrent requests = workers X threads = 8
worker_class = 'sync' # sync = 1 request at a time unlike the ('eventlet' = async)
timeout = 120 # if request takes more than 2 minutes kill worker
accesslog = '-'
errorlog = '-'
capture_output = True
loglevel = 'info'

