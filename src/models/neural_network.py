import pandas as pd
from sklearn.neural_network import MLPRegressor
from models.abstract_model import AbstractModel
from sklearn.preprocessing import StandardScaler

class MLP(AbstractModel):
  def __init__(self, data, labels):
    scaler = StandardScaler().fit(data)
    data = pd.DataFrame(scaler.transform(data))
    super().__init__(data, labels)
    self.mlp = MLPRegressor(solver='lbfgs', max_iter=5000, tol=1e-7, n_iter_no_change=500).fit(self.get_training_data(), self.get_training_labels())
    print(self.mlp.n_layers_)

  def test(self):
    self.predicted = self.mlp.predict(self.get_testing_data())
    print(self.predicted)
