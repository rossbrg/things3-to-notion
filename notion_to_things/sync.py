from datetime import datetime, timezone
from tasks_from_notion import get_notion_tasks, create_notion_task, update_notion_status
from tasks_from_things import get_things_tasks, create_things_task, update_things_status
from task import Task

notion_tasks = get_notion_tasks()
things_tasks = get_things_tasks()

# Mapping tasks by title for quick lookup
notion_tasks_by_title = {task.title: task for task in notion_tasks}
things_tasks_by_title = {task.title: task for task in things_tasks}

# For each task in Notion, check if it exists in Things. If not, create it in Things.
for task in notion_tasks:
    if task.title not in things_tasks_by_title:
        print(f"Creating task in Things: {task}")
        print(f"Debug Things UUID: {task.things_id}")
        create_notion_task(task.title, task.status_notion, task.things_id)

# For each task in Things, check if it exists in Notion. If not, create it in Notion.
for task in things_tasks:
    if task.title not in notion_tasks_by_title:
        print(f"Creating task in Notion: {task}")
        print(f"Debug: {task.title} has Things UUID: {task.things_id}")
        if task.things_id is not None:
            create_notion_task(task.title, task.status_notion, task.things_id)
        else:
            print(f"Debug: Skipping task '{task.title}' as it has no Things UUID.")


# Sync the status of tasks between Notion and Things
for task_title, things_task in things_tasks_by_title.items():
    if task_title in notion_tasks_by_title:
        notion_task = notion_tasks_by_title[task_title]
        if things_task.status != notion_task.status_things:
            if things_task.last_updated > notion_task.last_updated:
                print(f"Updating task in Notion: {things_task.title}")
                update_notion_status(things_task)
            else:
                print(f"Updating task in Things: {notion_task.title}")
                update_things_status(notion_task)

print("Sync complete!")
