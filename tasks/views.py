from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Topic, Task


def normalize_answer(answer):
    return answer.strip().lower().replace(",", ".")


def home(request):
    latest_tasks = Task.objects.select_related("topic").order_by("-id")[:6]

    topics = Topic.objects.annotate(
        total_tasks=Count("tasks"),
        base_tasks=Count("tasks", filter=Q(tasks__difficulty="easy")),
        profile_tasks=Count("tasks", filter=Q(tasks__difficulty__in=["hard"])),
    )[:6]

    return render(request, "tasks/home.html", {
        "latest_tasks": latest_tasks,
        "topics": topics,
    })


def task_list(request):
    selected_topic = request.GET.get("topic")
    selected_difficulty = request.GET.get("difficulty")
    search_query = request.GET.get("q", "").strip()

    tasks = Task.objects.select_related("topic").all()
    topics = Topic.objects.all()

    if selected_topic:
        tasks = tasks.filter(topic_id=selected_topic)

    if selected_difficulty:
        tasks = tasks.filter(difficulty=selected_difficulty)

    if search_query:
        search_query_lower = search_query.casefold()

        tasks = [
            task for task in tasks
            if search_query_lower in task.title.casefold()
            or search_query_lower in task.condition.casefold()
            or search_query_lower in task.explanation.casefold()
            or search_query_lower in task.topic.name.casefold()
        ]

    difficulty_choices = Task.DIFFICULTY_CHOICES
    tasks_count = len(tasks)

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "topics": topics,
        "selected_topic": selected_topic,
        "selected_difficulty": selected_difficulty,
        "search_query": search_query,
        "difficulty_choices": difficulty_choices,
        "tasks_count": tasks_count
    })


def task_detail(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related("topic"),
        id=task_id
    )

    result = None
    user_answer = ""

    if request.method == "POST":
        user_answer = request.POST.get("user_answer", "")
        correct_answer = task.answer.strip()

        if normalize_answer(user_answer) == normalize_answer(correct_answer):
            result = "correct"
        else:
            result = "wrong"

    return render(request, "tasks/task_detail.html", {
        "task": task,
        "result": result,
        "user_answer": user_answer,
    })


def topic_list(request):
    topics = Topic.objects.annotate(
        total_tasks=Count("tasks"),
        base_tasks=Count("tasks", filter=Q(tasks__difficulty="easy")),
        profile_tasks=Count("tasks", filter=Q(tasks__difficulty__in=["hard"])),
    )

    return render(request, "tasks/topic_list.html", {
        "topics": topics,
    })


def tasks_by_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    tasks = Task.objects.select_related("topic").filter(topic=topic)

    return render(request, "tasks/tasks_by_topic.html", {
        "topic": topic,
        "tasks": tasks,
    })