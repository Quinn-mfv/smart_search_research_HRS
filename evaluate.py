import json
import pandas as pd
from datetime import datetime


# KEYS = ['payee_name', 'personal_in_charge', 'start_date', 'end_date', 'route', 'status']
KEYS_HRS = ['affiliations', 'department', 'occupation', 'employment_type', 'lastname', 'firstname', 'employee_number', 'status']

def format_gt_HSR(gt):
    if pd.isna(gt['affiliations']):
        gt['affiliations'] = ''
    else:
        tmp = json.loads(gt['affiliations'])
        tmp = str(sorted(tmp))
        gt['affiliations'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['department']):
        gt['department'] = ''
    else:
        tmp = json.loads(gt['department'])
        tmp = str(sorted(tmp))
        gt['department'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['occupation']):
        gt['occupation'] = ''
    else:
        tmp = json.loads(gt['occupation'])
        tmp = str(sorted(tmp))
        gt['occupation'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['employment_type']):
        gt['employment_type'] = ''
    else:
        tmp = json.loads(gt['employment_type'])
        tmp = str(sorted(tmp))
        gt['employment_type'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['lastname']):
        gt['lastname'] = ''
    else:
        tmp = json.loads(gt['lastname'])
        tmp = str(sorted(tmp))
        gt['lastname'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['firstname']):
        gt['firstname'] = ''
    else:
        tmp = json.loads(gt['firstname'])
        tmp = str(sorted(tmp))
        gt['firstname'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['employee_number']):
        gt['employee_number'] = ''
    else:
        tmp = json.loads(gt['employee_number'])
        tmp = str(sorted(tmp))
        gt['employee_number'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['status']):
        gt['status'] = ''
    else:
        print("DEBUG status:", gt['status'])
        tmp = json.loads(gt['status'])
        tmp = str(sorted(tmp))
        gt['status'] = tmp.replace('"', '').replace("'", '')
    return gt[['affiliations', 'department', 'occupation', 'employment_type', 'lastname', 'firstname', 'employee_number', 'status']].to_dict()


def format_pred_HSR(pred):
    if 'affiliations' in pred and pred['affiliations']:
        if isinstance(pred['affiliations'], list):
            pred['affiliations'] = str(sorted(pred['affiliations'])).replace('"', '').replace("'", '')
        else:
            affiliations = list(map(lambda x: x.strip(), pred['affiliations'].split(',')))
            if len(affiliations) > 1:
                pred['affiliations'] = str(sorted(affiliations)).replace('"', '').replace("'", '')
            else:
                pred['affiliations'] = str(affiliations).replace('"', '').replace("'", '')
    else:
        pred['affiliations'] = ''
    if 'department' in pred and pred['department']:
        if isinstance(pred['department'], list):
            pred['department'] = str(sorted(pred['department'])).replace('"', '').replace("'", '')
        else:
            departments = list(map(lambda x: x.strip(), pred['department'].split(',')))
            if len(departments) > 1:
                pred['department'] = str(sorted(departments)).replace('"', '').replace("'", '')
            else:
                pred['department'] = str(departments).replace('"', '').replace("'", '')
    else:
        pred['department'] = ''

    if 'occupation' in pred and pred['occupation']:
        if isinstance(pred['occupation'], list):
            pred['occupation'] = str(sorted(pred['occupation'])).replace('"', '').replace("'", '')
        else:
            occupations = list(map(lambda x: x.strip(), pred['occupation'].split(',')))
            if len(occupations) > 1:
                pred['occupation'] = str(sorted(occupations)).replace('"', '').replace("'", '')
            else:
                pred['occupation'] = str(occupations).replace('"', '').replace("'", '')
    else:
        pred['occupation'] = ''
    if 'employment_type' in pred and pred['employment_type']:
        if isinstance(pred['employment_type'], list):
            pred['employment_type'] = str(sorted(pred['employment_type'])).replace('"', '').replace("'", '')
        else:
            employment_types = list(map(lambda x: x.strip(), pred['employment_type'].split(',')))
            if len(employment_types) > 1:
                pred['employment_type'] = str(sorted(employment_types)).replace('"', '').replace("'", '')
            else:
                pred['employment_type'] = str(employment_types).replace('"', '').replace("'", '')
    else:
        pred['employment_type'] = ''
    if 'lastname' in pred and pred['lastname']:
        if isinstance(pred['lastname'], list):
            pred['lastname'] = str(sorted(pred['lastname'])).replace('"', '').replace("'", '')
        else:
            lastnames = list(map(lambda x: x.strip(), pred['lastname'].split(',')))
            if len(lastnames) > 1:          
                pred['lastname'] = str(sorted(lastnames)).replace('"', '').replace("'", '')
            else:
                pred['lastname'] = str(lastnames).replace('"', '').replace("'", '')
    else:
        pred['lastname'] = ''
    if 'firstname' in pred and pred['firstname']:    
        if isinstance(pred['firstname'], list):
            pred['firstname'] = str(sorted(pred['firstname'])).replace('"', '').replace("'", '')
        else:
            firstnames = list(map(lambda x: x.strip(), pred['firstname'].split(',')))
            if len(firstnames) > 1:
                pred['firstname'] = str(sorted(firstnames)).replace('"', '').replace("'", '')
            else:
                pred['firstname'] = str(firstnames).replace('"', '').replace("'", '')
    else:
        pred['firstname'] = ''
    if 'employee_number' in pred and pred['employee_number']:
        if isinstance(pred['employee_number'], list):
            pred['employee_number'] = str(sorted(pred['employee_number'])).replace('"', '').replace("'", '')
        else:
            employee_numbers = list(map(lambda x: x.strip(), pred['employee_number'].split(',')))
            if len(employee_numbers) > 1:
                pred['employee_number'] = str(sorted(employee_numbers)).replace('"', '').replace("'", '')
            else:
                pred['employee_number'] = str(employee_numbers).replace('"', '').replace("'", '')
    else:
        pred['employee_number'] = ''
    if 'status' in pred and pred['status']:   
        if isinstance(pred['status'], list):
            pred['status'] = str(sorted(pred['status'])).replace('"', '').replace("'", '')
        else:
            statuses = list(map(lambda x: x.strip(), pred['status'].split(',')))
            if len(statuses) > 1:
                pred['status'] = str(sorted(statuses)).replace('"', '').replace("'", '')
            else:
                pred['status'] = str(statuses).replace('"', '').replace("'", '')    
    else:
        pred['status'] = ''
    return pred

def recheck_end_date(pred):
    if pred['start_date'] and not pred['end_date']:
        if datetime.today() > datetime.strptime(pred['start_date'], '%Y-%m-%d'):
            pred['end_date'] = datetime.today().strftime('%Y-%m-%d')
    return pred



def evaluation_sample_HSR(pred, gt, prompt):
    gt = format_gt_HSR(gt)
    pred = format_pred_HSR(pred)
    for k in KEYS_HRS:
        if pred[k] != gt[k].replace('"', '').replace("'", ''):
            print(k)
            print('Prompt: ', prompt)
            print('Predict: ', pred)
            print('groundtruth: ', gt)
            print("False")
            return [False, k]
    print("True")
    return [True, '']