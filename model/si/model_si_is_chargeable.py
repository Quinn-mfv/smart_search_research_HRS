import re
import time
import json
import os
import pandas as pd
from datetime import datetime
from dateutil import relativedelta
from dotenv import load_dotenv
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama.llms import OllamaLLM
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate

from evaluation.evaluation_si import evaluate

ENG_WEEKDAYS = { 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday' }
today = datetime.now().strftime("%A, '%Y/%m/%d")
print('Today: ', today)

load_dotenv()
# OLLAMA_SERVER = os.getenv('OLLAMA_SERVER')
OLLAMA_SERVER = os.getenv('OLLAMA_SERVER')
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')

llm = AzureChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2025-03-01-preview",
)

# with open('prompts/si/old_prompt.txt', 'r') as fl:
with open('prompts/si/prompt_si_final.txt', 'r') as fl:
    template = fl.read()

print('Template: ', template)

# Create the prompt using LangChain's PromptTemplate
prompt = PromptTemplate(input_variables=['user_input'], template=template)
chain = prompt | llm

df = pd.read_csv('dataset/si/data_si_is_chargeable.csv')
# df = pd.read_csv('dataset/HRS_data_remove_exclude_range.csv')
print(df.columns)
print('Test length: ', df.shape[0])


time_arr = []
true_count = 0
err_key = []
for idx, row in df.iterrows():
    # user_input = re.sub(r'[\s\u3000]+', '', row['prompt'])  
    user_input = row['prompt']
    # user_input = " ".join([w.surface for w in tagger(row['prompt'])])
    stime = time.time()
    
    print('Prompt: ', user_input)
    # print('today: ', today.strftime('%Y-%m-%d'))
    # print('weekday: ', ENG_WEEKDAYS[today.weekday()])
    
    response = chain.invoke({
        'user_input': user_input,
        'today': today,
        'group': row['group']
    })
    response = response.content
    single_timer = time.time() - stime
    time_arr.append(single_timer)
    print('{} - {} - {}'.format(len(time_arr), row['No'], single_timer))
    
    print('Respone: ', response) 

    try: 
        json_res = json.loads(response)
    except Exception as ex:
        print('JSON is invalid _ error: ', ex)
        continue
    eval_res = evaluate(json_res, row, user_input)
    true_count += eval_res[0]
    err_key.append(eval_res[1])
    print('\n')
print('All inference time: ', sum(time_arr))
print('Avg inference time: ', sum(time_arr)/len(time_arr))
print('Accuracy: ', true_count, true_count/df.shape[0])
print('Err keys: ', pd.Series(err_key).value_counts())
