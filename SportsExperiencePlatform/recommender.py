import numpy as np
from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
import joblib
from google.cloud import storage

BUCKET_NAME = 'wagon-817-project-sports'
STORAGE_LOCATION = 'models/recommender/model_template.joblib'

iris = datasets.load_iris()
X = iris["data"][:, (2, 3)] # Länge, Breite der Kronblätter
y = (iris["target"] == 2).astype(np.float64) # Iris virginica
svm_clf = Pipeline([
("scaler", StandardScaler()),
("linear_svc", LinearSVC(C=1, loss="hinge")),
])
svm_clf.fit(X, y)

client = storage.Client()

bucket = client.bucket(BUCKET_NAME)

blob = bucket.blob(STORAGE_LOCATION)
joblib.dump(svm_clf, 'model_template.joblib')
blob.upload_from_filename('model_template.joblib')
