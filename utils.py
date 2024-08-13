import numpy as np
import os.path as osp

from numpy import dot
from numpy.linalg import norm
from transformers import AutoTokenizer

from models import ProductCategory
from config import PROPERTIES


LOCAL_FILE_PATH = PROPERTIES['LOCAL_FILE_PATH']


"""코사인 유사도"""
def cos_sim(A, B):
  return dot(A, B)/(norm(A)*norm(B))

def save_numpy(path, arr):
  with open(osp.join(LOCAL_FILE_PATH, path), 'wb') as f:
    np.save(f, arr)

def load_numpy(path):
  with open(osp.join(LOCAL_FILE_PATH, path), 'rb') as f:
    arr = np.load(f, allow_pickle=True)
  return arr

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

class FileUtils:

  def __init__(self):
    return
  
  @staticmethod
  def existsFile(path):
      return osp.isfile(osp.join(LOCAL_FILE_PATH, path))