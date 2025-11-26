from django.core.serializers.json import DjangoJSONEncoder
import json

def serialize_task(task_obj):
    """
    Manual serializer to convert a Task database model into a dictionary.
    We do this manually since we aren't using Django REST Framework 
    (to keep dependencies simple as per instructions).
    """
    return {
        "id": task_obj.id,
        "title": task_obj.title,
        "due_date": task_obj.due_date.isoformat() if task_obj.due_date else None,
        "estimated_hours": task_obj.estimated_hours,
        "importance": task_obj.importance,
        "dependencies": task_obj.dependencies,
        "completed": task_obj.completed
    }