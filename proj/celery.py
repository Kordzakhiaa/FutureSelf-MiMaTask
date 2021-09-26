from celery import Celery
from celery.schedules import crontab

app = Celery('proj',
             broker='amqp://',
             backend='rpc://',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)


@app.task
def test(arg):
    print(arg)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    sender.add_periodic_task(
        crontab(minute=1),
        test.s('Testing:) mail sending'),
        expires=1
    )


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}

app.conf.timezone = 'Asia/Tbilisi'

if __name__ == '__main__':
    setup_periodic_tasks()
