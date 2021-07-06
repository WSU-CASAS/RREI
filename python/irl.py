import glob
from class_irl import cont_mdp
from itertools import product
import numpy as np
import scipy as sp
from scipy import optimize
from copy import deepcopy
import datetime
from sklearn.preprocessing import MinMaxScaler
import time
from scipy import math
from scipy import linalg
import sys
import random
import pandas as pd
import pickle
import datetime
import os
import re
from scipy import stats
import rooms_cells
import paths_date
from datetime import datetime, timedelta

def count_from_traj(trajs, objs):
    for traj in trajs:
        for i in range(len(traj[0])-1):

            current_step=traj[0][i]
            next_step=traj[0][i+1]
            x1=current_step[0]
            y1=current_step[1]
            x2=next_step[0]
            y2=next_step[1]

            if (abs(x2-x1)>1 or abs(y2-y1)>1):
                continue
            col = 9
            grid_index = col*(x1-1) + y1-1
            objs[grid_index].x = x1
            objs[grid_index].y = y1

            action_index = 3*(x2-(x1-1)) + (y2-(y1-1))
            objs[grid_index].a[action_index] += 1

def policy_from_traj(objs):
    for grid_i in range(0, 72):
        for p_i in range(0, 9):
            objs[grid_i].p[p_i] = objs[grid_i].a[p_i]/np.sum(objs[grid_i].a)

def grid_action_index(current_step, next_step):
    x1=current_step[0]
    y1=current_step[1]
    x2=next_step[0]
    y2=next_step[1]
    col = 9
    grid_index = col*(x1-1) + y1-1
    action_index = 3*(x2-(x1-1)) + (y2-(y1-1))
    return grid_index, action_index


def calculate_ratio_from_policies(sample_traj,base_policy,objs):
    ratios=[]
    for traj in sample_traj:
        ratio=1
        for i in range(len(traj[0])-1):
            current_step=traj[0][i]
            next_step=traj[0][i+1]
            grid_index, action_index = grid_action_index(current_step, next_step)
            try:
                ratio+=math.log(base_policy/float(objs[grid_index][action_index]))
            except:
                ratio+=0
        ratios.append(ratio)
    return np.array(ratios)


def norm(first_element,second_element):    
    max_norm=0
    for i in range(len(first_element)):
        max_norm += math.pow(abs(first_element[i]-second_element[i]),2)
    return max_norm

def calculate_sample_importance(feature_matrix, theta, ratio, l_feature):
    iterated_rewards=ratio+np.dot(theta,feature_matrix.T)
    feature_count=np.zeros(l_feature)
    sample_importance=0
    iterated_rewards -= max(iterated_rewards)
    for i in range(len(feature_matrix)):
        sample_importance += math.exp(iterated_rewards[i])
        feature_count += math.exp(iterated_rewards[i])*feature_matrix[i]
        
    return feature_count, sample_importance

def gradient_func(ratio, feature_matrix ,learning_rate, feature_expectation, threshold):
    diff=float('inf')
    l_feature = len(feature_expectation)
    theta=np.random.random(size=(l_feature,))
    counter=0
    while ( abs(diff) > threshold and counter <= 100000):
        feature_count, sample_importance = calculate_sample_importance(feature_matrix, theta, ratio,  l_feature)
        gradient = feature_expectation-feature_count/float(sample_importance)
        theta += gradient*learning_rate
        diff = norm(gradient,np.zeros(l_feature))
        counter += 1
    return theta

