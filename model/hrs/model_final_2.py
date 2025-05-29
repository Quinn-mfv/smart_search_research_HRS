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

from evaluation.evaluate_hrs import evaluation_sample_HSR

load_dotenv()
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')

llm = AzureChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2025-03-01-preview",
)

with open('prompts/hrs/prompt.txt', 'r') as fl:
    template = fl.read()

print('Template: ', template)

# Create the prompt using LangChain's PromptTemplate
prompt = PromptTemplate(input_variables=['user_input'], template=template)
chain = prompt | llm


# df = pd.read_csv('dataset/hrs/HRS_data_update_2.csv')
df = pd.read_csv('dataset/hrs/Ordered_Prompts_update_2.csv')
print(df.columns)
print('Test length: ', df.shape[0])


time_arr = []
true_count = 0
err_key = []
for idx, row in df.iterrows():
    user_input = row['prompt']
    stime = time.time()
    
    response = chain.invoke({
        'user_input': user_input,
        'affiliations_list': row['affiliations_list'],
        'departments_list': row['departments_list'],
        'occupations_list': row['occupations_list'],
    })
    single_timer = time.time() - stime
    time_arr.append(single_timer)
    print('{} - {} - {}'.format(len(time_arr), row['No'], single_timer))
    
    response = response.content
    print('Respone: ', response) 

    try: 
        json_res = json.loads(response)
    except Exception as ex:
        print('JSON is invalid _ error: ', ex)
        continue
    eval_res = evaluation_sample_HSR(json_res, row, user_input)
    true_count += eval_res[0]
    err_key.append(eval_res[1])
    print('\n')
print('All inference time: ', sum(time_arr))
print('Avg inference time: ', sum(time_arr)/len(time_arr))
print('Accuracy: ', true_count, true_count/df.shape[0])
print('Err keys: ', pd.Series(err_key).value_counts())
