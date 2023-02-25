def make_efficientnet():
    import backend.classifiers.efficientnet

    return backend.classifiers.efficientnet.EfficientNetClassifier()


classifier_makers = {
    "tf-efficientnet": make_efficientnet,
}
