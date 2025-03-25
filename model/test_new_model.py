import re
import time
import json
import pandas as pd
from datetime import datetime
from dateutil import relativedelta
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
# from langchain_groq import ChatGroq

from evaluate import evaluation_sample_HSR

from utils import process_gt_date, parse_json_res_v1, postprocess_pred_date

load_dotenv()

# ENG_WEEKDAYS = { 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday' }
llm = OllamaLLM(model='qwen2.5:14b', temperature=0)
# llm = OllamaLLM(
#     base_url="", 
#     model="qwen2.5:14b",             
#     temperature=0
# )

with open('prompts/prompt_exclude_range.txt', 'r') as fl:
    template = fl.read()

print('Template: ', template)

# Create the prompt using LangChain's PromptTemplate
prompt = PromptTemplate(input_variables=['user_input'], template=template)

chain = prompt | llm
# today = datetime.today() # - relativedelta.relativedelta(days=7)

df = pd.read_csv('dataset/test_data_HRS_exclude_range.csv')
# df = df[df['No'] == 68]
print('Test length: ', df.shape[0])

time_arr = []
true_count = 0
err_key = []
for idx, row in df.iterrows():

    user_input = row['prompt'].replace(' ', '')
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

    print('Json res: ', json_res)
    eval_res = evaluation_sample_HSR(json_res, row, row['prompt'])
    true_count += eval_res[0]
    err_key.append(eval_res[1])
    print('\n')
print('All inference time: ', sum(time_arr))
print('Avg inference time: ', sum(time_arr)/len(time_arr))
print('Accuracy: ', true_count, true_count/df.shape[0])
print('Err keys: ', pd.Series(err_key).value_counts())
