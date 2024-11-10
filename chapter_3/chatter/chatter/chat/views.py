from django.shortcuts import render
from django.http import JsonResponse
from chatbot import chatbot


def chat_query(request):
    user_message = request.POST['message']
    response = chatbot().get_response(user_message)
    response_data = response.text
    return JsonResponse({"message": response_data})


def main_view(request):
    context = {}
    return render(request, 'chat/main.html', context)