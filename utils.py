import re
import ast
import copy
import json
import calendar
import pandas as pd
from word2number import w2n
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_community.llms import HuggingFacePipeline
# from langchain_huggingface.llms import HuggingFacePipeline


DATE_FORMAT = '%Y-%m-%d'
def format_response(response):
    if 'payee_name' in response and response['payee_name']:
        if isinstance(response['payee_name'], str):
            payees = response['payee_name'].split(',')
            if len(payees) > 1:
                response['payee_name'] = list(map(str.strip, payees))
            else:
                response['payee_name'] = payees
    else:
        response['payee_name'] = []
        
    if 'personal_in_charge' in response and response['personal_in_charge']:
        if isinstance(response['personal_in_charge'], str):
            pics = response['personal_in_charge'].split(',')
            if len(pics) > 1:
                response['personal_in_charge'] = list(map(str.strip, pics))
            else:
                response['personal_in_charge'] = pics
    else:
        response['personal_in_charge'] = []
    
    if 'route' in response and response['route']:
        if isinstance(response['route'], str):
            routes = response['route'].split(',')
            if len(routes) > 1:
                response['route'] = list(map(str.strip, routes))
            else:
                response['route'] = routes
    else:
        response['route'] = []
        
    if 'status' in response and response['status']:
        if isinstance(response['status'], str):
            statuses = response['status'].split(',')
            if len(statuses) > 1:
                response['status'] = list(map(str.strip, statuses))
            else:
                response['status'] = statuses
    else:
        response['status'] = []

    response = postprocess_pred_date(response)
    try:
        fstart_date = normalize_date(response['start_date']).strftime(DATE_FORMAT)
        response['start_date'] = fstart_date
    except ValueError as err:
        print(err)
        pass
    
    try:
        fend_date = normalize_date(response['end_date']).strftime(DATE_FORMAT)
        response['end_date'] = fend_date
    except ValueError as err:
        print(err)
        pass
    return response

def normalize_date(dt):
    for fmt in ('%Y年%m月%d日', '%Y年%m月', '%Y年', '%Y/%m/%d', '%Y/%m', '%Y', '%Y-%m-%d', '%Y-%m'):
        try:
            return datetime.strptime(dt, fmt)
        except ValueError:
            pass
    raise ValueError('No valid date format found')

def parse_json_res_v1(result):
    if 'json' in result:
        starts_pos = [i.start() + 8 for i in re.finditer('```json\n{', result)]
    else:
        starts_pos = [i.start() + 4 for i in re.finditer('```\n{', result)]
    ends_pos = [i.start() + 1 for i in re.finditer('}\n```', result)]
    if len(starts_pos) != len(ends_pos):
        print(result)
        assert len(starts_pos) == len(ends_pos)
    
    res = []
    for start_pos, end_pos in zip(starts_pos, ends_pos):
        res.append(json.loads(result[start_pos:end_pos]))
    return res

def load_llm_model():
    # model_name = 'EleutherAI/gpt-j-6B'
    # model_name = 'Qwen/Qwen2.5-7B-Instruct'
    # model_name = 'bigscience/bloomz-7b1'
    model_name = 'sbintuitions/sarashina2-7b'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    text_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=1024
    )
    llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})
    return llm

def process_variable_reldate(row, today=None, col_name=None):
    if not today:
        today = datetime.today()
    if isinstance(row, str) and 'ago' in row:
        x = int(re.findall(r'\d+', row)[0])
        if 'days' in row:
            dt = today - relativedelta(days=x)
            return dt.strftime(DATE_FORMAT)
        elif 'weeks' in row:
            dt = today - relativedelta(weeks=x)
            if col_name == 'sd':
                return (dt - timedelta(days=dt.weekday()) - timedelta(days=1)).strftime(DATE_FORMAT)
            else:
                return (dt - timedelta(days=dt.weekday()) + timedelta(days=5)).strftime(DATE_FORMAT)
        elif 'months' in row:
            dt = today - relativedelta(months=x)
            if col_name == 'sd':
                return dt.strftime(f'%Y-%m-01')
            else:
                return dt.strftime(f'%Y-%m-{calendar.monthrange(dt.year, dt.month)[1]}')
        elif 'years' in row:
            dt = today - relativedelta(years=x)
            if col_name == 'sd':
                return dt.strftime('%Y-01-01')
            else:
                return dt.strftime('%Y-12-31')
    else:
        return row
    
