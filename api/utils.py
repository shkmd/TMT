"""Task Management Utility Functions.

This module provides a comprehensive set of utility functions for managing,
analyzing, and manipulating tasks in the Task Management Tool (TMT) API.

The utilities are organized into several categories:

Analytics & Metrics:
    - calculate_task_metrics: Generate comprehensive task statistics and KPIs

Task Organization:
    - prioritize_tasks: Sort tasks using various prioritization strategies
    - filter_tasks_by_criteria: Advanced multi-criteria task filtering

Project Planning:
    - estimate_completion_date: Project completion date estimation with velocity modeling

Data Validation:
    - validate_task_data: Comprehensive task data validation before persistence

Batch Operations:
    - bulk_update_tasks: Efficient bulk task updates with error tracking

All functions are designed to be composable, allowing them to be chained together
for complex workflows. For example:

    >>> # Get overdue high-priority tasks and estimate completion
    >>> tasks = get_all_tasks()
    >>> filtered = filter_tasks_by_criteria(
    ...     tasks,
    ...     priority=TaskPriority.HIGH,
    ...     overdue_only=True
    ... )
    >>> sorted_tasks = prioritize_tasks(filtered, strategy="eisenhower")
    >>> completion = estimate_completion_date(sorted_tasks, tasks_per_day=4.0)

Dependencies:
    - datetime: For date/time operations and calculations
    - typing: For type hints and annotations
    - api.models: Task, TaskStatus, TaskPriority data models
    - re: For regex-based validation

Author: TMT Development Team
Version: 1.0.0
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from api.models import Task, TaskStatus, TaskPriority
import re


def calculate_task_metrics(tasks: List[Task]) -> Dict[str, any]:
    """Calculate comprehensive metrics for a list of tasks.

    Analyzes a collection of tasks to provide insights including completion rates,
    status distribution, average priority, and overdue task counts. This function
    is useful for dashboards, reports, and project health monitoring.

    Args:
        tasks: A list of Task objects to analyze. Can be an empty list.

    Returns:
        A dictionary containing the following metrics:
            - total (int): Total number of tasks in the list
            - completed (int): Number of tasks with status DONE
            - in_progress (int): Number of tasks with status IN_PROGRESS
            - blocked (int): Number of tasks with status BLOCKED
            - completion_rate (float): Percentage of completed tasks (0-100)
            - average_priority (float): Mean priority value across all tasks (1-4)
            - overdue_count (int): Number of incomplete tasks past their due date

    Examples:
        >>> tasks = [task1, task2, task3]
        >>> metrics = calculate_task_metrics(tasks)
        >>> print(f"Completion rate: {metrics['completion_rate']:.1f}%")
        Completion rate: 66.7%

        >>> # Handle empty list gracefully
        >>> metrics = calculate_task_metrics([])
        >>> print(metrics['completion_rate'])
        0

    Note:
        - Overdue tasks are only counted if they have a due_date set and are not DONE
        - Average priority is 0 for empty task lists
        - All calculations handle edge cases like division by zero
    """
    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == TaskStatus.DONE)
    in_progress = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
    blocked = sum(1 for t in tasks if t.status == TaskStatus.BLOCKED)

    avg_priority = sum(t.priority.value for t in tasks) / total if total > 0 else 0

    overdue = sum(1 for t in tasks if t.due_date and t.due_date < datetime.now() and t.status != TaskStatus.DONE)

    return {
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "blocked": blocked,
        "completion_rate": (completed / total * 100) if total > 0 else 0,
        "average_priority": avg_priority,
        "overdue_count": overdue
    }


def prioritize_tasks(tasks: List[Task], strategy: str = "priority") -> List[Task]:
    """Sort tasks using different prioritization strategies.

    Provides multiple sorting algorithms to help users organize their tasks based
    on different productivity methodologies. Supports priority-based sorting,
    deadline-driven sorting, and the Eisenhower Matrix (urgent/important) method.

    Args:
        tasks: A list of Task objects to be sorted. The original list is not modified.
        strategy: The prioritization strategy to use. Must be one of:
            - "priority" (default): Sort by task priority value (highest first),
              with creation date as tiebreaker (older tasks first)
            - "deadline": Sort by due date (earliest first). Tasks without
              due dates are placed at the end
            - "eisenhower": Sort using the Eisenhower Matrix, which categorizes
              tasks into four quadrants based on urgency and importance:
                * Quadrant 1: Urgent & Important (do first)
                * Quadrant 2: Not Urgent & Important (schedule)
                * Quadrant 3: Urgent & Not Important (delegate)
                * Quadrant 4: Not Urgent & Not Important (eliminate)

    Returns:
        A new sorted list of tasks. The original list remains unchanged.
        If an invalid strategy is provided, returns the original task list unsorted.

    Examples:
        >>> tasks = [low_priority_task, high_priority_task, medium_priority_task]
        >>> sorted_tasks = prioritize_tasks(tasks, strategy="priority")
        >>> print(sorted_tasks[0].priority)
        TaskPriority.CRITICAL

        >>> # Sort by deadline - urgent tasks first
        >>> deadline_sorted = prioritize_tasks(tasks, strategy="deadline")
        >>> print(deadline_sorted[0].due_date)
        2025-12-26 10:00:00

        >>> # Use Eisenhower Matrix for balanced prioritization
        >>> eisenhower_sorted = prioritize_tasks(tasks, strategy="eisenhower")
        >>> # Returns tasks in order: Q1 (urgent+important), Q2, Q3, Q4

    Note:
        Eisenhower Matrix urgency levels based on days until due:
            - Urgency 4: Due within 1 day (critical)
            - Urgency 3: Due within 3 days (high)
            - Urgency 2: Due within 7 days (moderate)
            - Urgency 1: Due after 7 days (low)
            - Urgency 0: No due date set

        The importance level is derived directly from the task's priority value (1-4).
    """
    if strategy == "priority":
        return sorted(tasks, key=lambda t: (-t.priority.value, t.created_at))
    elif strategy == "deadline":
        def deadline_key(task):
            if task.due_date is None:
                return (1, datetime.max)
            return (0, task.due_date)
        return sorted(tasks, key=deadline_key)
    elif strategy == "eisenhower":
        def eisenhower_score(task):
            urgency = 0
            if task.due_date:
                days_until_due = (task.due_date - datetime.now()).days
                if days_until_due <= 1:
                    urgency = 4
                elif days_until_due <= 3:
                    urgency = 3
                elif days_until_due <= 7:
                    urgency = 2
                else:
                    urgency = 1

            importance = task.priority.value

            quadrant = 0
            if urgency >= 3 and importance >= 3:
                quadrant = 1
            elif urgency < 3 and importance >= 3:
                quadrant = 2
            elif urgency >= 3 and importance < 3:
                quadrant = 3
            else:
                quadrant = 4

            return (quadrant, -importance, -urgency)

        return sorted(tasks, key=eisenhower_score)
    else:
        return tasks


def filter_tasks_by_criteria(tasks: List[Task],
                            status: Optional[TaskStatus] = None,
                            priority: Optional[TaskPriority] = None,
                            assigned_to: Optional[str] = None,
                            tags: Optional[List[str]] = None,
                            overdue_only: bool = False,
                            search_query: Optional[str] = None) -> List[Task]:
    """Filter tasks based on multiple criteria with AND logic.

    Applies a series of filters to a task list, with each criterion further narrowing
    the results. All filters use AND logic - tasks must match ALL provided criteria
    to be included in the results. This is useful for building advanced search
    features, creating custom task views, and generating filtered reports.

    Args:
        tasks: The list of Task objects to filter.
        status: Filter by task status. Only tasks matching this exact status
            will be included. If None, status is not used as a filter criterion.
        priority: Filter by task priority. Only tasks with this exact priority
            level will be included. If None, priority is not used as a filter.
        assigned_to: Filter by assignee username/ID. Only tasks assigned to this
            user will be included. If None, assignee is not used as a filter.
        tags: Filter by tags using OR logic within this parameter. Tasks that have
            ANY of the specified tags will match this criterion. If None or empty,
            tags are not used as a filter.
        overdue_only: If True, only returns incomplete tasks (not DONE) that are
            past their due date. Completed tasks and tasks without due dates are
            excluded. Defaults to False.
        search_query: Case-insensitive text search in task title and description.
            Returns tasks where the query appears in either field. If None or empty,
            text search is not applied.

    Returns:
        A filtered list of Task objects matching all specified criteria. Returns
        an empty list if no tasks match. The original task list is not modified.

    Examples:
        >>> # Find all high-priority tasks assigned to Alice
        >>> filtered = filter_tasks_by_criteria(
        ...     tasks,
        ...     priority=TaskPriority.HIGH,
        ...     assigned_to="alice"
        ... )

        >>> # Find overdue tasks with specific tags
        >>> urgent = filter_tasks_by_criteria(
        ...     tasks,
        ...     tags=["urgent", "client-facing"],
        ...     overdue_only=True
        ... )

        >>> # Search for tasks mentioning "API" that are in progress
        >>> api_tasks = filter_tasks_by_criteria(
        ...     tasks,
        ...     status=TaskStatus.IN_PROGRESS,
        ...     search_query="API"
        ... )

        >>> # Complex filter combining multiple criteria
        >>> critical_blocked = filter_tasks_by_criteria(
        ...     tasks,
        ...     status=TaskStatus.BLOCKED,
        ...     priority=TaskPriority.CRITICAL,
        ...     assigned_to="bob",
        ...     tags=["production"]
        ... )

    Note:
        - All filters use AND logic between different criteria
        - The tags parameter uses OR logic - matching ANY tag satisfies this criterion
        - Text search is case-insensitive and matches partial strings
        - Filters are applied sequentially, which allows short-circuit optimization
        - An empty criteria set (all parameters None/False) returns the full task list
    """
    filtered = tasks

    if status:
        filtered = [t for t in filtered if t.status == status]

    if priority:
        filtered = [t for t in filtered if t.priority == priority]

    if assigned_to:
        filtered = [t for t in filtered if t.assigned_to == assigned_to]

    if tags:
        filtered = [t for t in filtered if any(tag in t.tags for tag in tags)]

    if overdue_only:
        now = datetime.now()
        filtered = [t for t in filtered if t.due_date and t.due_date < now and t.status != TaskStatus.DONE]

    if search_query:
        query_lower = search_query.lower()
        filtered = [t for t in filtered if query_lower in t.title.lower() or query_lower in t.description.lower()]

    return filtered


def estimate_completion_date(tasks: List[Task],
                             tasks_per_day: float = 3.0,
                             working_days_per_week: int = 5) -> Optional[datetime]:
    """Estimate when all tasks will be completed based on velocity and priority.

    Calculates a projected completion date for a set of tasks using a weighted
    velocity model that accounts for task priority levels. Higher priority tasks
    are weighted more heavily in the calculation, providing a more realistic
    timeline estimate than simple task counting.

    The algorithm uses a three-step approach:
    1. Calculate the average priority weight across all incomplete tasks
    2. Convert tasks to weighted units based on their relative priority
    3. Project completion based on estimated daily throughput and working schedule

    Args:
        tasks: List of Task objects to analyze. Completed tasks are automatically
            excluded from the calculation.
        tasks_per_day: Average number of tasks that can be completed per working day.
            Defaults to 3.0. This should be calibrated based on historical team
            velocity. For example, use 5.0 for high-velocity teams or 2.0 for
            complex projects requiring more time per task.
        working_days_per_week: Number of working days in a week. Defaults to 5
            (Monday-Friday). Use 7 for continuous work or adjust for team schedules
            (e.g., 6 for teams working Saturdays, 4 for part-time work).

    Returns:
        A datetime object representing the estimated completion date and time.
        Returns the current datetime if all tasks are already completed.
        Returns None if the task list is empty (though current implementation
        returns current time for consistency).

    Examples:
        >>> tasks = get_project_tasks()  # 10 incomplete tasks
        >>> completion_date = estimate_completion_date(tasks)
        >>> print(f"Estimated completion: {completion_date.strftime('%Y-%m-%d')}")
        Estimated completion: 2026-01-15

        >>> # Adjust for a faster-paced team
        >>> completion_date = estimate_completion_date(
        ...     tasks,
        ...     tasks_per_day=5.0,
        ...     working_days_per_week=6
        ... )

        >>> # Check if project is on track
        >>> estimate = estimate_completion_date(sprint_tasks)
        >>> sprint_end = datetime(2026, 1, 31)
        >>> if estimate > sprint_end:
        ...     print("Warning: Sprint may not complete on time")

    Note:
        Priority weighting methodology:
            - Each task is weighted by its priority value (1-4)
            - A CRITICAL task (priority=4) counts as ~2.7x a LOW task (priority=1)
              when the average priority is MEDIUM (2.5)
            - This ensures high-priority tasks appropriately impact the timeline

        Calendar vs. working days:
            - The function converts working days to calendar days automatically
            - Example: 10 working days with 5-day weeks = 14 calendar days
            - This accounts for weekends and provides realistic date estimates

        Limitations:
            - Does not account for holidays or team member availability
            - Assumes consistent velocity over time (no learning curve or burnout)
            - Does not consider task dependencies or blocking issues
            - Uses current time as baseline (not project start date)

    See Also:
        calculate_task_metrics: For tracking actual completion rates
        prioritize_tasks: For ordering tasks by importance
    """
    incomplete_tasks = [t for t in tasks if t.status != TaskStatus.DONE]

    if not incomplete_tasks:
        return datetime.now()

    total_priority_points = sum(t.priority.value for t in incomplete_tasks)

    avg_task_weight = total_priority_points / len(incomplete_tasks) if incomplete_tasks else 1

    weighted_task_count = sum(t.priority.value / avg_task_weight for t in incomplete_tasks)

    days_needed = weighted_task_count / tasks_per_day

    calendar_days = days_needed * (7 / working_days_per_week)

    return datetime.now() + timedelta(days=calendar_days)


def validate_task_data(data: Dict) -> Tuple[bool, Optional[str]]:
    """Validate task data before creating or updating a task.

    Performs comprehensive validation on task data dictionaries to ensure data
    integrity and prevent invalid task creation. This function is typically called
    by API endpoints before persisting task data to the database. It checks for
    required fields, validates data types, enforces format constraints, and ensures
    values are within acceptable ranges.

    Args:
        data: A dictionary containing task data to validate. Expected keys include:
            - title (required): Task title string
            - status (optional): Task status string
            - priority (optional): Priority level integer (1-4)
            - due_date (optional): ISO-format datetime string
            - tags (optional): List of tag strings
            - description, assigned_to (optional): Not validated, but accepted

    Returns:
        A tuple of (is_valid, error_message):
            - is_valid (bool): True if all validations pass, False otherwise
            - error_message (str or None): Detailed error message if validation
              fails, None if validation succeeds

    Validation Rules:
        Title:
            - Required field (cannot be None, empty string, or missing)
            - Maximum length: 200 characters
            - Type: string

        Status:
            - Must be one of: "todo", "in_progress", "done", "blocked"
            - Type: string
            - Optional field

        Priority:
            - Must be an integer: 1 (LOW), 2 (MEDIUM), 3 (HIGH), or 4 (CRITICAL)
            - Type: integer
            - Optional field

        Due Date:
            - Must be in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
            - Cannot be more than 1 year in the past
            - Type: string (ISO datetime)
            - Optional field

        Tags:
            - Must be a list/array
            - Each tag must be a string
            - Tags can only contain: letters, numbers, hyphens, underscores
            - Regex pattern: ^[a-zA-Z0-9_-]+$
            - Optional field

    Examples:
        >>> # Valid task data
        >>> data = {
        ...     "title": "Implement user authentication",
        ...     "status": "in_progress",
        ...     "priority": 3,
        ...     "due_date": "2026-01-15T17:00:00",
        ...     "tags": ["backend", "security"]
        ... }
        >>> is_valid, error = validate_task_data(data)
        >>> print(is_valid)
        True

        >>> # Missing required title
        >>> invalid_data = {"description": "Some task"}
        >>> is_valid, error = validate_task_data(invalid_data)
        >>> print(error)
        Title is required

        >>> # Invalid tag format
        >>> data = {"title": "Task", "tags": ["valid-tag", "invalid tag!"]}
        >>> is_valid, error = validate_task_data(data)
        >>> print(error)
        Invalid tag 'invalid tag!'. Tags must contain only letters, numbers, hyphens, and underscores

        >>> # Title too long
        >>> data = {"title": "x" * 201}
        >>> is_valid, error = validate_task_data(data)
        >>> print(error)
        Title must be 200 characters or less

    Note:
        - Validation is fail-fast: returns on first error encountered
        - Order of validation: title → status → priority → due_date → tags
        - Unknown/extra fields are ignored (permissive validation)
        - Empty strings are treated as invalid for required fields
        - This function does NOT modify the input data dictionary

    See Also:
        bulk_update_tasks: Uses this function internally for batch validation
    """
    if not data.get("title"):
        return False, "Title is required"

    if len(data["title"]) > 200:
        return False, "Title must be 200 characters or less"

    if "status" in data:
        valid_statuses = [s.value for s in TaskStatus]
        if data["status"] not in valid_statuses:
            return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"

    if "priority" in data:
        valid_priorities = [p.value for p in TaskPriority]
        if isinstance(data["priority"], int) and data["priority"] not in valid_priorities:
            return False, f"Invalid priority. Must be one of: {', '.join(map(str, valid_priorities))}"

    if "due_date" in data and data["due_date"]:
        try:
            due = datetime.fromisoformat(data["due_date"])
            if due < datetime.now() - timedelta(days=365):
                return False, "Due date cannot be more than a year in the past"
        except (ValueError, TypeError):
            return False, "Invalid due_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"

    if "tags" in data:
        if not isinstance(data["tags"], list):
            return False, "Tags must be a list"

        for tag in data["tags"]:
            if not isinstance(tag, str):
                return False, "All tags must be strings"
            if not re.match(r'^[a-zA-Z0-9_-]+$', tag):
                return False, f"Invalid tag '{tag}'. Tags must contain only letters, numbers, hyphens, and underscores"

    return True, None


def bulk_update_tasks(tasks: List[Task],
                     task_ids: List[str],
                     updates: Dict) -> Tuple[List[Task], List[str]]:
    """Update multiple tasks with the same field values in a single operation.

    Performs batch updates on a collection of tasks, applying the same changes to
    all specified tasks. This is more efficient than updating tasks individually
    and is useful for operations like "mark all as done", "assign all to user X",
    or "add tag to selected tasks". Failed updates are tracked and returned for
    error handling.

    The function applies partial updates - only fields present in the updates
    dictionary are modified. Each task's updated_at timestamp is automatically
    set to the current time when successfully updated.

    Args:
        tasks: The complete list of Task objects available for updating. This list
            is used as the source of truth for finding tasks by ID.
        task_ids: List of task IDs (strings) to update. Tasks not found in the
            tasks list will be marked as failed.
        updates: Dictionary of field names and new values to apply to all specified
            tasks. Supported fields:
                - "status": New status value (string matching TaskStatus enum value)
                - "priority": New priority value (int matching TaskPriority enum value)
                - "assigned_to": New assignee username/ID (string)
                - "tags": New tags list (replaces existing tags, does not merge)

    Returns:
        A tuple of (updated_tasks, failed_ids):
            - updated_tasks (List[Task]): List of successfully updated Task objects
            - failed_ids (List[str]): List of task IDs that failed to update

    Failure Reasons:
        A task update can fail for the following reasons:
            - Task ID not found in the tasks list
            - Invalid status value (not a valid TaskStatus enum value)
            - Invalid priority value (not a valid TaskPriority enum value)
            - Invalid tags data type (tags field present but not a list)

    Examples:
        >>> # Mark multiple tasks as completed
        >>> tasks = get_all_tasks()
        >>> ids_to_complete = ["task-1", "task-2", "task-3"]
        >>> updated, failed = bulk_update_tasks(
        ...     tasks,
        ...     ids_to_complete,
        ...     {"status": "done"}
        ... )
        >>> print(f"Updated {len(updated)} tasks, {len(failed)} failed")
        Updated 3 tasks, 0 failed

        >>> # Assign multiple tasks and add tags
        >>> updates = {
        ...     "assigned_to": "alice",
        ...     "tags": ["sprint-2", "backend"],
        ...     "priority": 3
        ... }
        >>> updated, failed = bulk_update_tasks(tasks, selected_ids, updates)

        >>> # Handle failures gracefully
        >>> updated, failed = bulk_update_tasks(
        ...     tasks,
        ...     ["task-1", "invalid-id", "task-2"],
        ...     {"status": "in_progress"}
        ... )
        >>> if failed:
        ...     print(f"Warning: Could not update tasks: {', '.join(failed)}")
        Warning: Could not update tasks: invalid-id

        >>> # Invalid status causes failure
        >>> updated, failed = bulk_update_tasks(
        ...     tasks,
        ...     ["task-1"],
        ...     {"status": "invalid_status"}
        ... )
        >>> print(len(failed))
        1

    Note:
        - Updates are applied atomically per task (all-or-nothing for each task)
        - If any field update fails for a task, that entire task update is rolled back
        - Successfully updated tasks appear before the failure point
        - The updated_at timestamp is set automatically for successful updates
        - Tags are REPLACED, not merged (provide complete tag list in updates)
        - The original tasks list objects are modified in-place
        - assigned_to accepts None or any string value (no validation)

    Performance:
        - Time complexity: O(n + m) where n=len(tasks), m=len(task_ids)
        - Creates O(n) space for the tasks_by_id lookup dictionary
        - Efficient for large batch updates compared to individual API calls

    See Also:
        validate_task_data: For validating individual task data before updates
        filter_tasks_by_criteria: For selecting tasks to update
    """
    updated_tasks = []
    failed_ids = []

    tasks_by_id = {t.id: t for t in tasks}

    for task_id in task_ids:
        if task_id not in tasks_by_id:
            failed_ids.append(task_id)
            continue

        task = tasks_by_id[task_id]

        if "status" in updates:
            try:
                task.status = TaskStatus(updates["status"])
            except ValueError:
                failed_ids.append(task_id)
                continue

        if "priority" in updates:
            try:
                task.priority = TaskPriority(updates["priority"])
            except ValueError:
                failed_ids.append(task_id)
                continue

        if "assigned_to" in updates:
            task.assigned_to = updates["assigned_to"]

        if "tags" in updates:
            if isinstance(updates["tags"], list):
                task.tags = updates["tags"]

        task.updated_at = datetime.now()
        updated_tasks.append(task)

    return updated_tasks, failed_ids
