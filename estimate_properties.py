import numpy as np
from fetch_data import fetch_light_curve, parse_args
from clean_data import clean_light_curve
from detect_transit import find_best_period

# Known properties for Kepler-10
star_radius_solar = 1.065  # Units: solar radii
star_mass_solar = 0.913  # Units: solar mass

# Useful conversion constants
solar_radius_to_earth_radius = 109.2  # 1 solar radius = 109.2 Earth radii

def measure_transit_depth(lc_flat, best_period, transit_window=0.02):
    """ Measure the transit depth from the folded light curve, using
        average flux within a window around the minimum transit
        
        transit_window: half-width of the in-transit region, in units
        of phase (0.02 = 2% of the orbital period on either side of the
        deepest point) """
    folded = lc_flat.fold(period=best_period)

    flux = folded.flux.value
    phase = folded.phase.value

    min_phase = phase[np.argmin(flux)]
    in_transit = np.abs(phase - min_phase) < transit_window
    out_of_transit = np.abs(phase - min_phase) > transit_window

    in_transit_flux = np.nanmean(flux[in_transit])
    out_of_transit_flux = np.nanmean(flux[out_of_transit])

    depth = out_of_transit_flux - in_transit_flux

    return depth

def estimate_planet_radius(depth):
    """ Estimate the planet's radius from the transit depth using
        depth = (R_planet / R_star)^2 """
    r_planet_solar = star_radius_solar * np.sqrt(depth)
    r_planet_earth = r_planet_solar * solar_radius_to_earth_radius

    return r_planet_solar, r_planet_earth

def estimate_semi_major_axis(best_period):
    """ Estimate the semi-major axis using Kepler's Third Law 
        a^3 = M_star * P^2  (a in AU, M_star in solar masses, P in
        years) """
    period_years = best_period / 365.25

    a_au = (star_mass_solar * period_years**2) ** (1/3)

    return a_au

if __name__ == "__main__":
    args = parse_args()
    lc = fetch_light_curve(args.target)
    lc_flat = clean_light_curve(lc)
    bls, best_period = find_best_period(lc_flat)

    depth = measure_transit_depth(lc_flat, best_period)
    r_planet_solar, r_planet_earth = estimate_planet_radius(depth)
    a_au = estimate_semi_major_axis(best_period)

    print(f"Transit depth: {depth:.6f}")
    print(f"Planet radius: {r_planet_solar:.4f} solar radii ({r_planet_earth:.2f} Earth radii)")
    print(f"Semi-major axis: {a_au:.4f} AU")