import json
import pandas as pd
from datetime import datetime


# KEYS = ['payee_name', 'personal_in_charge', 'start_date', 'end_date', 'route', 'status']
KEYS_HRS = ['affiliations', 'department', 'occupation', 'employment_type', 'lastname', 'firstname', 'employee_number', 'employee_number_range', 'status', 'exclude']

def format_gt_HRS(gt):
    if pd.isna(gt['affiliations']) or gt['affiliations'] == '':
        gt['affiliations'] = ''
    else:
        tmp = json.loads(gt['affiliations'])
        tmp = str(sorted(tmp))
        gt['affiliations'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['department']) or gt['department'] == '':
        gt['department'] = ''
    else:
        tmp = json.loads(gt['department'])
        tmp = str(sorted(tmp))
        gt['department'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['occupation']) or gt['occupation'] == '':
        gt['occupation'] = ''
    else:
        tmp = json.loads(gt['occupation'])
        tmp = str(sorted(tmp))
        gt['occupation'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['employment_type']) or gt['employment_type'] == '':
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
    if pd.isna(gt['firstname']) or gt['firstname'] == '':
        gt['firstname'] = ''
    else:
        tmp = json.loads(gt['firstname'])
        tmp = str(sorted(tmp))
        gt['firstname'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['employee_number']) or gt['employee_number'] == '':
        gt['employee_number'] = ''
    else:
        tmp = json.loads(gt['employee_number'])
        tmp = str(sorted(tmp))
        gt['employee_number'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['employee_number_range']) or gt['employee_number_range'] == '':
        gt['employee_number_range'] = ''
    else:
        tmp = json.loads(gt['employee_number_range'])
        # if -1 not in tmp: 
        #     tmp = str(sorted(tmp))
        gt['employee_number_range'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['status']) or gt['status'] == '':
        gt['status'] = ''
    else:
        # print(f"DEBUG status before parsing: {gt['status']}")
        tmp = json.loads(gt['status'])
        tmp = str(sorted(tmp))
        gt['status'] = tmp.replace('"', '').replace("'", '')
    if pd.isna(gt['exclude']) or gt['exclude'] == '':
        gt['exclude'] = ''  
    else:
        tmp = json.loads(gt['exclude'])
        tmp = str(sorted(tmp))
        gt['exclude'] = tmp.replace('"', '').replace("'", '')
    return gt[['affiliations', 'department', 'occupation', 'employment_type', 'lastname', 'firstname', 'employee_number', 'employee_number_range', 'status', 'exclude']].to_dict()


def format_label_HRS(gt):
    # fields = ['affiliations', 'department', 'occupation', 'employment_type', 'lastname', 'firstname', 'employee_number', 'employee_number_range', 'status']
    
    for field in KEYS_HRS:
        if pd.isna(gt[field]) or gt[field] == '':
            gt[field] = ''
        else:
            try:
                tmp = json.loads(gt[field])
                if field != 'employee_number_range':
                    tmp = str(sorted(tmp))        
                gt[field] = str(tmp).replace('"', '').replace("'", '')
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError for {field}: {gt[field]} - {e}")
                gt[field] = ''
    return gt[KEYS_HRS].to_dict()

def format_pred_HRS(pred):
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
    # if 'employee_number_range' in pred and pred['employee_number_range']:
    #     if isinstance(pred['employee_number_range'], list):
    #         pred['employee_number_range'] = str(sorted(pred['employee_number_range'])).replace('"', '').replace("'", '')
    #     else:
    #         employee_number_ranges = list(map(lambda x: x.strip(), pred['employee_number_range'].split(',')))
    #         if len(employee_number_ranges) > 1:
    #             pred['employee_number_range'] = str(sorted(employee_number_ranges)).replace('"', '').replace("'", '')
    #         else:
    #             pred['employee_number_range'] = str(employee_number_ranges).replace('"', '').replace("'", '')

    if 'employee_number_range' in pred and pred['employee_number_range']:
        ranges = pred['employee_number_range']
        if not isinstance(ranges, list):
            ranges = list(map(lambda x: x.strip(), ranges.split(',')))
        # if -1 not in ranges:
        #     ranges = sorted(ranges)
        pred['employee_number_range'] = str(ranges).replace('"', '').replace("'", '')
    else:
        pred['employee_number_range'] = ''
    # if 'status' in pred and pred['status']:
    #     status = pred['status']
    #     if not isinstance(status, list):
    #         status = list(map(lambda x: x.strip(), status.split(',')))
    #     pred['status'] = str(sorted(status)).replace('"', '').replace("'", '')
    # else:
    #     pred['status'] = ''
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
    if 'exclude' in pred and pred['exclude']:
        if isinstance(pred['exclude'], list):
            pred['exclude'] = str(sorted(pred['exclude'])).replace('"', '').replace("'", '')
        else:
            excludes = list(map(lambda x: x.strip(), pred['exclude'].split(',')))
            if len(excludes) > 1:
                pred['exclude'] = str(sorted(excludes)).replace('"', '').replace("'", '')
            else:
                pred['exclude'] = str(excludes).replace('"', '').replace("'", '')
    else:
        pred['exclude'] = ''
    return pred

# def format_prediction_HRS(pred):
#     # fields = ['affiliations', 'department', 'occupation', 'employment_type', 'lastname', 'firstname', 'employee_number', 'status']
    
#     for field in KEYS_HRS:
#         if field in pred and pred[field]:
#             if isinstance(pred[field], list):
#                 pred[field] = str(sorted(pred[field])).replace('"', '').replace("'", '')
#             else:
#                 items = list(map(lambda x: x.strip(), pred[field].split(',')))
#                 if len(items) > 1:
#                     pred[field] = str(sorted(items)).replace('"', '').replace("'", '')
#                 else:
#                     pred[field] = str(items).replace('"', '').replace("'", '')
#         else:
#             pred[field] = ''
    
#     return pred



def evaluation_sample_HSR(pred, gt, prompt):
    # print("gt: ", gt)
    gt = format_label_HRS(gt)
    # print(f"After processing: {gt}")

    # print("pred: ", pred)
    pred = format_pred_HRS(pred)
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