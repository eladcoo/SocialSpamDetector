from sklearn.feature_extraction import DictVectorizer
from BE.communityManager import add_account_to_heap, get_max_element, heapify
from BE.RotatingForestAlg import train_model
from BE.featuresExtractor import extract_global_features, extract_local_features

def execute_ALD(top_suspect_communities,communities,communication_graph,num_of_rotations, k_param):
    #train model
    global_features = extract_global_features(communication_graph)
    local_features = extract_local_features(communication_graph,communities)
    rf_models = train_model(communication_graph, communities, global_features, local_features, num_of_rotations)

    heap = []
    vec = DictVectorizer()

    #  for each community and for each account in that community - run ML on that account and insert the score to a max heap
    for community in top_suspect_communities:
        level = int(community.split('-')[0])
        community_id = int(community.split('-')[1])
        for account in communities[level][community_id]:
            account_feature = {}
            account_feature.update(global_features[account])
            account_feature.update(local_features[account][community])
            account_feature_data = vec.fit_transform(account_feature).toarray()
            score = rf_models[level].predict(account_feature_data)
            print("score:", score[0])
            add_account_to_heap(heap,account,score[0])

    heapify(heap)
    #show the K most suspicious accounts
    suspect_list = []
    while (len(suspect_list) < k_param) and heap:
        account = get_max_element(heap)
        if account not in suspect_list:
            suspect_list.append(account)

    print("suspect_list: ", suspect_list)

    return suspect_list