from datetime import date, timedelta

def count_business_days(start_date, end_date):
    """
    Bonus Feature: Counts only weekdays (Mon-Fri) between two dates.
    This gives a realistic "working days" remaining count.
    """
    days = 0
    current = start_date
    while current < end_date:
        # 5 = Saturday, 6 = Sunday. We only count if it's 0-4 (Mon-Fri)
        if current.weekday() < 5:
            days += 1
        current += timedelta(days=1)
    return days

def calculate_priority_score(task_data):
    """
    Calculates a priority score for a task.
    Higher score = Higher priority.
    """
    
    # 1. Base Score (Importance)
    # Importance is 1-10. We multiply by 10 to give it a 10-100 baseline.
    score = task_data.get('importance', 5) * 10
    
    # 2. Urgency Logic (Date Intelligence Upgrade)
    due_date_str = task_data.get('due_date')
    if due_date_str:
        today = date.today()
        try:
            # Parse date string if needed
            if isinstance(due_date_str, str):
                due_date = date.fromisoformat(due_date_str)
            else:
                due_date = due_date_str
            
            # RAW DAYS (Calendar days)
            days_until_due = (due_date - today).days

            # BUSINESS DAYS (Bonus Logic)
            # If the deadline is in the future, check how many WORK days we actually have
            if days_until_due > 0:
                business_days = count_business_days(today, due_date)
            else:
                business_days = days_until_due # Keep it negative or zero if overdue

            if days_until_due < 0:
                # OVERDUE: Massive boost. The more overdue, the higher the score.
                score += 100 + (abs(days_until_due) * 5)
            elif days_until_due == 0:
                # DUE TODAY: Big boost
                score += 50
            elif business_days <= 2:
                # DUE SOON (Only 2 working days left!): Panic mode boost
                # We use business_days here instead of raw days
                score += 40 
            elif business_days <= 5:
                # DUE THIS WEEK (1 work week): High boost
                score += 20
            elif days_until_due <= 7:
                # Calendar week, but plenty of work days
                score += 10
                
        except ValueError:
            pass

    # 3. Effort Logic (Quick Wins)
    estimated_hours = task_data.get('estimated_hours', 0)
    if estimated_hours <= 2:
        score += 10  # Quick win bonus
    elif estimated_hours >= 8:
        score -= 5   # Penalty for huge tasks (break them down!)

    # 4. Dependency Logic (NEW ADDITION)
    # Requirement: "Weigh dependencies"
    # Logic: If a task has dependencies, it is blocked. We reduce its score 
    # so unblocked tasks (the blockers) appear higher.
    dependencies = task_data.get('dependencies')
    # We check if it's a string and not empty to avoid errors
    if dependencies and isinstance(dependencies, str) and len(dependencies.strip()) > 0:
        score -= 30  # "Blocked" Penalty. It moves down the list.

    return score