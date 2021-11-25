import yaml

from yaml_merger import YamlMergerImpl, YamlMerger


def test_given_example():
    with open('test-example.yml') as f:
        yml = f.read()

    yml_config = ('- image: tfidf_vectorizer:0.1\n'
                  '  imagePullPolicy: IfNotPresent\n'
                  '  name: tfidfvectorizer')

    yaml_merger: YamlMerger = YamlMergerImpl()

    expected = '''apiVersion: machinelearning
kind: SeldonDeployment
metadata:
  labels:
    app: seldon
  name: seldon-deployment-{{workflow.name}}
  namespace: kubeflow
spec:
  annotations:
    project_name: NLP Pipeline
    deployment_version: v1
  name: seldon-deployment-{{workflow.name}}
  predictors:
  - componentSpecs:
    - spec:
        containers:
        - image: clean_text_transformer:0.1
          imagePullPolicy: IfNotPresent
          name: cleantext
        - image: tfidf_vectorizer:0.1
          imagePullPolicy: IfNotPresent
          name: tfidfvectorizer
        volumes:
        - name: mypvc
          persistentVolumeClaim:
            claimName: '{{workflow.name}}-my-pvc'
    graph:
      children:
      - name: spacytokenizer
        endpoint:
          type: REST
    annotations:
      predictor_version: v1
'''

    result = yaml_merger.merge(yml, yml_config)

    assert result == expected

