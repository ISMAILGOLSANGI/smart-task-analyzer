import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from datetime import date
from .models import Task
from .scoring import calculate_priority_score
from .serializers import serialize_task

def generate_explanation(task_data):
    """
    Helper function to generate the 'Why' text for any task.
    Used by both 'analyze' and 'suggest' endpoints.
    """
    reasons = []
    
    # Importance
    imp = task_data.get('importance', 0)
    if imp >= 8: reasons.append("High Importance")
    elif imp <= 3: reasons.append("Low Importance")
    
    # Effort
    hours = task_data.get('estimated_hours', 0)
    if hours <= 2: reasons.append("Quick Win (<2h)")
    elif hours >= 8: reasons.append("High Effort")
    
    # Urgency (Simple display logic)
    due_str = task_data.get('due_date')
    if due_str:
        try:
            today = date.today()
            if isinstance(due_str, str):
                due_date = date.fromisoformat(due_str)
            else:
                due_date = due_str
                
            days_left = (due_date - today).days
            
            if days_left < 0: reasons.append("Overdue!")
            elif days_left == 0: reasons.append("Due Today")
            elif days_left <= 3: reasons.append("Urgent Deadline")
        except ValueError:
            pass
            
    # Dependency Check
    deps = task_data.get('dependencies')
    if deps and len(deps.strip()) > 0:
        reasons.append("Blocked by Dependency")

    return " + ".join(reasons) if reasons else "Standard Priority"


@csrf_exempt
def analyze_tasks(request):
    """
    API Endpoint: POST /api/tasks/analyze/
    [cite_start]Returns list sorted by priority score[cite: 33].
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tasks_data = data.get('tasks', [])
            
            processed_tasks = []
            for task in tasks_data:
                # 1. Calculate Score
                score = calculate_priority_score(task)
                task['priority_score'] = score
                
                # 2. Generate Explanation
                task['explanation'] = generate_explanation(task)
                
                processed_tasks.append(task)
            
            # Sort by score (Descending)
            processed_tasks.sort(key=lambda x: x['priority_score'], reverse=True)
            
            return JsonResponse({'tasks': processed_tasks, 'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

def suggest_tasks(request):
    """
    API Endpoint: GET /api/tasks/suggest/
    [cite_start]Returns top 3 tasks with explanations[cite: 33].
    """
    if request.method == 'GET':
        # 1. Get unfinished tasks from DB
        db_tasks = Task.objects.filter(completed=False)
        
        scored_tasks = []
        for db_task in db_tasks:
            task_dict = serialize_task(db_task)
            
            # 2. Calculate Score
            task_dict['priority_score'] = calculate_priority_score(task_dict)
            
            # 3. Generate Explanation (Now included!)
            task_dict['explanation'] = generate_explanation(task_dict)
            
            scored_tasks.append(task_dict)
            
        # 4. Sort and pick Top 3
        scored_tasks.sort(key=lambda x: x['priority_score'], reverse=True)
        suggestions = scored_tasks[:3]
        
        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'error': 'Only GET method allowed'}, status=405)

def index(request):
    return render(request, 'tasks/index.html')