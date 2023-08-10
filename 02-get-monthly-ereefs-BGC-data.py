# Copyright Eric Lawrey, Australian Institute of Marine Science
# This script downloads the eReefs BGC data from the AIMS THREDDS data service 
# using OpenDAP. It saves the data as a local NetCDF file for later processing.
# 
import xarray as xr
import os
import sys

# OpenDAP URL
url = "https://thredds.ereefs.aims.gov.au/thredds/dodsC/GBR4_H2p0_B3p1_Cq3b_Dhnd/monthly.nc"

destination_folder = os.path.join("src-data", "eReefs-BGC")

depth = -3.0

# For reference (GBR4)
gbr4_depth_to_k_table = {
    -0.5: 16,
    -1.5: 15,
    -3.0: 14,
    -5.55: 13,
    -8.8: 12,
    -12.75: 11,
    -17.75: 10,
    -23.75: 9,
    -31.0: 8,
    -39.5: 7,
    -49.0: 6,
    -60.0: 5,
    -73.0: 4,
    -88.0: 3,
    -103.0: 2,
    -120.0: 1,
    -145.0: 0
}

k = gbr4_depth_to_k_table.get(depth, None)
if k is None:
    print(f"Depth {depth_value} not found in the lookup table.")
    sys.exit(1)
    
print("Opening the remote dataset...")
# Open the dataset
ds = xr.open_dataset(url)

# List of desired variables
variables = ['TN', 'TP', 'DIN', 'DIP', 'Chl_a_sum', 'NO3', 'NH4', 'DOR_N', 'DOR_P', 
             'PhyL_N', 'PhyL_NR', 'PhyS_N', 'PhyS_NR', 'Tricho_N', 'Tricho_NR']

if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
filename = os.path.join(destination_folder,f'GBR4_H2p0_B3p1_Cq3b_Dhnd_WQ_monthly_{abs(depth)}m.nc')

print("Downloading data from OpenDAP service. This will take about 30 min.")

# Download each variable at a time so we can provide some feedback on the process
ds[[]].to_netcdf(filename, mode='w')  # This creates an empty NetCDF with the same coordinates/dimensions

for var in variables:
    print(f"Fetching data for {var} at depth k={depth}...")
    subset = ds[var].sel(k=k)
    
    print(f"Saving data for {var} to {filename}...")
    subset.to_netcdf(filename, mode='a')  # Append mode, to add data to the existing NetCDF

    print(f"Data for {var} saved successfully!")

print("All data extraction and saving completed!")