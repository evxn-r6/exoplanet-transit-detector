import matplotlib.pyplot as plt
import lightkurve as lk
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Exoplanet transit detection")
    parser.add_argument("--target", type=str, default="Kepler-10",
                        help="Name of the target star to search (e.g 'Kepler-10)")
    return parser.parse_args()

def fetch_light_curve(target_name):
    """ Search and download a light curve for the given target star """
    search_result = lk.search_lightcurve(target_name, mission="Kepler")
    print(search_result)

    lc = search_result[4].download()
    return lc

def plot_raw(lc):
    """ Plot the raw light curve: time vs flux """
    lc.plot()

if __name__ == "__main__":
    args = parse_args()
    lc = fetch_light_curve(args.target)
    plot_raw(lc)
    plt.show()