from sklearn.linear_model import LinearRegression
from models.abstract_model import AbstractModel

class LR(AbstractModel):
  def __init__(self, data, labels):
    super().__init__(data, labels)
    self.lr = LinearRegression().fit(self.get_training_data(), self.get_training_labels())

  def test(self):
    self.predicted = self.lr.predict(self.get_testing_data())