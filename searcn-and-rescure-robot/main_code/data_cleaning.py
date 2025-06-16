import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import scipy.stats as stats
import math

def getFirstElements(l):
  return [[item[0]] for item in l]

def getRest(l):
  return [item[1:] for item in l]

def getDataRows(fileName, n):
  data = []
  data_part = []
  with open(fileName) as f:
    lines = f.readlines()
    a = []
    for i in lines:
      a.append([i])
  for i in range(len(a)):
    data.append(a[i][0].split(","))
  data_part = [data[i][0:n] for i in range(len(data))]

  x = data_part[len(data_part) - 1][len(data_part[0]) - 1].strip()
  data_part[len(data_part) - 1][len(data_part[0]) - 1] = x

  data_clean = convertToDecimal(data_part)
  x = getFirstElements(data_clean)
  y = getRest(data_clean)
  y = np.matrix(y)
  return y

def convertToDecimal(l):
  for item in l:
    for i in range(len(item)):
      item[i] = item[i].strip()
      item[i] = float(item[i])
  return l

def cal_gaussian(measurement):
  m = np.mean(measurement, axis=0)
  if np.size(measurement,0) > 1:
    v = np.cov(measurement,rowvar=False)
  else:
    v = np.zeros([np.size(measurement,1),np.size(measurement,1)])
  return [m, v]


#Mean and variance
final_gaus = [0,0]

def plot_gaussian(final_gaus):
  sigma = math.sqrt(final_gaus[1])
  x = np.linspace(final_gaus[0] - 3*sigma, final_gaus[0] + 3*sigma, 100)
  plt.plot(x, stats.norm.pdf(x, final_gaus[0], sigma))
  plt.show()


def convert_actual_toMat(data):
    x = getFirstElements(data)
    temp = []
    for i in range(len(x)):
      for j in range(len(data[0])):
        temp += x[i]
    temp = np.array(temp)
    temp = temp.reshape(len(data),len(data[0]))
    return temp

def cal_variance(error):
  data_size =len(error)
  total_squared_error = 0
  variance = []
  for i in range(data_size):
    for j in range(len(error[0])):
      total_squared_error = math.pow(error[i][j], 2)
    variance.append(total_squared_error/(data_size-1))
    total_squared_error = 0 
  print('Variances:',variance)
  return variance

def plot_figure(x, y):
  font1 = {'family':'serif','color':'blue','size':20}
  font2 = {'family':'serif','color':'darkred','size':15}
  plt.title("Actual Distances vs. Measurements - Angle 0", fontdict = font1)
  plt.xlabel("Actual Distance", fontdict = font2)
  plt.ylabel("Measurements", fontdict = font2)
  plt.scatter(x, y)
  plt.show()
