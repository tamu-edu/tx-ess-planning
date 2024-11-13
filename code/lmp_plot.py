import matplotlib.pyplot as plt
import pandas as pd
import os

# Define paths
data_release_path = '../data_release'
data_source_path = '../data_source'

# Load map and node data
map_img = plt.imread(os.path.join(data_release_path, 'Texas_Plain_600x600.png'))
node_df = pd.read_csv(os.path.join(data_release_path, 'nodes_coordinates.csv'))

# Define the year
year = '2022'  # yyyy

# Load LMP data
lmp = pd.read_csv(os.path.join(data_source_path, 'lmp', f'nodes_{year}.csv'))

# Define date, and time prefix
date = '07/25'  # mm/dd
time = '17:35'  # hh:mm
datetime_prefix = f'{date}/{year} {time}'

# Find a column that starts with the specified datetime prefix
datetime_column = next((col for col in lmp.columns if col.startswith(datetime_prefix)), None)

if datetime_column:
    # Merge LMP data with node coordinates and flip Y-axis
    node_coordinates = node_df.merge(lmp[['SettlementPoint', datetime_column]],
                                     left_on='Node', right_on='SettlementPoint')

    # Plot map and data
    plt.imshow(map_img, extent=[0, 600, 0, 600])
    scatter = plt.scatter(node_coordinates['x'], node_coordinates['y'],
                          c=node_coordinates[datetime_column], cmap='turbo', s=10)
    
    # Create colorbar and set font sizes
    cbar = plt.colorbar(scatter)
    cbar.set_label('LMP ($/MWh)', fontsize=18)
    cbar.ax.tick_params(labelsize=18)

    # Remove square outline by hiding spines
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    cbar.outline.set_visible(False)  # Hide the colorbar outline
    
    plt.xticks([])
    plt.yticks([])
    # plt.title(f'LMP Values for {datetime_prefix}')
    plt.tight_layout()
    plt.show()
else:
    print(f"No column found starting with '{datetime_prefix}' in the data.")