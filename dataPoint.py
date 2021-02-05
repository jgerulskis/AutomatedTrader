import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class DataPoint:
  def __init__(self, date):
    self.count = 0
    self.sum = 0
    self.date = date
  
  def add_entry(self, entry):
    self.count = self.count + 1
    self.sum = self.sum + entry

  def get_average(self):
    return self.sum / self.count

  def as_dict(self):
    return {'count': self.count, 'average': self.get_average(), 'date': self.date}

