import pandas as pd
import json

KEYS_TA_dynamic = ['group_id','authority_type']
KEYS_TA = ['specified_name_or_number','specified_login_address','encrypted_selected_group_id','selected_authority_type_option','selected_connected_with_option','selected_working_status_option','selected_joined_at_from','selected_joined_at_to','selected_retired_at_from','selected_retired_at_to']

def format_groundtruth(gt):
    """
    Format the groundtruth data to match the expected format.
    """
    # for key in KEYS_TA_dynamic:
    #     if pd.isna(gt[key]) or gt[key] == '':
    #         gt[key] = ''
    #     else:
    #         tmp = json.loads(gt[key])
    #         tmp = str(sorted(tmp))
    #         gt[key] = tmp.replace('"','').replace("'",'')
    for key in KEYS_TA:
        if pd.isna(gt[key]) or gt[key] == '':
            gt[key] = ''
    return gt[['specified_name_or_number','specified_login_address','encrypted_selected_group_id','selected_authority_type_option','selected_connected_with_option','selected_working_status_option','selected_joined_at_from','selected_joined_at_to','selected_retired_at_from','selected_retired_at_to']].to_dict()

def format_prediction(pred):
    """
    Format the prediction data to match the expected format.
    """
    for key in KEYS_TA_dynamic:
        if pd.isna(pred[key]) or pred[key] == '':
            pred[key] = ''
        else:
            tmp = json.loads(pred[key])
            tmp = str(sorted(tmp))
            pred[key] = tmp.replace('"','').replace("'",'')
    for key in KEYS_TA:
        if pd.isna(pred[key]) or pred[key] == '':
            pred[key] = ''
    return pred

def evaluate(pred, gt, prompt):
    gt = format_groundtruth(gt)
    for k in KEYS_TA:
        if pred[k] != gt[k].replace("'",''):
            print(k)
            print('Prompt: ', prompt)
            print('Predict: ', pred)
            print('groundtruth: ', gt)
            print("False")
            return [False, k]
    print("True")
    return [True, '']