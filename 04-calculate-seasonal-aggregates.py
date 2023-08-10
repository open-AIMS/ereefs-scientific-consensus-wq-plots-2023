# Copyright Eric Lawrey, Australian Institute of Marine Science
# This script generates season aggregates of the eReefs NetCDF BCG data downloaded
# in 02-get-monthly-ereefs-BGC-data.py.
import xarray as xr
import os


# Load the data
ds = xr.open_dataset('src-data/eReefs-BGC/GBR4_H2p0_B3p1_Cq3b_Dhnd_WQ_monthly_3.0m.nc')
destination_folder = os.path.join('derived','eReefs-BGC')

# List of variables
variables = ['TN', 'TP', 'DIN', 'DIP', 'Chl_a_sum', 'NO3', 'NH4', 'DOR_N', 'DOR_P', 
             'PhyL_N', 'PhyL_NR', 'PhyS_N', 'PhyS_NR', 'Tricho_N', 'Tricho_NR']

# Define months for each season
wet_months = [11, 12, 1, 2, 3, 4]
dry_months = [5, 6, 7, 8, 9, 10]

averages_wet = {}
averages_dry = {}

# This time series goes from Dec 2010 to Apr 2019. We need to trim off the start
# since it is only a fraction of a wet season.
ds = ds.sel(time=slice('2011-05-01', None))

# Compute the average for each variable for each season
for var in variables:
    print(f"Processing variable: {var}...")
    
    # Filter data for the wet season and compute average
    wet_data = ds[var].where(ds['time.month'].isin(wet_months), drop=True)
    
    # Print the time slices for the wet season for checking purposes
    if var == variables[0]:
        print("\nWet season time slices for averaging:")
        print(wet_data.time.values)
    
    averages_wet[var] = wet_data.mean(dim='time')
    
    # Filter data for the dry season and compute average
    dry_data = ds[var].where(ds['time.month'].isin(dry_months), drop=True)
    
    # Print the time slices for the dry season for checking purposes
    if var == variables[0]:
        print("\nDry season time slices for averaging:")
        print(dry_data.time.values)
    
    averages_dry[var] = dry_data.mean(dim='time')
    
    print(f"Completed seasonal processing for {var}.")

# Create new datasets with the averages for each season
averaged_ds_wet = xr.Dataset(averages_wet)
averaged_ds_dry = xr.Dataset(averages_dry)


if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        
# Save the results to new NetCDF files
output_file_wet = os.path.join(destination_folder, 'GBR4_H2p0_B3p1_Cq3b_Dhnd_WQ_wet_3.0m_Nov2012-Apr2019.nc')
output_file_dry = os.path.join(destination_folder, 'GBR4_H2p0_B3p1_Cq3b_Dhnd_WQ_dry_3.0m_May2011-Oct2018.nc')

averaged_ds_wet.to_netcdf(output_file_wet)
averaged_ds_dry.to_netcdf(output_file_dry)

print(f"\nWet season data saved to {output_file_wet}")
print(f"Dry season data saved to {output_file_dry}")
