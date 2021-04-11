# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16GXkFvb6TwKcR6xpMpd1RDzFLMk1bYK4
"""

import numpy as np
import PIL
from PIL import Image
from os import listdir
from matplotlib import image
import scipy.optimize as opt
import math

def RandomInitialiseWeights(A,B):
  epsilon_init = 0.12;
  arr=np.random.rand(A,B)
  arr=arr*2*epsilon_init-epsilon_init
  return arr

def sigmoid(z):
  g=np.zeros(z.shape)
  g=1/(1+np.exp(-z))
  return g

def CostFunction(nnParams):

  #initialisation of ds required later in the function

  nnParams=np.array(nnParams,dtype=float)

  Theta1=nnParams[0:(HIDDEN1_LAYER_SIZE*(INPUT_LAYER_SIZE+1))]
  Theta1=Theta1.reshape((HIDDEN1_LAYER_SIZE,INPUT_LAYER_SIZE+1))


  Theta2=nnParams[ HIDDEN1_LAYER_SIZE*(INPUT_LAYER_SIZE+1) :nnParams.size]
  Theta2=Theta2.reshape((NUM_LABELS,HIDDEN1_LAYER_SIZE+1))

  #Fake Thetas for regularisation

  Temp_Theta1 = Theta1 
  Temp_Theta2 = Theta2

  for i in range(Theta1.shape[0]):
    Temp_Theta1[i][0]=0
  
  for i in range(Theta2.shape[0]):
    Temp_Theta2[i][0]=0
 
  Temp_nnParams = np.concatenate( (Temp_Theta1.reshape(Theta1.size,1),Temp_Theta2.reshape(Theta2.size,1)),axis=0 ) #just for the regularisation part of the cost 

  #forward propogation for cost calculation

  #calculating second layer units for all test cases

  A2 = np.dot( Theta1 , X.transpose() )

  A2 = sigmoid(A2)


  A2 = np.concatenate( (np.ones((1,M)) , A2) , axis = 0 ) #creating bias unit in all test cases

  #calculating third layer units/final output layer for all test cases

  A3 = np.dot( Theta2 , A2 )

  A3 = sigmoid(A3)

  #We don't need bias unit for the final output layer

  #calculating the cost for all the test cases considering all the classes output

  Total_Cost = 0 

  

  for i in range(M) :

    output_here = A3[:,i]
    output_here = output_here.reshape( (output_here.size,1) )
    true_output = Y[:,i]
    true_output = true_output.reshape( (true_output.size,1) )

    cost = -( true_output * (np.log(output_here)) + (1-true_output)* ( np.log( 1 - output_here ) ) )

    Total_Cost = Total_Cost + np.sum(cost)

  Total_Cost = ( Total_Cost/M ) + ( (Lambda/(2*M)) * np.sum( np.power(Temp_nnParams,2)   ))

  
  

  #Now BackPropagation for Gradient of Weights

  #print "size of theta1 and theta2 are",Theta1.shape,Theta2.shape

  Cap_Delta1 = np.zeros(Theta1.shape)
  Cap_Delta2 = np.zeros(Theta2.shape)

  #print "BACKWARD PPGN STARTED"

  for i in range(M) :

    delta_3 = A3[:,i] - Y[:,i] 
    delta_3 = delta_3.reshape(10,1)

    a2 = A2[:,i] 
    a2 = a2.reshape(A2.shape[0],1)

    delta_2 = ( np.dot(Theta2.transpose(),delta_3) ) * a2 * (1-a2)

    delta_2 = np.delete(delta_2,0,axis=0)

    Cap_Delta2 = Cap_Delta2 + ( np.dot( delta_3 , a2.transpose() ) ) 

    x = X[i,:]
    x = x.reshape(1 , x.size )

    Cap_Delta1 = Cap_Delta1 + ( np.dot( delta_2 ,  x  ) )

    #print "TEST CASE ",i

  #print "BACKWARD PPGN DONE"

  #Now time for gradient calculation using these capital deltas

  Theta2_Grad = ( Cap_Delta2/M ) + ( (Lambda/M) * Temp_Theta2 )
  Theta1_Grad = ( Cap_Delta1/M ) + ( (Lambda/M) * Temp_Theta1 )

  Theta2_Grad = Theta2_Grad.reshape( (Theta2_Grad.size) , 1 )
  Theta1_Grad = Theta1_Grad.reshape( (Theta1_Grad.size) , 1 )

  Gradient = np.concatenate( (Theta1_Grad,Theta2_Grad),axis=0 )

  return Total_Cost,Gradient

"""PREDICT FUNCTION"""

def predict(x):

  A2 = np.dot( OPT_Theta1 , x.transpose() )

  A2 = sigmoid(A2)

  A2 = np.concatenate( (np.ones((1,1)) , A2) , axis = 0 ) 

  A3 = np.dot( OPT_Theta2 , A2 )

  A3 = sigmoid(A3)
  
  maxi=-1
  maxv=-1

  #print A3

  for i in range(A3.shape[0]):

    if A3[i][0] > maxv :
      maxv=A3[i][0]
      maxi=i
  
  return maxi

def check_BP() :
  global Lambda
  prev=Lambda
  Lambda=0
  J,GRAD_BY_CF=CostFunction(initial_theta)

  GRAD_MANNUAL=np.zeros(GRAD_BY_CF.shape)

  initial_theta2=np.zeros(initial_theta.shape)
  e = 1e-4
  RelDiff=0

  for i in range(10):
    initial_theta2[i][0] = e 
    J1,G1= CostFunction( initial_theta+initial_theta2 ) 
    J2,G1= CostFunction( initial_theta-initial_theta2 )
    GRAD_MANNUAL[i][0]=(J1-J2)/(2*e)
    RelDiff += abs( GRAD_MANNUAL[i][0] - GRAD_BY_CF[i][0] )
    initial_theta2[i][0] = 0
    
  print "RELATIVE DIFFERENC IN GRADIENT : ",RelDiff

  Lambda=prev

#!unzip trainingSet.zip

"""LOADING AND VISUALISING THE DATASET"""

X2=[] #for the parameters/features of the dataset
Y2=[] #the output value of the dataset
print "Getting Data"
mp={}
for digit in range(10):
  
  count2=0
  for filename in listdir("/content/trainingSet/"+str(digit)):
    count2+=1
    if count2>=100 :
      break

    #load image
    img_here = Image.open("/content/trainingSet/"+str(digit)+"/"+filename)
    img_here = img_here.convert(mode='L')
    img_here.thumbnail((20,20))
    x_features=np.array(img_here,dtype=float)
    #print x_features.shape
    x_features=x_features.flatten()
    #print x_features.shape
    x_features /= 255.0
    x_features=x_features.tolist()
    x_features.insert(0,1)
    X2.append(x_features)
    Y2.append(int(digit))

print "Data Stored Locally"

"""SETTING UP PARAMETERS 

