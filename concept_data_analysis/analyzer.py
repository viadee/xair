# imports

import numpy as np
import skfuzzy as fuzz
from scipy.stats import skew
import os
from alibi.utils.discretizer import Discretizer
from alibi.datasets import fetch_adult
import pandas as pd
import helper as h

import matplotlib.pyplot as plt

percentiles = np.arange(10, 110, 10)


def get_stats_from_corrs(global_corrs, corr_mf, x_corr, save=None):
    '''
        Get statistics from global gk correlation values

        @param global_corrs: Global gk correlation values
        @param corr_mf: Correlation membership function
        @param corr_x: Universe of discourse of correlation
        @param save: Save figure to png (current directory), if one is given
    '''


    print("Global Correlation values:")
    print([np.around(g,3) for g in global_corrs])
    corr_mems = h.get_mems(corr_mf,x_corr, [(c*100) for c in global_corrs])
    
    '''
    print("--"*50)
    print("Memberships per Membership function")
    print("--"*50)
    
    mem_c = 0
    for mem_c in range(len(rating_5)):
        print("Membership ", rating_5[mem_c])
        sum_mem = 0
        for c,mems in corr_mems.items():
            if mems[mem_c] > 0:
                print("    {}: {}".format(c,  np.around(mems[mem_c],3)))
                sum_mem += mems[mem_c]
        print(" --> Sum: ", np.around(sum_mem,3))
    '''  
        
    corr_dist,corr_degree = h.get_features_per_mem(corr_mems)
    _,corr_degree_exact = h.get_features_per_mem_exact(corr_mems)

    #print("--"*50)
    print("Number of features per membership: \n   ",corr_degree )
    print("Exact number of features per membership: \n   ",{k: np.around(v,3) for k,v in corr_degree_exact.items()} )
    #print("--"*50)
    plt.bar(range(len(corr_degree_exact)), list(corr_degree_exact.values()), align='center')
    plt.xticks(range(len(corr_degree_exact)), list(corr_degree_exact.keys()))
    plt.ylabel("Summe der Zugehörigkeitswerte")
    plt.xlabel("Zugehörigkeitsfunktion")
    
    if save:
        plt.savefig(os.path.join("./{}.png".format(save)),dpi=300)   


def get_global_corr(global_corrs,corr_mf, x_corr, verbose=False):
    '''
        Get global correlation of global PhiK correlation values

        @param global_corrs: Global gk correlation values
        @param corr_mf: Correlation membership function
        @param corr_x: Universe of discourse of correlation
        @return exact correlation value, dict of all fuzzy memberships of exact correlation value
    '''
    
    mean = np.mean(global_corrs)
    mad = h.calc_mad(global_corrs)

    corr_prop_mad = np.around((mean+(mad/2)),3)
    corr_prop_mems_mad= h.get_all_memberships(corr_mf,x_corr,(corr_prop_mad * 100))

    if verbose:
        print("--"*50)
        get_stats_from_corrs(global_corrs,corr_mf, x_corr)

        print("Mean: ", np.around(mean,3))
        print("MAD: ",np.around(mad,3))

        corr_prop_old = np.around((mean+(mad)),3)
        corr_prop_mems_mad_old= h.get_all_memberships(corr_mf,x_corr,(corr_prop_old * 100))
        print("--- Mean + MAD: ")
        print(f"    Value to fuzzify: {corr_prop_old},  membership values: {[c for c,v in corr_prop_mems_mad_old.items()if v > 0]}") 
        print("--"*50)


        print("--- Mean + MAD/2: ")
        print(f"    Value to fuzzify: {corr_prop_mad},  membership values: {[c for c,v in corr_prop_mems_mad.items()if v > 0]}") 


    return corr_prop_mad, corr_prop_mems_mad
    


