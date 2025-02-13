from django.shortcuts import render, redirect
from calculatorapp.models import History
import math
import re


PATTERNS_SUB = [
    (r'sqrt\(([\d.]+),([\d.]+)\)', 'sqrt'),
    (r'log\(([\d.]+)(?:,([\d.]+))?\)', 'log'),
    (r'sin\((\d+(?:\.\d+)?)\)', 'sin'),
    (r'cos\((\d+(?:\.\d+)?)\)', 'cos'),
    (r'tan\((\d+(?:\.\d+)?)\)', 'tan'),]


PATTERNS_REPLACE = [
    (' ', ''),
    ('^', '**'),
    ('mod', '%'),]


PATTERNS_SUB_REPAIR = [
    (r'math\.math\.log\(([^,]+),\s*([^)]+)\)', r'math.log(\1,\2)'),
    (r'math\.math\.log\(([^,]+)\)', r'math.log(\1)'),]


def calculation_history(request, cookie):
    if cookie:
        pk_cookie = [int(pk_history) for pk_history in cookie.split('_')]
        history = History.objects.filter(pk__in=pk_cookie).order_by('-id')
        return history


def replace_action(match, action):
    if action == 'sqrt':
        return replace_sqrt(match)              
    elif action == 'log':
        return replace_log(match)
    else:
        return replace_sin_cos_tan(match, action)


def replace_sqrt(match):
    value_x = float(match.group(1))
    value_y = float(match.group(2))
    return f"math.pow({value_x}, 1/{value_y})"


def replace_log(match):
    value_x = float(match.group(1))
    value_y = match.group(2)
    if value_y is None:
        return f"math.log({value_x})"
    else:
        value_y = float(match.group(2))
        return f"math.log({value_x},{value_y})"


def replace_sin_cos_tan(match, sin_cos_tan):
    value = float(match.group(1))
    return f"math.{sin_cos_tan}(math.radians({value}))"


def remove_history(request, pk):
    response = redirect('home')
    cookie = request.COOKIES.get('history') or None
    pk_cookie = [int(pk_history) for pk_history in cookie.split('_')]
    pk_cookie.remove(pk)
    History.objects.filter(pk=pk).delete()
    response.set_cookie(key='history', value="_".join(map(str, pk_cookie))) if pk_cookie else response.delete_cookie('history')
    return response


def home(request):
    cookie = request.COOKIES.get('history') or None
    history = calculation_history(request, cookie) or None
    input_to_replace = request.POST['inputField'] if 'inputField' in request.POST else None
    input_without_spaces = input_to_replace.replace(' ', '') if input_to_replace else None

    if input_to_replace:
        try:
            for before, after in PATTERNS_REPLACE:
                input_to_replace = input_to_replace.replace(before, after)

            for pattern, action in PATTERNS_SUB:
                input_to_replace = re.sub(pattern, lambda match: replace_action(match, action), input_to_replace)

            for pattern, action in PATTERNS_SUB_REPAIR:
                input_to_replace = re.sub(pattern, action, input_to_replace)

            output = eval(input_to_replace)
        except:
            output = 'Incorrect operation'
    else:
        output = None

    context = {'input': input_without_spaces, 'output': output, 'history': history}

    if request.method == 'POST' and output != 'Incorrect operation' and output is not None:
        obj = History.objects.create(result=f'{input_without_spaces} = {output}')
        history = history | History.objects.filter(pk=obj.pk) if history else History.objects.filter(pk=obj.pk)
        context['history'] = history
        response = render(request, 'home.html', context=context)
        response.set_cookie(key='history', value=f'{cookie}_{obj.pk}') if cookie else response.set_cookie(key='history', value=f'{obj.pk}')
    else:
        response = render(request, 'home.html', context=context)
    return response
