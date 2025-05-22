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
from constants.constants_hrs import affiliations, department, occupation, employment_type, status
# from langchain_groq import ChatGroq

from evaluation.evaluate_hrs import evaluation_sample_HSR

load_dotenv()
OLLAMA_SERVER = os.getenv('OLLAMA_SERVER')

llm = OllamaLLM(model='qwen2.5:14b', temperature=0)
# llm = OllamaLLM(
#     base_url=OLLAMA_SERVER,
#     model="qwen2.5:14b",             
#     temperature=0
# )

with open('prompts/prompt_input_updateExclude_range.txt', 'r') as fl:
    template = fl.read()

print('Template: ', template)

# Create the prompt using LangChain's PromptTemplate
prompt = PromptTemplate(input_variables=['user_input', 'affiliations', 'department', 'occupation', 'employment_type', 'status'], template=template)
chain = prompt | llm

# df = pd.read_csv('dataset/test_data_HRS_exclude_range_2.csv')
df = pd.read_csv('dataset/Ordered_Prompts.csv')
print(df.columns)
# df = df[df['No'] == 68]
print('Test length: ', df.shape[0])

time_arr = []
true_count = 0
err_key = []
for idx, row in df.iterrows():

    user_input = row['prompt'].replace(' ', '')
    stime = time.time()

    # formatted_prompt = prompt.format(
    #     user_input=user_input,
    #     affiliations=affiliations,
    #     department=department,
    #     occupation=occupation,
    #     employment_type=employment_type,
    #     status=status
    # )

    # print("Formatted Prompt:\n", formatted_prompt)
    
    response = chain.invoke({
        'user_input': user_input,
        'affiliations': affiliations, 
        'department': department,
        'occupation': occupation,
        'employment_type': employment_type,
        'status': status
    })
    single_timer = time.time() - stime
    time_arr.append(single_timer)
    print('{} - {} - {}'.format(len(time_arr), row['No'], single_timer))
    
    # print("data: ", row)
    # for col, value in row.items():
    #     print(f"{col}: {value} (type: {type(value)})")
    # print('Respone: ', response) 

    try: 
        json_res = json.loads(response)
    except Exception as ex:
        print('JSON is invalid _ error: ', ex)
        continue
    eval_res = evaluation_sample_HSR(json_res, row, row['prompt'])
    true_count += eval_res[0]
    err_key.append(eval_res[1])
    print('\n')
print('All inference time: ', sum(time_arr))
print('Avg inference time: ', sum(time_arr)/len(time_arr))
print('Accuracy: ', true_count, true_count/df.shape[0])
print('Err keys: ', pd.Series(err_key).value_counts())
