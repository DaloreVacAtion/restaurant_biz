import json
import re

from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout

from account.models import User

import logging

logger = logging.getLogger('views')


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'auth/authorization.html')

    def post(self, request):
        if len(request.POST):
            data = request.POST
        elif len(request.body):
            data = json.loads(request.body)
        else:
            raise Http404
        if 'code' in list(data):
            code = int(data['code'])
            if 'username' in list(data):
                username = data['username'].replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
                if re.match(r'(\+7)(\d{10})', username) or re.match(r'\d{10}', username):
                    user = User.objects.get(username=username)
                    if code == 12345:
                        auth.login(request, user)
                        url = ''
                        return JsonResponse({'success': True, 'url': url})
                    else:
                        return JsonResponse({'success': False, 'message': 'Простите, это всего-лишь ТЗ, поэтому, будьте '
                                                                          'добры, введите код, указанный в чекбоксе '
                                                                          '(12345)...'})
                else:
                    return JsonResponse({'success': False, 'message': 'Некорректный запрос. Обратитесь в '
                                                                      'тех.поддержку...'})
            else:
                return JsonResponse({'success': False, 'message': 'Некорректный запрос. Обратитесь в '
                                                                  'тех.поддержку...'})

        elif 'username' in list(data):
            username = data['username'].replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if re.match(r'(\+7)(\d{10})', username):
                user, _ = User.objects.get_or_create(username=username)
                return JsonResponse({'success': True, 'cool_time': 60})
            else:
                return JsonResponse({'success': False, 'message': 'Некорректный запрос. Обратитесь в '
                                                                  'тех.поддержку...'})
        return render(request, 'auth/authorization.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
