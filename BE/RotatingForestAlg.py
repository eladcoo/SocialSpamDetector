from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
def setFeaturesForRF(G, globalFeatures, localFeatures):
    rf_features = dict()
    feature_dicts = []
    spam_labels = []
    for node in G.nodes():
        node_feature = {}
        node_feature.update(globalFeatures[node])
        node_feature.update(localFeatures[node])
        feature_dicts.append(node_feature)
        spam_labels.append(1 if G.nodes[node]['color'] == 'red' else 0)

    # Convert the dictionary objects to a feature matrix
    vec = DictVectorizer()
    data = vec.fit_transform(feature_dicts).toarray()
    rf_features["feature_dicts"] = data
    rf_features["spam_labels"] = spam_labels
    return rf_features


def trainModel(G, globalFeatures, localFeatures, num_of_rotations):
    rf_features = setFeaturesForRF(G, globalFeatures, localFeatures)
    print("spam_labels: ",  rf_features["spam_labels"])

    rf = RandomForestClassifier(n_estimators=num_of_rotations)
    rf.fit(rf_features["feature_dicts"], rf_features["spam_labels"])

    return rf