import matplotlib.pyplot as plt
from fetch_data import fetch_light_curve, parse_args

def clean_light_curve(lc):
    """ Remove long term trends from the light curve, 
        leaving behind features such like transits """
    lc_clean = lc.remove_nans()

    lc_flat = lc_clean.flatten()

    return lc_flat

def plot_flat(lc_flat):
    """ Plot the flattened light curve """
    lc_flat.plot()

if __name__ == "__main__":
    args = parse_args()
    lc = fetch_light_curve(args.target)
    lc_flat = clean_light_curve(lc)
    plot_flat(lc_flat)
    plt.show()
    
