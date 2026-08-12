# Exoplanet Transit Detector
A Python pipeline that detects exoplanets transits from Kepler mission light curve data and estimates the planet's physical properties.

## What it does 
Once given a name of a Kepler target star, the pipeline:
1. Fetches real light curve data from the Kepler mission archive (via ```lightkurve```)
2. Cleans the data by removing missing values and flattens out long-term stellar trends
3. Detects periodic transit signals using a Box Least Squares (BLS) periodogram search and phase-folds the light curve to reveal the transit shape
4. Estimates the planet's radius and semi-major axis from the transit depth and period, while also using transit geometry and Kepler's Third Law

## Example Result: Kepler-10 b
Run on a single 9-day quarter of long-cadence Kepler data for Kepler-10:

| Quantity | Detected | Published Value |
| --- | --- | --- |
| Orbital Period | 0.838 days | 0.8375 days |
| Planet Radius | 1.61 Earth radii | ~1.47 Earth radii | 
| Semi-major axis | 0.0169 AU | ~0.017 AU | 

The period and semi-major axis match published values closely. The radius estimate is within 10%, this is likely due to **limb darkening**: real stars are dimmer at the edge of their visible disc than the centre, which softens the sharp "box" shape assumed by the BLS method. Averaging flux over an in-transit window (rather than taking a single minimum point) noticeably improved the estimate from an initial 1.94 to 1.61 Earth radii.

## Example Result: Kepler-8 b
To check the pipeline works beyond just one star, it was also run on Kepler-8, a known hot Jupiter. The period detection and transit depth both came back consistent with a real, much larger planet but the estimated radius was measurably off since the stellar parameters (radius, mass) are currently hardcoded for Kepler-10 rather than looked up per target.

## How to run it
``` ruby 
pip install -r requirements.txt

python fetch_data.py --target "Kepler-10"
python clean_data.py --target "Kepler-10"
python detect_transit.py --target "Kepler-10"
python estimate_properties.py --target "Kepler-10"
```
Each script can be run independently. ``` --target ``` accepts any valid Kepler input, catalog name or star name recognised by ```lightkurve```'s search.

## Known Limitations
- **Stellar paraments are hardcoded for Kepler-10** Running on another target still detects the correct period and transit depth, but the radius/semi-major axis estimates will be physically incorrect unless the target's real stellar radius/mass are supplied. A future iteration could query these automatically from the NASA Exoplanet Archive via ```astroquery```.
- **No limb darkening correction.** The BLS method and depth measurement assume a simplified "box" transit shape. This is the likely source of the radius overestimate seen for Kepler-10 b.
- **Single quarter of data.** Only one 9-day quarter of Kepler data is used per run. Stitching together multiple quarters would increase the number of observed transits and improve detection confidence.

