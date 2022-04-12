"""Example using the drug type prediction dataset."""

import numpy as np
import pandas as pd
import test_anonymity


def check_anonymity(file_name, quasi_ident, sens_att, l_new, new_file_name):
    """Function for check all the anonymity techniques under study."""
    data = pd.read_csv(file_name)

    max_l = []
    for sa_value in sens_att:
        max_l.append(len(np.unique(data[sa_value].values)))
    max_l = min(max_l)

    k_anon = test_anonymity.calculate_k(data, quasi_ident)
    l_div = test_anonymity.calculate_l(data, quasi_ident, sens_att)
    entropy_l = test_anonymity.calculate_entropy_l(data, quasi_ident, sens_att)
    alpha, k_alpha = test_anonymity.get_alpha_k(data, quasi_ident, sens_att)
    basic_beta = test_anonymity.calculate_basic_beta(data, quasi_ident, sens_att)
    enhanced_beta = test_anonymity.calculate_enhanced_beta(data, quasi_ident, sens_att)
    delta_disclosure = test_anonymity.calculate_delta_disclosure(data, quasi_ident, sens_att)
    t_clos = test_anonymity.calculate_t_closeness(data, quasi_ident, sens_att)
    c_div, _ = test_anonymity.calculate_c_l_diversity(data, quasi_ident, sens_att)

    assert k_anon == k_alpha, 'Error. Check get_alpha_k() and calculate_k().'
    print(f'''File: {file_name}. The dataset verifies k-anonymity with k={k_anon}, l-diversity
    with l={l_div}, entropy l-diversity with l={entropy_l}, (alpha,k)-anonymity with alpha={alpha}
    and k = {k_anon}, basic beta-likeness with beta = {basic_beta}, enhanced beta-likeness with
    beta = {enhanced_beta}, delta-disclosure privacy with delta = {delta_disclosure}, t-closeness
    with t={t_clos}.''')
    if np.isnan(c_div) is False:
        print(f'and (c,l)-diversity with c={c_div} and l={l_div}.')
    else:
        print(f'as l={l_div} c cannot be calculated for (c,l)-diversity.')
    assert l_new <= max_l, f'Error, the maximum value for l is {max_l}'
    df_new = test_anonymity.l_diversity(data, quasi_ident, sens_att, l_new)
    if len(df_new) > l_new:
        df_new.to_csv(new_file_name, index = False)
        print(f'Dataset veryfying l-diversity with l={l_new} saved in: {new_file_name}.\n')
    else:
        print(f'The dataset cannot verify l-diversity with l = {l_new} only by suppression.\n')
QI = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']
SA = ['Drug']
FILE_NAME = './Data/Processed/drug_type.csv'
L_NEW = 2
NEW_FILE_NAME = f'./Data/l_diversity/drug_type_l{L_NEW}.csv'
check_anonymity(FILE_NAME, QI, SA, L_NEW, NEW_FILE_NAME)

L_NEW = 3
FILE_NAME = './Data/Processed/drugs_k5.csv'
NEW_FILE_NAME = f'./Data/l_diversity/drugs_k5_anonymized_l{L_NEW}.csv'
check_anonymity(FILE_NAME, QI, SA, L_NEW, NEW_FILE_NAME)
