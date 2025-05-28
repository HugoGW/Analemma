# Analemma Simulation and Image Overlay

This project simulates the **analemma**—the figure-eight-shaped path the Sun traces in the sky when observed at the same time every day over the course of a year. The code overlays this simulated path onto real photographs taken from specific locations to compare the theoretical prediction with observational data.

## Overview

An **analemma** results from two main astronomical effects:

* **Axial tilt** (obliquity): The Earth's axis is tilted \~23.5° relative to its orbital plane.
* **Orbital eccentricity**: The Earth's orbit around the Sun is elliptical, not perfectly circular.

Because of these, the solar time and the Sun's apparent position in the sky vary throughout the year, even at the same clock time each day. When plotted, the solar position at a fixed time forms a figure-eight curve.

This project provides both:

* A simulation of the analemma using astronomical computation.
* A visual comparison by overlaying the simulation on real photos from:

  * Tehran
  * Buenos Aires
  * Antarctica

---

## Project Structure

The main Python script is `analemma.py`, which is structured into three main parts:

### 1. **Time and Location Setup**

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, get_body
```

* Uses `Astropy` to handle time and Earth coordinates.
* The function `loc_time(location, year, month, day, hour)` generates:

  * A `Time` array spanning one year.
  * The observer's `EarthLocation` using a string address.
  * An `AltAz` frame for computing the apparent position of celestial objects.

**Purpose**: This sets up the temporal and spatial context needed for accurate solar position calculations.

### 2. **Solar Position Calculation**

```python
sun = get_body("sun", time=time).transform_to(frame)
alt = sun.alt.deg
az = sun.az.deg
```

* Computes the Sun’s apparent position (`altitude` and `azimuth`) for each day of the year.
* Uses `astropy.coordinates.get_body()` to get solar coordinates and converts them to the horizontal coordinate system.

**Key Physical Quantities**:

* **Altitude (Alt)**: Angle above the horizon (0° = horizon, 90° = zenith).
* **Azimuth (Az)**: Cardinal direction (0° = North, 90° = East, etc.).

### 3. **Visualization and Image Overlay**

```python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
```

* Plots the computed analemma using `Matplotlib` and `Cartopy` for geographic and celestial projections.
* An orthographic projection is used, centered on the mean position of the Sun.

If `superposition=True` and the corresponding image file is available, the code:

* Loads a background image (e.g., a real photo of the analemma).
* Aligns the simulated curve over the photo with scaling and offset adjustments.
* Plots the solar path in red on top of the image.

If no image is provided, a simple figure of the solar path is plotted using a coordinate grid.

---

## Example Outputs

Below are comparisons of the simulated analemma with real photos:

### 📍 Buenos Aires

Simulated analemma (red curve) overlaid on a photo taken in Buenos Aires.

![Buenos Aires](https://github.com/user-attachments/assets/65d41964-a078-4cae-becb-8d02d84c2c8d)

---

### 📍 Tehran

Comparison of simulated and observed analemma in Tehran.

![Tehran](https://github.com/user-attachments/assets/412534df-31b8-403c-a041-ae43e5101327)

---

### 📍 Antarctica

An exceptional analemma at high latitudes.

![Antarctica](https://github.com/user-attachments/assets/f9b5f283-4022-43c0-8830-06d0206ebde9)

---

### 📈 Pure Simulation

Analemma without any photographic background.

![Simulated Analemma](https://github.com/user-attachments/assets/8124cb81-d19a-4b72-acc9-489e2f9cd649)

---

## Requirements

Install the following Python packages:

```bash
pip install numpy matplotlib astropy cartopy
```

## Parameters and Customization

You can modify the following parameters in the script:

```python
Location = "Buenos Aires"  # Observer's location
year = 2013
month = "Jan"
day = 12
hour = "00:28"              # Local observation time
superposition = True        # Overlay photo or not
image_filename = "Analemma_argentina.jpg"
```

To simulate the analemma for another location or time:

* Change the `Location` to any address (e.g., "Paris", "Tokyo", etc.).
* Adjust the `month`, `day`, and `hour` to the desired daily observation time.
* Provide a matching photo if available for overlay.

---

## Notes

* The simulation assumes local solar noon is aligned with the provided time. Any time offset from solar noon can cause the analemma to appear tilted or displaced.
* Earth's motion is modeled using high-precision ephemerides provided by Astropy, ensuring realistic Sun positions.

---

## License

This project is provided under the MIT License.

---

## Acknowledgements

* **Astropy**: For celestial mechanics and coordinate transformations.
* **Cartopy**: For geographic projections.
* **Matplotlib**: For visualization.
* Real photos of analemmas used here were taken by skilled astrophotographers and sourced for educational comparison.

---

Let me know if you'd like a `requirements.txt`, a command-line version of the script, or additional Markdown badges or sections like "How to contribute".


