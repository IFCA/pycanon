import numpy as np
import pandas as pd
import test_anonymity


def check_anonymity(file, QI, SA, l_new, new_file_name):
    df = pd.read_csv(file)

    max_l = []
    for sa in SA:
        max_l.append(len(np.unique(df[sa].values)))
    max_l = min(max_l)

    k = test_anonymity.calculate_k(df, QI)
    l = test_anonymity.calculate_l(df, QI, SA)
    entropy_l = test_anonymity.calculate_entropy_l(df, QI, SA)
    alpha, k_alpha = test_anonymity.get_alpha_k(df, QI, SA)
    basic_beta = test_anonymity.calculate_basic_beta(df, QI, SA)
    enhanced_beta = test_anonymity.calculate_enhanced_beta(df, QI, SA)
    delta_disclosure = test_anonymity.calculate_delta_disclosure(df, QI, SA)
    t = test_anonymity.calculate_t_closeness(df, QI, SA)
    c, _ = test_anonymity.calculate_c_l_diversity(df, QI, SA)

    assert k == k_alpha, 'Error. Check get_alpha_k() and calculate_k().'
    
    print(f'File: {file}. The dataset verifies k-anonymity with k={k}, l-diversity with l={l}, ')
    print(f'entropy l-diversity with l={entropy_l}, (alpha,k)-anonymity with alpha={alpha} and k={k}')
    print(f'basic beta-likeness with beta={basic_beta}, enhanced beta-likeness with beta={enhanced_beta},')
    print(f'delta-disclosure privacy with delta = {delta_disclosure}, t-closeness with t={t}') 
    if np.isnan(c) == False:
        print(f'and (c,l)-diversity with c={c} and l={l}.')
    else:
        print(f'as l={l} c cannot be calculated for (c,l)-diversity.')
    
    assert l_new <= max_l, f'Error, the maximum value for l is {max_l}' 
    df_new = test_anonymity.l_diversity(df, QI, SA, l_new)
    
    if len(df_new) > l_new:
        assert test_anonymity.calculate_l(df_new, QI, SA) == l_new, 'Error, check l_diversity().'
        df_new.to_csv(new_file_name, index = False)
        print(f'Dataset veryfying l-diversity with l={l_new} saved in: {new_file_name}. \n')
    else: 
        print(f'The dataset cannot verify l-diversity with l = {l_new} only by suppression. \n')
    
QI = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson']
file = './Data/Processed/StudentsMath_Score.csv'
SA = ['Score']
l_new = 3
new_file_name = f'./Data/l_diversity/StudentsMath_Score_l{l_new}.csv'
check_anonymity(file, QI, SA, l_new, new_file_name)

for i in [2, 5, 7]:
    file = f'./Data/Processed/StudentsMath_Score_k{i}.csv'
    new_file_name = f'./Data/l_diversity/StudentsMath_Score_k{i}_anonymized_l{l_new}.csv'
    check_anonymity(file, QI, SA, l_new, new_file_name)
    l_new += 2