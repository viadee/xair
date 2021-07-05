# imports

import numpy as np
import skfuzzy as fuzz
from scipy.stats import skew
import os
from alibi.utils.discretizer import Discretizer
from alibi.datasets import fetch_adult
import pandas as pd

import matplotlib.pyplot as plt

## Some variables and helper functions

rating_5 = ["VL","L","M","H","VH"]
rating_3 = ["L", "M", "H"]
rating_2 = ["No", "Yes"]

all_ratings = [rating_2, rating_3, rating_5]

# memberhsip values
mems_corr_unscaled = [[0.0,0.0,0.2,0.3],
                [0.2,0.3,0.4,0.5],
                [0.4,0.5,0.6,0.7],
                [0.6,0.7,0.8,0.9],
                [0.8,0.9,1,1]]


def plot_memberships(universe,mem_funcs,mem_names=["L","M","H"],colors = ["b", "g", "r", "y", "m"],figsize=(8,4), save=None):
    f = plt.figure(figsize=figsize)
    ax = f.add_subplot(111)
    # universe, membership function, color
    for mem,label,color in zip(mem_funcs, mem_names, colors):
        ax.plot(universe, mem, color, linewidth=1.5, label=label)

    # Hide the right and top spines
    #ax.spines['right'].set_visible(False)
    #ax.spines['top'].set_visible(False)

    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.ylabel('Zugehörigkeitswert')
    plt.xlabel('Diskursuniversum')


    #ax.set_title(self.name)
    #ax.legend(loc=2)
    ax.legend()
    
    if save:
        plt.savefig(f"./{save}.png",dpi=300)
        
        
def plot_distribution(feat, name, legend,figsize=(9,6), savedir=None):
    f = plt.figure(figsize=figsize)
    ax = f.add_subplot(111)
    plt.hist(feat)

    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    ax.xaxis.labelpad = 15
    ax.yaxis.labelpad = 15

    plt.ylabel('Anzahl')
    plt.xlabel(legend)
    
    if savedir is not None:
        plt.tight_layout()
        plt.savefig(os.path.join(savedir,"{}.png".format(name)),dpi=300)
        
def get_mems(mem_funcs, universe,vals):
    '''
        @param mem_vals: membership functions of feature
        @param universe: universe of feature
        @vals: values to determine memberships
        returns: Dict of membership degrees per feature
    '''
    mems = {}
    add = 0
    if type(vals) != dict:
        global_vals = {}
        for i,c in enumerate(vals):
            # create dict
            global_vals[i] = c
    else:
        global_vals = vals
        
    for label,val in global_vals.items():
        mems[label] = [fuzz.interp_membership(universe, m, val) for m in mem_funcs]
        add += val
    return mems

def get_all_memberships(memberships,universe, val, labels=None):
    '''
        Returns the memberships of the given value 

        @param universe: universe of feature
        @param memberships: memberships of feature
        @param val: value to determine memberships (has to be scaled to 100)
        @param labels: labels for returned membership dict (optional)
    '''
    if labels is not None:
        rating = labels
    else:
        rating = [r for r in all_ratings if len(r) == len(memberships)][0]

    mems = {}
    for idx,m in enumerate(memberships):
        mems[rating[idx]] = np.around(fuzz.interp_membership(universe, m, val),3)
    return mems

def get_features_per_mem(mem_vals,labels=None):
    '''
        @param mem_vals: dict of membership values per feature
        returns: 
            - Features sorted by Rating 
            - Dict of number of features per rating
    '''
    
    # get labels
    rating = labels if labels is not None else [r for r in all_ratings if len(r) == len(list(mem_vals.values())[0])][0]

    crisp_ratings = {}
    r_nums = {}
    for ri,rating in enumerate(rating):
        crisp_ratings[rating] = [n for n,v in mem_vals.items() if v[ri] > 0]
        r_nums[rating] = len(crisp_ratings[rating])
    return crisp_ratings,r_nums

def get_features_per_mem_exact(mem_vals,labels=None):
    '''
        @param mem_vals: dict of membership values per feature
        returns: 
            - Features sorted by Rating 
            - Dict of number of features per rating
    '''
    rating = labels if labels is not None else [r for r in all_ratings if len(r) == len(list(mem_vals.values())[0])][0]

    crisp_ratings = {}
    for ri,rating in enumerate(rating):
        crisp_ratings[rating] = [n for n,v in mem_vals.items() if v[ri] > 0]

    r_nums = {}
    c = 0
    for rating,(idx,val) in zip(crisp_ratings.keys(),enumerate(crisp_ratings.values())):
        for v in val:
            c += mem_vals[v][idx]
        r_nums[rating] = c
        c = 0                                 
    
    return crisp_ratings,r_nums

def get_all_membership_values(universe, memberships, val, rating=["L","M","H"]):
    mems = {}
    for idx,m in enumerate(memberships):
        mems[rating[idx]] = np.around(fuzz.interp_membership(universe, m, val),3)
    return mems

def calc_mad(data, axis=None):
    return np.mean(np.absolute(data - np.mean(data, axis)), axis)