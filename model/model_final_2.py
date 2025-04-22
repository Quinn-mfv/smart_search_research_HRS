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

from evaluate import evaluation_sample_HSR

load_dotenv()
OLLAMA_SERVER = os.getenv('OLLAMA_SERVER')

llm = OllamaLLM(model='qwen2.5:14b', temperature=0)
# llm = OllamaLLM(
#     base_url=OLLAMA_SERVER,
#     model="qwen2.5:14b",             
#     temperature=0
# )

with open('prompts/prompt_final_2.txt', 'r') as fl:
    template = fl.read()

print('Template: ', template)

# Create the prompt using LangChain's PromptTemplate
prompt = PromptTemplate(input_variables=['user_input'], template=template)
chain = prompt | llm

# df = pd.read_csv('dataset/Ordered_Prompts_update_2.csv')
df = pd.read_csv('dataset/HRS_data_update_2.csv')
print(df.columns)
print('Test length: ', df.shape[0])


time_arr = []
true_count = 0
err_key = []
for idx, row in df.iterrows():
    user_input = re.sub(r'[\s\u3000]+', '', row['prompt'])  
    # user_input = " ".join([w.surface for w in tagger(row['prompt'])])
    stime = time.time()
    
    response = chain.invoke({
        'user_input': user_input,
    })
    single_timer = time.time() - stime
    time_arr.append(single_timer)
    print('{} - {} - {}'.format(len(time_arr), row['No'], single_timer))
    
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
