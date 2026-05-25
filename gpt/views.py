from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .services import ask_gpt


def gpt_page(request):
    """Страница с чатом GPT"""
    return render(request, 'gpt/gpt_page.html', {'title': 'Yandex GPT'})


@csrf_exempt
def gpt_ask(request):
    """Обработка AJAX-запроса к GPT"""
    if request.method == 'POST':
        question = request.POST.get('question', '')
        if question:
            answer = ask_gpt(question)
            return JsonResponse({'answer': answer})
    return JsonResponse({'error': 'Неверный запрос'}, status=400)