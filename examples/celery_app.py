from celery import Celery

# Create a Celery instance and configure it to use Redis as the message broker
app = Celery("example", broker="redis://localhost:6379/0")

# Define a task
@app.task
def long_running_task(x):
  import time
  time.sleep(15) # simulate a long-running operation
  return x*x
