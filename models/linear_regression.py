from models.abstract_model import AbstractModel
from sklearn.linear_model import LinearRegression

class KNN(AbstractModel):
  def __init__(self, data, labels):
    super().__init__(data, labels)
    self.lr = LinearRegression()

  def train(self):
    self.lr.fit(self.get_training_data(), self.get_training_labels())

  def test(self):
    print(self.lr.score(self.get_testing_data(), self.get_testing_labels()))