def get_discr_stats(data, feature_names,skip_empty = False, verbose = False):
    '''
        @param data: Dataset with numerical features
        @param feature_names: Names of features
        @param skip_empty: If true, only return discretizability values of features with non-empty bins
        @param verbose: Print statements

        @return List of MADs per feature, Discretizer of data
    '''
    
    # Prepare discretizer
    # make discretizer using Alibi implementation (used within suggested Anchors and CFProto implementation)
    # treat everything as numerical feat
    disc = Discretizer(
            data,
            numerical_features=np.arange(0,len(feature_names),1),
            feature_names=feature_names,
            percentiles=percentiles
        )
    
    # List with bin values for each feature that is discretized
    bins = disc.bins(data)

    contains_empty = []
    mads = []

    for idx,(n,b) in enumerate(zip(feature_names,bins)):

        if skip_empty and  len(b) > len(set(b)):
            #print(b,"   --> contains more than one equal bin edges")
            contains_empty.append(True)
        else:
            # Relation of biggest bin
            # add min value to list and sort
            minv = data[:,idx].min()
            rangev = b[-1]-minv
            b= np.append(b,minv)
            b.sort()
            
            # calculate differences
            widths = []
            for i in range(0,len(b)-1):
                widths.append(np.around(b[i+1]- b[i],3))

            width_props = [np.around(d/rangev,3) for d in widths]

            if verbose:
                # calc metrics on normal widths
                mean = np.mean(widths)
                mad = h.calc_mad(widths)
                
                print(n)
                print("  bin edges: ")
                print("  ",np.around(b,3))
                
                print("  Bin widths:\n  ",widths)

                print("-"*20)
                print("  Mean Widths: ", np.around(mean,3))
                print("  MAD Widths: ",np.around(mad,3))
                print("-"*20)

            # calc metrics on width_props
            mean = np.mean(width_props)
            mad = h.calc_mad(width_props)
            mads.append(np.around(mad,3))
            
            if verbose:
                print("  Bin width props:\n  ",width_props)
                print("  Mean Width Proportions: ", np.around(mean,3))
                print("  MAD Width Proportions: ",np.around(mad,4))

            widths.sort(reverse=True)

            # check for empty bins
            contains_empty.append(True) if 0.0 in widths else contains_empty.append(False)

                
    return mads, disc



def get_global_discr_from_mads(mads,universe,mems, verbose=False):
    '''
       Aggregate feature MADs to final discretizability value of dataset

        @param mads: MADs of difference of optimal bin width to actual bins representing a feature discretizability
        @param universe: Universe of discourse of discretizability
        @param mems: Discretizability membership function
        @param verbose: Print statements

        @return exact discretizability value of dataset, dict of fuzzy memberships of exact discretizability
    '''

    # The discretizability is determined by subtracting the MAD from the optimal bin width.
    # If the MAD is greater than 0.1, the resulting value is negative, indicating the existence of very large 
    # width differences. In this case, there is at least one very large bin that greatly reduces the width of the others.
    # The higher this value is, the better the discretizability of the feature.

    # scale to fit universe
    mads = [(10-m*100) for m in mads]
    mean = np.mean(mads)
    mad = h.calc_mad(mads)
    
    prop_mad = np.around((mean+(mad/2)),3)
    mems_mad = h.get_all_membership_values(universe,mems,(prop_mad ))
    
    if verbose:
        print(mads)
        print("Mean: ", np.around(mean,3))
        print("MAD: ",np.around(mad,3))

        prop_mad_old = np.around((mean+(mad)),3)
        print("Prop MAD: ", prop_mad_old)
        mems_mad_old = h.get_all_membership_values(universe,mems,(prop_mad_old ))
        print(" Value to fuzzify (Mean + MAD): ",mems_mad_old) 
        print("  --> Fuzzification of ",[c for c,v in mems_mad_old.items() if v >= 0.5] )
        print("-"*50)      
        print("Prop MAD/2: ", prop_mad)
        print(" Value to fuzzify (Mean + MAD/2): ",mems_mad) 
        print("  --> Fuzzification of ",[c for c,v in mems_mad.items() if v >= 0.5] )
        print("-"*50)
    
    return prop_mad, mems_mad

def get_global_discr(data, feature_names,universe,mems, verbose=False):
    '''
        Get discretizability value of dataset of features that are considered numerically
        @param data: Dataset with numerical features
        @param feature_names: Names of features
        @param universe: Universe of discourse of discretizability
        @param mems: Discretizability membership function
        @param verbose: Print statements

        @return exact discretizability value of dataset, dict of fuzzy memberships of exact discretizability
    '''
    
    mads, _ = get_discr_stats(data, feature_names,verbose=False)
    return get_global_discr_from_mads(mads,universe,mems, verbose=verbose)
    
