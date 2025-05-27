import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.time
import astropy.coordinates
import cartopy.crs as ccrs

# Function to define the observation time and location
def loc_time(location, year, month, day, hour):
    # Convert month name (e.g., "Jan") to integer if needed
    if isinstance(month, str):
        month = month.strip()[:3].title()
        months = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6,
                  "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
        if month not in months:
            raise ValueError(f"Invalid month name: {month}")
        month = months[month]

    # Format the hour string (e.g., "13:00")
    hour_str = hour if isinstance(hour, str) else f"{int(hour):02d}:00"
    time_str = f"{year}-{month:02d}-{day:02d}T{hour_str}"

    # Create a time array covering one year from the input time
    time = astropy.time.Time(time_str) + np.arange(365) * u.day

    # Convert location string to EarthLocation
    location = astropy.coordinates.EarthLocation.of_address(location)

    # Create the AltAz frame for the full year
    frame = astropy.coordinates.AltAz(obstime=time, location=location)
    return time, location, frame

# ----------------------------
# PARAMETERS TO CUSTOMIZE
# ----------------------------
Location = "Buenos Aires"                   # Observer's location
year = 2013                                 # Start year
month = "Jan"                               # Start month
day = 12                                    # Start day
hour = "00:28"                              # Local time at start
superposition = True                        # Whether to overlay an image
image_filename = "Analemma_argentina.jpg"   # Image to overlay (if exists)

# Get the Sun's position over the year
time, location, frame = loc_time(Location, year, month, day, hour)
sun = astropy.coordinates.get_body("sun", time=time).transform_to(frame)
alt = sun.alt.deg   # Altitude of the Sun (degrees)
az = sun.az.deg     # Azimuth of the Sun (degrees)

# Use orthographic projection centered on the mean Sun position
projection = ccrs.Orthographic(az.mean(), alt.mean())

# ----------------------------
# PLOT WITH IMAGE OVERLAY
# ----------------------------
if superposition:
    try:
        # Try to read the image file
        img = plt.imread(image_filename)

        # Create the main figure and axis with projection
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=projection, facecolor='none')

        # Define the extent of the sky view
        buffer_az = 1
        buffer_alt = 1
        az_min, az_max = az.min() - buffer_az, az.max() + buffer_az
        alt_min, alt_max = alt.min() - buffer_alt, alt.max() + buffer_alt
        ax.set_extent([az_min, az_max, alt_min, alt_max], crs=ccrs.PlateCarree())
        ax.set_zorder(1)  # Keep it above background image

        # Get the position and size of the plot for background image placement
        bbox = ax.get_position()
        left, bottom, width, height = bbox.x0, bbox.y0, bbox.width, bbox.height

        # Adjust background image size and offset
        offset_left = 0.09
        offset_bottom = 0
        zoom_factor = 1.16

        # Add image as background
        ax_img = fig.add_axes([
            left - offset_left,
            bottom - offset_bottom,
            width * zoom_factor,
            height * zoom_factor
        ], frameon=False)
        ax_img.imshow(img, aspect='auto')
        ax_img.set_xticks([])
        ax_img.set_yticks([])
        ax_img.set_zorder(0)  # Draw behind the plot

        # Plot the Sun path on top of the image
        ax.plot(az, alt, transform=ccrs.PlateCarree(), color="red", linewidth=2, label="Sun path")
        ax.gridlines(draw_labels=True)
        plt.title(f"Apparent Path of the Sun (Seen from {Location})")
        plt.legend()
        plt.show()

    except FileNotFoundError:
        # If the image file is missing, only print a message (no plot)
        print("⚠️ Image not found.")

# ----------------------------
# PLOT WITHOUT IMAGE OVERLAY
# ----------------------------
else:
    # Create figure and sky plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=projection, facecolor='none')
    ax.plot(az, alt, transform=ccrs.PlateCarree(), color="red", linewidth=2, label="Sun path")
    ax.gridlines(draw_labels=True)
    plt.title(f"Apparent Path of the Sun (Seen from {Location})")
    plt.legend()
    plt.show()
