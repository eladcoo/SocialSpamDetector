from sklearn.feature_extraction import DictVectorizer

from BE.basicGraph import getAmounts
from BE.communityManager import add_account_to_heap, get_max_element, heapify
from BE.RotatingForestAlg import train_model
from BE.featuresExtractor import extract_global_features, extract_local_features

def execute_ALD(top_suspect_communities,communities,communication_graph,num_of_rotations, k_param, run_stats):
    #train model
    global_features = extract_global_features(communication_graph)
    local_features = extract_local_features(communication_graph,communities)
    rf_models = train_model(communication_graph, communities, global_features, local_features, num_of_rotations)
    list_of_real_spammers, list_of_real_hammers = getAmounts()
    num_of_detected_spammers = 0
    num_of_undetected_spammers = 0
    heap = []
    vec = DictVectorizer()
    num_of_accounts = 0
    num_of_spammers = 0
    #  for each community and for each account in that community - run ML on that account and insert the score to a max heap
    for community in top_suspect_communities:
        level = int(community.split('-')[0])
        community_id = int(community.split('-')[1])
        for account in communities[level][community_id]:
            num_of_accounts += 1
            account_feature = {}
            account_feature.update(global_features[account])
            account_feature.update(local_features[account][community])
            account_feature_data = vec.fit_transform(account_feature).toarray()
            score = rf_models[level].predict(account_feature_data)
            if score[0] > 0:
                num_of_spammers+=1
                if account in list_of_real_spammers:
                    num_of_detected_spammers+=1
            else:
                if account in list_of_real_spammers:
                    num_of_undetected_spammers+=1
            add_account_to_heap(heap,account,score[0])

    heapify(heap)
    #show the K most suspicious accounts
    suspect_list = []
    scored_suspect_list = []

    if run_stats:
        print("num_of_spammers:", num_of_spammers)
        print("num_of_detected_spammers:", num_of_detected_spammers)
        print("num_of_undetected_spammers:", num_of_undetected_spammers)
        print("total_num_of_accounts:", num_of_accounts)
        print("num_of_ham:", num_of_accounts-num_of_spammers)

        while heap:
            score, account = get_max_element(heap)
            if account not in suspect_list and communication_graph.nodes[account]['color'] == 'blue':
                suspect_list.append(account)

        print("num_of_early_detection: ", len(suspect_list))

    else:
        while (len(suspect_list) < k_param) and heap:
            score, account = get_max_element(heap)
            if account not in suspect_list:
                suspect_list.append(account)
                scored_suspect_list.append((score, account))

        print("scored_suspect_list: ", scored_suspect_list)

    return scored_suspect_list