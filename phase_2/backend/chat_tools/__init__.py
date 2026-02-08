from .add_task import add_task_handler
from .list_tasks import list_tasks_handler
from .complete_task import complete_task_handler
from .update_task import update_task_handler
from .delete_task import delete_task_handler

MCP_TOOLS = {
    "add_task": add_task_handler,
    "list_tasks": list_tasks_handler,
    "complete_task": complete_task_handler,
    "update_task": update_task_handler,
    "delete_task": delete_task_handler
}
