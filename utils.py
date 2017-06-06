"""
utility functons
"""

from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection
from matplotlib import cm 
import numpy as np

__all__=['s_mu_tpcf_patches']
__author__=['Duncan Campbell']

def s_mu_tpcf_patches(tpcf, s_bins, mu_bins, cmap=cm.cool, vmin=None, vmax=None):
    """
    Return a collection of patches that can be used to plot the tpcf in s and mu bins.
    
    Parameters
    ----------
    tcpf : np.array
        numpy array with dimension len(s_bins) by len(mu_bins).
        This is the output of tpcf_s_mu()
    
    s_bins : np.array
        numpy array of shape (num_s_bin_edges, ) storing the :math:`s`
        boundaries defining the bins in which pairs are counted.
    
    mu_bins : np.array
        numpy array of shape (num_mu_bin_edges, ) storing the
        :math:`\cos(\theta_{\rm LOS})` boundaries defining the bins in
        which pairs are counted. All values must be between [0,1].
    
    cmap : matplotlib.colors.LinearSegmentedColormap object
        color map to use for coloring the patches
    
    vmin : float
        minimum value of tpcf used to normalize luminance data. Default is min(tpcf).
    
    vmax : float
        maximum value of tpcf used to normalize luminance data. Default is max(tpcf).
    
    Returns
    -------
    p : matplotlib.collections.PatchCollection object
        collection of patches
    
    Example
    -------
    For demonstration purposes we create a randomly distributed set of points within a
    periodic cube of length 250 Mpc/h.
    
    >>> Npts = 100
    >>> Lbox = 250.
    >>> x = np.random.uniform(0, Lbox, Npts)
    >>> y = np.random.uniform(0, Lbox, Npts)
    >>> z = np.random.uniform(0, Lbox, Npts)
    
    We transform our *x, y, z* points into the array shape used by the pair-counter by
    taking the transpose of the result of `numpy.vstack`. This boilerplate transformation
    is used throughout the `~halotools.mock_observables` sub-package:
    
    >>> sample1 = np.vstack((x,y,z)).T
    
    First, we calculate the correlation function using
    `~halotools.mock_observables.s_mu_tpcf`.
    
    >>> from halotools.mock_observables import s_mu_tpcf
    >>> s_bins  = np.linspace(0.01, 25, 10)
    >>> mu_bins = np.linspace(0, 1, 15)
    >>> xi_s_mu = s_mu_tpcf(sample1, s_bins, mu_bins, period=Lbox)
    
    Get a collection of patches taht represent the tpcf in s and mu bins:
    
    >>> p = s_mu_tpcf_patches(xi_s_mu, s_bins, mu_bins)
    
    Now, you can plot the tpcf:
    
    >>> fig, ax = plt.subplots()
    >>> ax.add_collection(p)
    >>> ax.set_xlim([0,25])
    >>> ax.set_ylim([0,25])
    >>> plt.show()
    """
    
    #normalize tpcf
    if vmin is None:
        min_tpcf = 1.0*np.min(tpcf)
    else:
        min_tpcf = vmin
        
    if vmax is None:
        max_tpcf = 1.0*np.max(tpcf)
    else:
        max_tpcf = vmax
    
    #set values over and under the vmin and vmax values
    mask = (tpcf>max_tpcf)
    tpcf[mask] = max_tpcf
    mask = (tpcf<min_tpcf)
    tpcf[mask] = min_tpcf
    
    #create lists to store wedges and color
    wedges = []
    colors=[]
    
    #set center of wedges to be the origin
    center = (0.0,0.0)
    
    #convert to degrees
    theta_bins = np.degrees(np.arccos(mu_bins))
    
    #change convention to start theta=0.0 on the positive x-axis
    #instead of the positive y-axis as is the theta_LOS convention
    theta_bins = 90.0 - theta_bins
    
    #loop over s bins
    for i, (s_low, s_high) in enumerate(zip(s_bins[:-1], s_bins[1:])):
        
        #loop over mu_bins
        for j, (theta_high, theta_low) in enumerate(zip(theta_bins[:-1], theta_bins[1:])): 
            
            #set radial extent
            r = s_high
            dr = s_high-s_low
            #set angular extent
            theta1 = theta_high
            theta2 = theta_low
            #set color
            c = 1.0*(tpcf[i,j]-min_tpcf)/max_tpcf
            
            #store wedges
            colors.append(c)
            wedges.append(Wedge(center, r, theta1, theta2, width=dr))
    
    #create a collection of patches
    p = PatchCollection(wedges, cmap=cmap)
    colors = np.array(colors)
    p.set_array(colors)
    p.set_linewidth(0.0)
    
    return p