def reldate_dict(today=None):
    if not today:
        today = datetime.today()
    last_year = today - relativedelta(years=1)
    next_year = today + relativedelta(years=1)
    last_month = today - relativedelta(months=1)
    next_month = today + relativedelta(months=1)
    last_week = today - relativedelta(weeks=1)
    next_week = today + relativedelta(weeks=1)

    rel_date_dict = {
        'last year start': last_year.strftime('%Y-01-01'),
        'last year end': last_year.strftime('%Y-12-31'),
        'this year start': today.strftime('%Y-01-01'),
        'this year end': today.strftime('%Y-12-31'),
        'next year start': next_year.strftime('%Y-01-01'),
        'next year end': next_year.strftime('%Y-12-31'),
        
        'last month start': last_month.strftime('%Y-%m-01'),
        'last month end': last_month.strftime(f'%Y-%m-{calendar.monthrange(last_month.year, last_month.month)[1]}'),
        'this month start': today.strftime('%Y-%m-01'),
        'this month end': today.strftime(f'%Y-%m-{calendar.monthrange(today.year, today.month)[1]}'),
        'next month start': next_month.strftime('%Y-%m-01'),
        'next month end': next_month.strftime(f'%Y-%m-{calendar.monthrange(next_month.year, next_month.month)[1]}'),

        # A week start on Sunday and end on Saturday
        'last week start': (last_week - timedelta(days=last_week.weekday()) - timedelta(days=1)).strftime(DATE_FORMAT),
        'last week end': (last_week - timedelta(days=last_week.weekday()) + timedelta(days=5)).strftime(DATE_FORMAT),
        'this week start': (today - timedelta(days=today.weekday()) - timedelta(days=1)).strftime(DATE_FORMAT),
        'this week end': (today - timedelta(days=today.weekday()) + timedelta(days=5)).strftime(DATE_FORMAT),
        'next week start': (next_week - timedelta(days=next_week.weekday()) - timedelta(days=1)).strftime(DATE_FORMAT),
        'next week end': (next_week - timedelta(days=next_week.weekday()) + timedelta(days=5)).strftime(DATE_FORMAT),

        'today': today.strftime(DATE_FORMAT),
    }
    return rel_date_dict


def process_gt_date(test_df, today=None):
    rel_date_dict = reldate_dict(today)
    test_df['processed_start_date'] = test_df['start_date'].str.replace('"', '').str.replace('/', '-')
    test_df['processed_start_date'] = test_df['processed_start_date'].map(rel_date_dict).fillna(test_df['processed_start_date'])
    test_df['processed_start_date'] = test_df['processed_start_date'].apply(process_variable_reldate, args=(None, 'sd',))
    test_df['processed_start_date'] = pd.to_datetime(test_df['processed_start_date'], format=DATE_FORMAT)
    
    test_df['processed_end_date'] = test_df['end_date'].str.replace('"', '').str.replace('/', '-')
    test_df['processed_end_date'] = test_df['processed_end_date'].map(rel_date_dict).fillna(test_df['processed_end_date'])
    test_df['processed_end_date'] = test_df['processed_end_date'].apply(process_variable_reldate, args=(None, 'ed',))
    test_df['processed_end_date'] = pd.to_datetime(test_df['processed_end_date'], format=DATE_FORMAT)
    
    return test_df

def postprocess_pred_date(pred):
    reldate_string = [
        'last year', 'this year', 'next year',
        'last month', 'this month', 'next month',
        'last week', 'this week', 'next week'
    ]
    rel_date_dict = reldate_dict()
    format_pred = copy.deepcopy(pred)
    if format_pred['start_date'] in reldate_string:
        format_pred['start_date'] = rel_date_dict[format_pred['start_date'] + ' start']
    if format_pred['end_date'] in reldate_string:
        format_pred['end_date'] = rel_date_dict[format_pred['end_date'] + ' end']
    return format_pred

