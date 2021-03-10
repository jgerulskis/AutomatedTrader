from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

class AbstractModel:
  def __init__(self, data, labels):
    self.data = data
    self.labels = labels
    self.training_data, self.testing_data, self.training_labels, self.testing_labels = train_test_split(data, labels)
    self.predicted = None
  
  def get_training_data(self):
    return self.training_data
  
  def get_training_labels(self):
    return self.training_labels
  
  def get_testing_data(self):
    return self.testing_data
  
  def get_testing_labels(self):
    return self.testing_labels

  def test(self):
    pass

  def evaluate(self):
    fig, ax = plt.subplots()
    ax.scatter(self.predicted, self.get_testing_labels(), edgecolors=(0, 0, 1))
    ax.plot([self.get_testing_labels().min(), self.get_testing_labels().max()], [self.get_testing_labels().min(), self.get_testing_labels().max()], 'r--', lw=3)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    plt.show()
    mae = metrics.mean_absolute_error(self.get_testing_labels(), self.predicted)
    mse = metrics.mean_squared_error(self.get_testing_labels(), self.predicted)
    r2 = metrics.r2_score(self.get_testing_labels(), self.predicted)

    print("The model performance for testing set")
    print("--------------------------------------")
    print('Mean Average Error is {}'.format(mae))
    print('Mean Squared Error is {}'.format(mse))
    print('R2 score is {}'.format(r2))