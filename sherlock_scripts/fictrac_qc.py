import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import bigbadbrain as bbb

def main(directory):
    fictrac_folder = os.path.join(directory, 'fictrac')
    fictrac_raw = bbb.load_fictrac(fictrac_folder)

    fly = os.path.split(os.path.split(directory)[0])[1]
    expt = os.path.split(directory)[1]
    full_id = fly + ', ' + expt

    resolution = 10 #desired resolution in ms
    expt_len = 1000*30*60
    fps = 50 #of fictrac camera
    behaviors = ['dRotLabY', 'dRotLabZ']
    fictrac = {}
    for behavior in behaviors:
        if behavior == 'dRotLabY': short = 'Y'
        elif behavior == 'dRotLabZ': short = 'Z'
        fictrac[short] = bbb.smooth_and_interp_fictrac(fictrac_raw, fps, resolution, expt_len, behavior)
    xnew = np.arange(0,expt_len,resolution)

    make_2d_hist(fictrac, fictrac_folder, full_id, save=True, fixed_crop=True)
    make_2d_hist(fictrac, fictrac_folder, full_id, save=True, fixed_crop=False)
    make_velocity_trace(fictrac, fictrac_folder, full_id, xnew, save=True)

    return None

def make_2d_hist(fictrac, fictrac_folder, full_id, save=True, fixed_crop=True):
        plt.figure(figsize=(10,10))
        norm = mpl.colors.LogNorm()
        plt.hist2d(fictrac['Y'],fictrac['Z'],bins=100,cmap='Blues',norm=norm);
        plt.ylabel('Rotation, deg/sec')
        plt.xlabel('Forward, mm/sec')
        plt.title('Behavior 2D hist {}'.format(full_id))
        plt.colorbar()
        name = 'fictrac_2d_hist.png'
        if fixed_crop:
            plt.ylim(-400,400)
            plt.xlim(-10,15)
            name = 'fictrac_2d_hist_fixed.png'
        if save:
            fname = os.path.join(fictrac_folder, name)
            plt.savefig(fname,dpi=100,bbox_inches='tight')
            
def make_velocity_trace(fictrac, fictrac_folder, full_id, xnew, save=True):
    plt.figure(figsize=(10,10))
    plt.plot(xnew/1000,fictrac['Y'],color='xkcd:dusk')
    plt.ylabel('forward velocity mm/sec')
    plt.xlabel('time, sec')
    plt.title(full_id)
    if save:
        fname = os.path.join(fictrac_folder, 'velocity_trace.png')
        plt.savefig(fname,dpi=100,bbox_inches='tight')

if __name__ == '__main__':
    main(sys.argv[1])