# transfer date from string (many different formats) to datetime
# input: 2024年12月10日 được extract từ prompt
# output: 2024-12-10
def process_date(dt):
    for fmt in ('%Y年%m月%d日', '%Y年%m月', '%Y年', '%Y/%m/%d', '%Y/%m', '%Y', '%Y-%m-%d', '%Y-%m'):
        try:
            return datetime.strptime(dt, fmt).strftime(DATE_FORMAT), 'single'
        except ValueError as ex:
            if len(ex.args) > 0 and ex.args[0].startswith('unconverted data remains'):
                aux = ex.args[0].split(':')[1].strip()
                date_part = dt.split(aux)[0].strip()
                date = datetime.strptime(date_part, fmt)
                if aux == '以前':
                    date = date - relativedelta(days=1)
                return date.strftime(DATE_FORMAT), 'before'
            else:
                continue
    return dt, ''

# thời gian tương đối --> thời gian cụ thể
# input: 10 days ago
# output: start_date, end_date
def process_relative_time(date_string):
    today = datetime.today()
    x = int(re.findall(r'\d+', date_string)[0])
    if 'days' in date_string:
        dt = today - relativedelta(days=x)
        return dt.strftime(DATE_FORMAT), dt.strftime(DATE_FORMAT)
    elif 'weeks' in date_string:
        dt = today - relativedelta(weeks=x)
        return (dt - relativedelta(days=dt.weekday()) - relativedelta(days=1)).strftime(DATE_FORMAT), (dt - relativedelta(days=dt.weekday()) + relativedelta(days=5)).strftime(DATE_FORMAT)
    elif 'months' in date_string:
        dt = today - relativedelta(months=x)
        return dt.strftime(f'%Y-%m-01'), dt.strftime(f'%Y-%m-{calendar.monthrange(dt.year, dt.month)[1]}')
    elif 'years' in date_string:
        dt = today - relativedelta(years=x)
        return dt.strftime('%Y-01-01'), dt.strftime('%Y-12-31')
    
def process_fix_relative_time(dt):
    reldate_string = [
        'last year', 'this year', 'next year',
        'last month', 'this month', 'next month',
        'last week', 'this week', 'next week'
    ]
    rel_date_dict = reldate_dict()

    if dt in reldate_string:
        return rel_date_dict[dt + ' start'], rel_date_dict[dt + ' end']
    return dt



# parse relative date string
# input: March
# output: 3
def parse_relative_dt(date_str):
    res = []
    for word in date_str.split(' '):
        try:
            res += [str(w2n.word_to_num(word))]
        except ValueError:
            res += [word]
    if ' '.join(res) == date_str:
        raise ValueError('Not found number in date string')
    else:
        return ' '.join(res)
    


# transfer date_response from string to tuple
# input: 2024年12月10日 được extract từ prompt
# output: ('2024-12-10', '2024-12-10')
def process_date_res(date_response):
    print("utils - data response: ", date_response)
    dates = date_response[date_response.index("["):date_response.index("]")+1]
    date_list = ast.literal_eval(dates)
    if not date_list:
        return tuple(['', ''])
    elif len(date_list) > 1:
        return tuple([process_date(date_list[0])[0], process_date(date_list[1])[0]])
    else:
        date_string = date_list[0]
        if bool(re.match('[a-zA-Z\s]+$', date_string)) or 'ago' in date_string:
            if bool(re.match('[a-zA-Z\s]+$', date_string)):
                try:
                    date_string = parse_relative_dt(date_string)  # three months ago --> 3 months ago
                    start_date, end_date = process_relative_time(date_string)
                except ValueError as err:
                    start_date, end_date = process_fix_relative_time(date_string) # last year --> 2021-01-01, 2021-12-31
            else:
                start_date, end_date = process_relative_time(date_string)
            return tuple([start_date, end_date])
        else:
            dt, aux = process_date(date_list[0])
            if aux == 'single':
                return tuple([dt, dt])
            elif aux == 'before':
                return tuple(['', dt])


