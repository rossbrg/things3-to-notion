from things import api as things_api
from things import database as things_db
import sqlite3
import os
import webbrowser
import urllib
from task import Task
from sys import exit

from dotenv import load_dotenv
load_dotenv()

THINGS_AUTH_TOKEN = os.environ['THINGS_AUTH_TOKEN']


def update_things_status(notion_task, id):
    print("Updating task in Things: {}".format(notion_task))
    completed = notion_task.status_things == 3
    webbrowser.open(
        "things:///update?id={}&completed={}&auth-token={}".format(id, str(completed).lower(), THINGS_AUTH_TOKEN))


def create_things_task(notion_task):
    print("Creating task in Things: {}".format(notion_task))
    title = urllib.parse.quote(notion_task.title)
    completed = notion_task.status_things == 3
    webbrowser.open(
        "things:///add?title={}&completed={}&tags=notion".format(title, str(completed).lower()))




def get_things_tasks():
    tasks = []
    things_tasks = things_api.tasks(type="to-do")
    for task in things_tasks:
        tasks.append(Task(task['title'], task['status'], task['uuid'], task['modified']))
    return tasks




if __name__ == '__main__':
    for t in get_things_tasks():
        print(t)
