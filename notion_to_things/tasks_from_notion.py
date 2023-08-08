import os
from notion_client import Client
from task import Task  # Assuming Task is imported from a module named task in the same package
from dotenv import load_dotenv
load_dotenv()

NOTION_DATABASE_ID = os.environ['NOTION_DATABASE_ID']
NOTION_TOKEN = os.environ['NOTION_TOKEN']

def get_all_notion_tasks():
    """Fetch all notion tasks using the new notion-sdk-py."""
    print("Debug:", NOTION_DATABASE_ID)  # Add this line
    NOTION_TOKEN = os.environ['NOTION_TOKEN']
    notion_task_lists = os.environ['NOTION_DATABASE_ID']
    tasks = []
    
    # Initialize the client using notion-sdk-py
    notion = Client(auth=NOTION_TOKEN)

    database_id = NOTION_DATABASE_ID
    results = notion.databases.query(database_id=database_id).get("results")
    tasks.extend(results)
    return tasks

def get_notion_tasks():
    """Fetch tasks from Notion using the new SDK."""
    all_tasks = get_all_notion_tasks()
    tasks = []
    
    for t in all_tasks:
        # Extracting necessary details from the task
        name = t["properties"]["Name"]["title"][0]["text"]["content"]
        status = t["properties"]["Status"]["select"]["name"] if "Status" in t["properties"] else None
        last_edited_time = t["last_edited_time"]
        
        print(f"Debug status: '{status}'")
        tasks.append(
            Task(name, status, last_updated=last_edited_time)
        )
    return tasks

def update_notion_status(things_task):
    """Update a task's status in Notion based on its status in Things 3 using the new SDK."""
    NOTION_TOKEN = os.environ['NOTION_TOKEN']
    notion_status = Task.THINGS_TO_NOTION_STATUS_MAP.get(things_task.status, "To Do")
    update_payload = {
        "properties": {
            "Status": {
                "select": {
                    "name": notion_status
                }
            }
        }
    }
    
    # Initialize the client using notion-sdk-py
    notion = Client(auth=NOTION_TOKEN)

    # Update the task in Notion
    notion.pages.update(page_id=things_task.notion_id, **update_payload)
# Any other necessary code or functions can be added here


def create_notion_task(title, status, things_uuid):
    print(f"Debug: Things UUID being passed to create_notion_task: {things_uuid}")
    """Create a new task in Notion with a given title, status, and Things UUID."""
    notion = Client(auth=NOTION_TOKEN)

    # Define the properties for the new task
    new_task_properties = {
        "Title": [{"text": {"content": title}}],
        "Status": {"name": status},
        "Things_UUID": [{"text": {"content": things_uuid}}],
    }

    # Create the new task in the Notion database
    new_task = notion.pages.create(
        parent={"database_id": NOTION_DATABASE_ID},
        properties=new_task_properties
    )

    return new_task
