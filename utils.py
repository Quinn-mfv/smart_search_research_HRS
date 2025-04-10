import re
import ast
import copy
import json
import calendar
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_community.llms import HuggingFacePipeline
# from langchain_huggingface.llms import HuggingFacePipeline



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