"""

print "INITIALISING THE PARAMETERS"

Y=np.array(Y2)
X=np.array(X2)

M=X.shape[0]
INPUT_LAYER_SIZE = len(X[0])-1
HIDDEN1_LAYER_SIZE = 26
NUM_LABELS = 10 
INITIAL_THETA1 = RandomInitialiseWeights(HIDDEN1_LAYER_SIZE,INPUT_LAYER_SIZE+1)
INITIAL_THETA2 = RandomInitialiseWeights(NUM_LABELS,HIDDEN1_LAYER_SIZE+1)
INITIAL_THETA1 = INITIAL_THETA1.reshape(INITIAL_THETA1.size,1)
INITIAL_THETA2 = INITIAL_THETA2.reshape(INITIAL_THETA2.size,1)
initial_theta = np.concatenate((INITIAL_THETA1,INITIAL_THETA2),axis=0)
Lambda=0.2
Y_new=np.zeros((M,10),dtype=np.float)

for i in range(M):
  Y_new[i][Y[i]]=1 

Y=Y_new.transpose()

print "PARAMETERS INITIALISED"
#print M

"""CHECK BP"""

check_BP()

"""TRAINING NEURAL NETWORK"""

print "TRAINING NEURAL NETWORK"

OPT_THETA = opt.fmin_tnc(func=CostFunction, x0=initial_theta,maxfun=100)

"""ACCURACY

"""

opt2 = OPT_THETA[0]
opt2 = np.array(opt2)
opt2 = opt2.reshape(opt2.size,1)

J1 = CostOnly(initial_theta)
print "COST BEFORE ",J1
J = CostOnly(opt2)
print "COST AFTER OPTM ",J

OPT_Theta1=opt2[0:(HIDDEN1_LAYER_SIZE*(INPUT_LAYER_SIZE+1))]
OPT_Theta1=OPT_Theta1.reshape((HIDDEN1_LAYER_SIZE,INPUT_LAYER_SIZE+1))

OPT_Theta2=opt2[ HIDDEN1_LAYER_SIZE*(INPUT_LAYER_SIZE+1) :len(opt2)]
OPT_Theta2=OPT_Theta2.reshape((NUM_LABELS,HIDDEN1_LAYER_SIZE+1))

correct_ans=0.0

for i in range(M):

  x = X[i,:]
  x = x.reshape(1,x.size)
  predicted_digit = predict(x)
  
  for j in range(10):
    if Y[j][i] == 1 :
      correct_digit = j 
      break 
  
  #print i,predicted_digit,correct_digit
  if predicted_digit == correct_digit :
    correct_ans += 1 

#print correct_ans
print "ACCURACY IN TRAINING SET",(correct_ans/M)*100

#!unzip testSet.zip

"""ACCURACY IN TEST SET

"""

from random import shuffle
from glob import glob
files = glob(r"/content/testSet")
shuffle(files)

count2=0.0
correct_ans=0.0
for filename in listdir("/content/testSet"):
  count2+=1
  if count2>= 20:
    break
  img_here = Image.open("/content/testSet/"+filename)
  display(img_here)
  img_here = img_here.convert(mode='L')
  img_here.thumbnail((20,20))
  x_features=np.array(img_here,dtype=float)
  #print x_features.shape
  x_features=x_features.flatten()
  #print x_features.shape
  x_features /= 255.0
  x_features=x_features.tolist()
  x_features.insert(0,1)
  x_features = np.array(x_features)
  x_features = x_features.reshape(1,x_features.size)
  
  print predict(x_features)
  print "IF CORRECT : 1 \nIF WRONG : 0 \nTO EXIT : 2"
  check = int(raw_input())
  if check == 1 :
    correct_ans+=1
  elif check == 2 :
    count2-=1
    break 

#print correct_ans
print (correct_ans/count2)*100