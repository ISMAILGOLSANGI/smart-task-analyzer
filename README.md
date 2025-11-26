# Smart Task Analyzer

A Django-based task management system that intelligently scores and prioritizes tasks based on urgency, importance, effort, and dependencies.

## Setup Instructions

1. **Clone the repository** (or extract the project folder).

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Initialize the Database**
   ```bash
   python manage.py migrate

5. **Start the Server**
   ```bash
   python manage.py runserver

6. Open your browser at
    ```bash
   http://127.0.0.1:8000/.

## Algorithm Explanation
The core priority algorithm (tasks/scoring.py) calculates a numerical score for each task based on four weighted factors. Higher scores indicate higher priority.

Importance (Base Score):

The user's importance rating (1-10) is multiplied by 10 to create a strong baseline (10-100 points).

Urgency (Date Intelligence):

Past Due: Critical priority. Receives +100 points plus extra points for every day late.

Business Days Logic: The algorithm detects weekends. A task due in 4 days that includes a weekend is treated as having only 2 working days, triggering a higher urgency bonus.

Panic Mode: Tasks with ≤ 2 business days remaining receive a +40 point bonus.

Effort (Quick Wins):

Tasks estimated at ≤ 2 hours receive a +10 point "Quick Win" bonus to encourage clearing small items.

Massive tasks (≥ 8 hours) receive a small penalty (-5 points) to encourage breaking them down.

Dependency Logic:

If a task has dependencies listed (e.g., "Waiting on Task A"), it is considered Blocked.

It receives a -30 point penalty.

Why? This ensures that "Blocker" tasks (which are free to start) naturally float to the top, while blocked tasks stay lower until they are unblocked.

## Design Decisions & Trade-offs
Logic Separation: The scoring logic was intentionally moved to scoring.py rather than keeping it in views.py. This keeps the code clean, testable, and maintainable.

Client-Side vs Server-Side Sorting:

"Smart Balance" runs on the Python backend because the weighted logic is complex.

"Fastest Wins" / "High Impact" are handled instantly in the Frontend (JavaScript) to provide immediate user feedback without reloading the server.

Circular Dependencies:

Trade-off: For this assignment, I chose not to implement a graph cycle detection algorithm (e.g., Depth First Search).

Reasoning: I prioritized code readability and a robust scoring algorithm over complex graph theory features for this MVP. In a production environment, I would add a validation layer to reject circular dependencies on input.

## Bonus Challenges Completed
Date Intelligence: The algorithm calculates Business Days (excluding weekends). A task due on Monday is treated as "Urgent" on the preceding Friday.

Unit Tests: Implemented comprehensive unit tests in tasks/tests.py to verify the scoring logic.


Frontend Polish: Enhanced the UI with a clean, modern design, visual priority indicators, and loading states for better UX.
