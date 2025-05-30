# POC for task Filter employee information using natural language

### Running API server locally:

1. Install dependencies: `pip install -r requirements.txt`


## Smart search for Payroll team
#### Dataset
- HRS_data_update_2.csv: HRS dataset with 8 fields (no excluding, ID number range case).
- Ordered_Prompts_update_2.csv: sythetic dataset with 8 fields (no excluding, ID number range case).

#### Prompt
- prompt_final_2_2.txt: prompt extracts 8 fields (no excluding, ID number range case).

#### Model
- model_final_2.py: model handle without ID number and excluding case (UPDATED).
- (model_final.py: model handle with excluding case.)

### Run code 
- Test SI model: `python -m model.hrs.model_final_2` 


## Smart search for SI team

### Dataset
- data_si.csv: SI data 
- data_synthetic_si.csv: synthetic/generation dataset 

### Model
Each model will check the field and data corresponding to the field in its name. For example:
- model_si_name_or_number.py: handle and evaluate name and id number field
- model_si_date.py: evhandle and evaluatealuate 4 date field.
- ...
- model_si.py: handle and evaluate all of fields.

### Prompt: 
- prompt_final.txt 

### Run code 
- Test SI model: `python -m model.si.model_si` 


## Smart search for TA team

### Dataset
- data_ta.csv: ta data 
- data_synthetic_ta.csv: synthetic/generation dataset 

### Model
Each model will check the field and data corresponding to the field in its name. For example:
- model_ta_name_or_number.py: handle and evaluate name and id number field
- model_ta_date.py: evhandle and evaluatealuate 4 date field.
- ...
- model_ta.py: handle and evaluate all of fields.

### Prompt: 
- prompt_ta.txt 

### Run code 
- Test ta model: `python -m model.ta.model_ta` 
