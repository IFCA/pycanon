"""Example using the drug type prediction dataset."""

import numpy as np
import test_anonymity

def check_anonymity(file_name, quasi_ident, sens_att, l_new, new_file_name):
    """Function for check all the anonymity techniques under study."""
    k_anon = test_anonymity.calculate_k(file_name, quasi_ident)
    l_div = test_anonymity.calculate_l(file_name, quasi_ident, sens_att)
    entropy_l = test_anonymity.calculate_entropy_l(file_name, quasi_ident, sens_att)
    alpha, _ = test_anonymity.get_alpha_k(file_name, quasi_ident, sens_att)
    basic_beta = test_anonymity.calculate_basic_beta(file_name, quasi_ident, sens_att)
    enhanced_beta = test_anonymity.calculate_enhanced_beta(file_name, quasi_ident, sens_att)
    delta_disclosure = test_anonymity.calculate_delta_disclosure(file_name, quasi_ident, sens_att)
    t_clos = test_anonymity.calculate_t_closeness(file_name, quasi_ident, sens_att)
    c_div, _ = test_anonymity.calculate_c_l_diversity(file_name, quasi_ident, sens_att)

    print(f'''File: {file_name}. The dataset verifies:
    \t - k-anonymity with k = {k_anon}
    \t - (alpha,k)-anonymity with alpha = {alpha} and k = {k_anon}
    \t - l-diversity with l = {l_div}
    \t - entropy l-diversity with l = {entropy_l}
    \t - basic beta-likeness with beta = {basic_beta}
    \t - enhanced beta-likeness with beta = {enhanced_beta}
    \t - delta-disclosure privacy with delta = {delta_disclosure}
    \t - t-closeness with t = {t_clos}''')
    if np.isnan(c_div):
        print(f'\t - As l = {l_div} for l-diversity, c cannot be calculated for (c,l)-diversity.\n')
    else:
        print(f'\t - (c,l)-diversity with c = {c_div} and l = {l_div}.\n')

    data = test_anonymity.read_file(file_name)
    max_l = []
    for sa_value in sens_att:
        max_l.append(len(np.unique(data[sa_value].values)))
    max_l = min(max_l)

    assert l_new <= max_l, f'Error, the maximum value for l is {max_l}'
    df_new = test_anonymity.l_diversity(file_name, quasi_ident, sens_att, l_new)
    if len(df_new) > l_new:
        df_new.to_csv(new_file_name, index = False)
        print(f'Dataset veryfying l-diversity with l = {l_new} saved in: {new_file_name}.\n')
    else:
        print(f'The dataset cannot verify l-diversity with l = {l_new} only by suppression.\n')

QI = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']
SA = ['Drug']
FILE_NAME = '../Data/Processed/drug_type.csv'
L_NEW = 2
NEW_FILE_NAME = f'../Data/l_diversity/drug_type_l{L_NEW}.csv'
check_anonymity(FILE_NAME, QI, SA, L_NEW, NEW_FILE_NAME)

L_NEW = 3
FILE_NAME = '../Data/Processed/drugs_k5.csv'
NEW_FILE_NAME = f'../Data/l_diversity/drugs_k5_anonymized_l{L_NEW}.csv'
check_anonymity(FILE_NAME, QI, SA, L_NEW, NEW_FILE_NAME)