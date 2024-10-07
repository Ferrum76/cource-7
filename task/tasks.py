from celery import shared_task

from task.models import Task
from task.services import send_tg_message


@shared_task
def task_track(habit_id):
    """
    Таск Celery для напоминания о выполнении привычки
    """
    remind_of_task(habit_id)


def remind_of_task(task_id):
    """
    Напоминание о выполнении привычки
    """
    task = Task.objects.get(pk=task_id)
    if task.user.chat_id:
        message = f'''Привет!\nНе забудь сегодня выполнить привычку: "{task.action}" в {task.time.strftime("%H:%M")}\n
        Место: {task.place}'''
        send_tg_message(message, task.user.chat_id)
