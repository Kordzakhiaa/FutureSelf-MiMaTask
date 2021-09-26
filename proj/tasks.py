from smtplib import SMTP

from proj.celery import app


@app.task
def test(arg):
    print(arg)


@app.task
def mail_to_myself(email: str, password: str, title: str, body: str) -> None:
    with SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email, password)

        msg = f'Subject: {title}\n\n{body}'
        smtp.sendmail(email, email, msg)


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
