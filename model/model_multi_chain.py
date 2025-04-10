import re
import time
import json
import os
import pandas as pd
from datetime import datetime
from dateutil import relativedelta
from dotenv import load_dotenv
# from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
# from langchain_groq import ChatGroq

from evaluate import evaluation_sample_HSR

load_dotenv()
OLLAMA_SERVER = os.getenv('OLLAMA_SERVER')

llm = OllamaLLM(model='qwen2.5:14b', temperature=0)
# llm = OllamaLLM(
#     base_url=OLLAMA_SERVER,
#     model="qwen2.5:14b",             
#     temperature=0
# )

with open('prompts/multi_chain/extract_entity_and_number.txt', 'r') as fl:
    template_entity_and_number = fl.read()
with open('prompts/multi_chain/extract_employment_and_role.txt', 'r') as fl:
    template_employment_and_role = fl.read()
with open('prompts/multi_chain/extract_exclude.txt', 'r') as fl:
    template_exclude = fl.read()


prompt_entity_and_number = PromptTemplate(input_variables=['user_input'], template=template_entity_and_number)
chain_1 = prompt_entity_and_number | llm

prompt_employment_and_role = PromptTemplate(input_variables=['user_input'], template=template_employment_and_role)
chain_2 = prompt_employment_and_role | llm

prompt_exclude = PromptTemplate(input_variables=['user_input'], template=template_exclude)
chain_3 = prompt_exclude | llm

# df = pd.read_csv('dataset/test_data_HRS_exclude_range_2.csv')
df = pd.read_csv('dataset/HRS_data.csv')
print(df.columns)
# df = df[df['No'] == 68]
print('Test length: ', df.shape[0])

time_arr = []
true_count = 0
err_key = []
for idx, row in df.iterrows():
    user_input = re.sub(r'[\s\u3000]+', '', row['prompt'])
    stime = time.time()

    
    response_1 = chain_1.invoke({
        'user_input': user_input,
    })
    response_2 = chain_2.invoke({
        'user_input': user_input,
    })
    response_3 = chain_3.invoke({
        'user_input': user_input,
    })
    single_timer = time.time() - stime
    time_arr.append(single_timer)
    print('{} - {} - {}'.format(len(time_arr), row['No'], single_timer))
    
    # print("data: ", row)
    # for col, value in row.items():
    #     print(f"{col}: {value} (type: {type(value)})")
    try:
        entity_data = json.loads(response_1)
    except Exception as ex:
        print('JSON is invalid _ error: ', ex)
        continue
    try:
        role_data = json.loads(response_2)
    except Exception as ex:
        print('JSON is invalid _ error: ', ex)
        continue
    try:
        exclude_data = json.loads(response_3)
    except Exception as ex:
        print('JSON is invalid _ error: ', ex)
        continue
    
    response = {
        "affiliations": role_data.get("affiliations", ""),
        "department": role_data.get("department", ""),
        "occupation": role_data.get("occupation", ""),
        "employment_type": role_data.get("employment_type", ""),
        "lastname": entity_data.get("lastname", ""),
        "firstname": entity_data.get("firstname", ""),
        "employee_number": entity_data.get("employee_number", ""),
        "employee_number_range": entity_data.get("employee_number_range", ""),
        "status": role_data.get("status", ""),
        "exclude": exclude_data.get("exclude", "")
    }
    print('Respone: ', response) 

    eval_res = evaluation_sample_HSR(response, row, row['prompt'])
    true_count += eval_res[0]
    err_key.append(eval_res[1])
    print('\n')
print('All inference time: ', sum(time_arr))
print('Avg inference time: ', sum(time_arr)/len(time_arr))
print('Accuracy: ', true_count, true_count/df.shape[0])
print('Err keys: ', pd.Series(err_key).value_counts())
