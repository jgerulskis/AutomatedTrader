from sklearn.linear_model import LinearRegression
from models.abstract_model import AbstractModel
from sklearn import metrics
import matplotlib.pyplot as plt

class LR(AbstractModel):
  def __init__(self, data, labels):
    super().__init__(data, labels)
    self.lr = LinearRegression().fit(self.get_training_data(), self.get_training_labels())

  def test(self):
    predicted = self.lr.predict(self.get_testing_data())
    fig, ax = plt.subplots()
    ax.scatter(predicted, self.get_testing_labels(), edgecolors=(0, 0, 1))
    ax.plot([self.get_testing_labels().min(), self.get_testing_labels().max()], [self.get_testing_labels().min(), self.get_testing_labels().max()], 'r--', lw=3)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    plt.show()
    mae = metrics.mean_absolute_error(self.get_testing_labels(), predicted)
    mse = metrics.mean_squared_error(self.get_testing_labels(), predicted)
    r2 = metrics.r2_score(self.get_testing_labels(), predicted)

    print("The model performance for testing set")
    print("--------------------------------------")
    print('Mean Average Error is {}'.format(mae))
    print('Mean Squared Error is {}'.format(mse))
    print('R2 score is {}'.format(r2))
