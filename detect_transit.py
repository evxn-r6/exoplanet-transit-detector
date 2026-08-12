import numpy as np
import matplotlib.pyplot as plt
from fetch_data import fetch_light_curve, parse_args
from clean_data import clean_light_curve

def find_best_period(lc_flat):
    """ Run a Box Least Squares search to find the most likely
        orbital period of a transisting planet.
        
        Define a range of periods to search over, in days """
    period_grid = np.linspace(0.5, 5, 10000)

    bls = lc_flat.to_periodogram(method="bls", period=period_grid)

    best_period = bls.period_at_max_power

    return bls, best_period

def plot_periodogram(bls):
    """ Plot BLS power against trial period - peaks indicate
        likely orbital periods """
    bls.plot()

def plot_folded_transit(lc_flat, best_period):
    """ 'Fold' the light curve at the best period, stack every orbit
        on top of each other so the transit becomes clear """
    lc_flat.fold(period=best_period).scatter()

if __name__ == "__main__":
    args = parse_args()
    lc = fetch_light_curve(args.target)
    lc_flat = clean_light_curve(lc)

    bls, best_period = find_best_period(lc_flat)
    print(f"Best-fit period: {best_period}")

    plot_periodogram(bls)
    plt.show()

    plot_folded_transit(lc_flat, best_period)
    plt.show()