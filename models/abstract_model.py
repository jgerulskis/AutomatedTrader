from sklearn.model_selection import train_test_split

class AbstractModel:
  def __init__(self, data, labels):
    self.data = data
    self.labels = labels
    self.training_data, self.testing_data, self.training_labels, self.testing_labels = train_test_split(data, labels)
  
  def get_training_data(self):
    return self.training_data
  
  def get_training_labels(self):
    return self.training_labels
  
  def get_testing_data(self):
    return self.testing_data
  
  def get_testing_labels(self):
    return self.testing_labels

  def train(self):
    pass

  def test(self):
    pass