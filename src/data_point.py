import numpy as np

class DataPoint:
  def __init__(self, date):
    self.count = 0
    self.values = []
    self.sum = None
    self.variance = None
    self.date = date
  
  def add_entry(self, entry):
    self.count = self.count + 1
    self.values.append(entry)

  def get_average(self):
    return np.sum(self.values) / self.count

  def get_variance(self):
    return np.var(self.values)

  def as_dict(self):
    return {'count': self.count, 'average': self.get_average(), 'variance': self.get_variance(), 'timestamp': self.date}
