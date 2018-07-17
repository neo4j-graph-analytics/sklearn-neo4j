import datetime

from neo4j.v1 import GraphDatabase, basic_auth
from sklearn import linear_model

from skneo4j.model_persistence import ModelPersistence

model_persistence = ModelPersistence(GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo")))

X = [[0., 0.], [1., 1.], [2., 2.], [3., 3.]]
Y = [0., 1., 2., 3.]
reg = linear_model.BayesianRidge()
reg.fit(X, Y)

model_name = "{0}-{1}".format(reg.__class__.__name__, int(datetime.datetime.timestamp(datetime.datetime.now())))
model_persistence.save(reg, model_name, ["coef_", "intercept_"])

print(reg.predict([[1, 0.]]))

new_reg = model_persistence.load(model_name)
print(new_reg.predict([[1, 0.]]))
