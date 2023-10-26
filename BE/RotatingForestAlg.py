from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer


def calculate_vector_sets(G, communities, global_features, local_features):
    spam_vector_sets = {}
    ham_vector_sets = {}

    for level in communities:
        spam_vector_sets[level] = []
        ham_vector_sets[level] = []
        for community_id in communities[level]:
            for node in communities[level][community_id]:
                node_vector_set = {}
                node_vector_set.update(global_features[node])
                node_vector_set.update(local_features[node][f"{level}-{community_id}"])
                if G.nodes[node]['color'] == 'red':
                    spam_vector_sets[level].append(node_vector_set)
                else:
                    ham_vector_sets[level].append(node_vector_set)

    return spam_vector_sets,ham_vector_sets


def train_model(G, communities, global_features, local_features, num_of_rotations):
    spam_vector_sets, ham_vector_sets = calculate_vector_sets(G, communities, global_features, local_features)
    vec = DictVectorizer()
    level_models = {}
    # undersampling
    for level in communities:
        if(len(spam_vector_sets[level])):
            level_vector_set = []
            level_vector_set.extend(spam_vector_sets[level])
            level_vector_set.extend(ham_vector_sets[level][0::len(spam_vector_sets[level])])

            level_spam_labels = [1]*len(spam_vector_sets[level])
            level_spam_labels.extend([0]*(len(level_vector_set) - len(spam_vector_sets[level])))

            # Convert the dictionary objects to a feature matrix
            level_data = vec.fit_transform(level_vector_set).toarray()
            level_model = RandomForestClassifier(n_estimators=num_of_rotations)
            level_model.fit(level_data, level_spam_labels)

            level_models[level] = level_model


    return level_models