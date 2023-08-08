class Task:
    NOTION_TO_THINGS_STATUS_MAP = {
        None: 0,
        "Not started": 0,
        "In progress": 0,
        "Completed": 3,
        "incomplete": 0
    }

    def __init__(self, title, status, things_id=None, notion_id=None, last_updated=None):
        self.title = title
        self.notion_id = notion_id
        self.things_id = things_id  # Assign the passed things_id to the attribute
        self.last_updated = last_updated

        print(f"Debug: Processing task '{title}' with status '{status}'")
        if self.things_id:
            print(f"Debug Things UUID: {self.things_id}")

        # Check if the status exists in the mapping
        if status not in Task.NOTION_TO_THINGS_STATUS_MAP:
            print(f"Error: Status '{status}' not found in NOTION_TO_THINGS_STATUS_MAP")
        else:
            self.status_things = Task.NOTION_TO_THINGS_STATUS_MAP[status]
            self.status_notion = status

    def __repr__(self):
        return f"<Task(title={self.title}, status_notion={self.status_notion}, status_things={self.status_things}, last_updated={self.last_updated})>"

def __repr__(self):
    return f"<Task(title={self.title}, status_notion={self.status_notion}, status_things={self.status_things}, things_id={self.things_id}, last_updated={self.last_updated})>"
