from accountLevelDetector import extractGlobalFeatures, extractLocalFeatures
from graph import buildTrainingGraph, buildDataGraph
from RotatingForestAlg import trainModel, setFeaturesForRF

def trainRFModel(num_of_rotations):
    training_graph = buildTrainingGraph("resources/ham","resources/spam")
    train_global_features = extractGlobalFeatures(training_graph)
    train_local_features = extractLocalFeatures(training_graph)

    rf_model = trainModel(training_graph,train_global_features,train_local_features,num_of_rotations)
    return rf_model

def runSCD(path, num_of_rotations, implementation_param, k_param,display_options):

    #TODO: run scd algorithm

    #train model
    rf_model = trainRFModel(num_of_rotations)
    data_graph = buildDataGraph(path)
    data_global_features = extractGlobalFeatures(data_graph)
    data_local_features = extractLocalFeatures(data_graph)
    data_features = setFeaturesForRF(data_graph,data_global_features,data_local_features)

#   #for each community, run the ml on that community and for each account - insert the score to a max heap
    predictions = rf_model.predict(data_features["feature_dicts"])
    print("predictions:", predictions)

    #show the K most suspicious accounts