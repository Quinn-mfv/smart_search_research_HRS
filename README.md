# POC for task Filter employee information using natural language

### Running API server locally:

1. Install dependencies: `pip install -r requirements.txt`

2. Test model: `python -m model.model_final_2.py` 


#### Dataset
- HRS_data_update_2.csv: HRS dataset with 8 fields (no excluding, ID number range case).
- Ordered_Prompts_update_2.csv: sythetic dataset with 8 fields (no excluding, ID number range case).

#### Prompt:
- prompt_final_2_2.txt: prompt extracts 8 fields (no excluding, ID number range case).

#### Model
- model_final_2.py: model handle without ID number and excluding case (UPDATED).
- (model_final.py: model handle with excluding case.)


