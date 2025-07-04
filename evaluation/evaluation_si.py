import pandas as pd


KEYS_SI = ['name_or_number', 'contract_arr', 'group_hash', 'status', 'is_chargeable', 'joined_at_from', 'joined_at_to', 'retired_at_from', 'retired_at_to']

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
    for key in KEYS_SI:
        if pd.isna(gt[key]) or gt[key] is None or gt[key] == "" or gt[key] == "nan":
            gt[key] = ""
    return gt[['name_or_number', 'contract_arr', 'group_hash', 'status', 'is_chargeable', 'joined_at_from', 'joined_at_to', 'retired_at_from', 'retired_at_to']].to_dict()

def format_prediction(pred):
    """
    Format the prediction data to match the expected format.
    """
    # for key in KEYS_TA_dynamic:
    #     if pd.isna(pred[key]) or pred[key] == '':
    #         pred[key] = ''
    #     else:
    #         tmp = json.loads(pred[key])
    #         tmp = str(sorted(tmp))
    #         pred[key] = tmp.replace('"','').replace("'",'')
    for key in KEYS_SI:
        if pred[key] is None or pred[key] == "" or pred[key] == "nan":
            pred[key] = ""
        if pred['status'] == '入社予定' or pred['status'] == '退職予定':
            pred['joined_at_from'] = ''
            pred['joined_at_to'] = ''
            pred['retired_at_from'] = ''
            pred['retired_at_to'] = ''
        if pred['joined_at_from'] == pred['joined_at_to']:
            pred['joined_at_to'] = ''
        if pred['retired_at_from'] == pred['retired_at_to']:
            pred['retired_at_to'] = ''
    return pred

def evaluate(pred, gt, prompt):
    gt = format_groundtruth(gt)
    pred = format_prediction(pred)
    for k in KEYS_SI:
        if pred[k] != gt[k].replace("'",''):
            print(k)
            print('Prompt: ', prompt)
            print('Predict: ', pred)
            print('groundtruth: ', gt)
            print("False")
            return [False, k]
    print("True")
    return [True, '']

