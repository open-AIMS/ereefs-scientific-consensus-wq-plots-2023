# Copyright Eric Lawrey, Australian Institute of Marine Science
# This script creates an annual aggregate for all the BGC variables of interest. This 
# date range is limited so that only whole years are included.
import xarray as xr
import os

# Load the data
ds = xr.open_dataset('src-data/eReefs-BGC/GBR4_H2p0_B3p1_Cq3b_Dhnd_WQ_monthly_3.0m.nc')

# Filter dataset to include only data from January 2011 to December 2018. In this way
# the averages occur only over full years. This will mean there is no seasonal bias.
ds = ds.sel(time=slice('2011-01-01', '2018-12-31'))

destination_folder = os.path.join('derived','eReefs-BGC')

# List of variables
variables = ['TN', 'TP', 'DIN', 'DIP', 'Chl_a_sum', 'NO3', 'NH4', 'DOR_N', 'DOR_P', 
             'PhyL_N', 'PhyL_NR', 'PhyS_N', 'PhyS_NR', 'Tricho_N', 'Tricho_NR']

averages = {}

# Compute the time average for each variable
for var in variables:
    print(f"Processing variable: {var}...")
    averages[var] = ds[var].mean(dim='time')

# Create a new dataset with the averages
averaged_ds = xr.Dataset(averages)

if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        
# Save the result to a new NetCDF file
output_file = os.path.join(destination_folder, 'GBR4_H2p0_B3p1_Cq3b_Dhnd_WQ_all_3.0m_Jan2011-Dec2018.nc')
averaged_ds.to_netcdf(output_file)

print(f"\nTime-averaged data saved to {output_file}")
