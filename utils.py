import pickle
import numpy as np

from numpy import dot
from numpy.linalg import norm
from transformers import AutoTokenizer

from models import ProductCategory


"""코사인 유사도"""
def cos_sim(A, B):
  return dot(A, B)/(norm(A)*norm(B))

"""Numpy Array -> Text"""
def ndarray_to_text(arr):
  return pickle.dumps(arr)

"""Text -> Numpy Array"""
def text_to_ndarray(text):
  return pickle.loads(text)


class SingletonInstane:
  __instance = None

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__getInstance
    return cls.__instance
  

class Tokenizer(SingletonInstane):
  _tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

  def __init__(self):
    return
  
  def get_product_vector(self, content, category_idx):
    product_vector = self.get_empty_vector()
    indices = np.append(self.__encode(content).squeeze(axis=0), np.array([category_idx]), axis=0)
    product_vector[indices] += 1
    return product_vector
  
  def get_empty_vector(self):
    return np.append([0] * Tokenizer._tokenizer.vocab_size, np.array([0] * ProductCategory.__len__()), axis=0)
  
  def __encode(self, content):
    return Tokenizer._tokenizer.encode(content, return_tensors='np')
