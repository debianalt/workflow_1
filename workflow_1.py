#!/usr/bin/env python
# coding: utf-8

# Data from the WFS service of the ICNF (2024) and Open Street Maps (OSM, 2024). Location of the GXTBR at the borders of Portugal and Spain.
# From OSM database two groups of roads were separated
# group_1 (or minor roads) = ['unclassified', 'living_street', 'pedestrian', 'path', 'steps', 'cycleway']
# group_2 (or major roads) = ['trunk', 'trunk_link', 'residential', 'tertiary', 'tertiary_link', 'secondary', 'primary', 'primary_link', 'secondary_link']
# 

# In[2]:


import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from owslib.wfs import WebFeatureService


wfs_url = 'https://si.icnf.pt/wfs/zonamento_biosfera?service=wfs&version=2.0.0&request=GetCapabilities'
wfs = WebFeatureService(wfs_url)


response = wfs.getfeature(typename=['BDG:zonamento_biosfera'], outputFormat='application/json')
gdf = gpd.read_file(response)
gdf_filtered = gdf[gdf['nome'] == 'Geres']


gdf_filtered = gdf_filtered.to_crs(epsg=4326)


road_network = gpd.read_file('~/Library/CloudStorage/OneDrive-Conicet/portugal database/Portugal Road Network/gx_osm/osmroads.shp').to_crs(epsg=4326)
new_layer = gpd.read_file('~/Library/CloudStorage/OneDrive-Conicet/portugal database/gx/gx/gx.shp').to_crs(epsg=4326)


category_styles = {
    'group_1': {'color': 'blue', 'linewidth': 1.0},
    'group_2': {'color': 'red', 'linewidth': 1.0}
}
group_1 = ['unclassified', 'living_street', 'pedestrian', 'path', 'steps', 'cycleway']
group_2 = ['trunk', 'trunk_link', 'residential', 'tertiary', 'tertiary_link', 'secondary', 'primary', 'primary_link', 'secondary_link']


fig, ax = plt.subplots(figsize=(20, 20))


for zone, color in zip(['Core', 'Buffer', 'Transition'], [(0.0, 0.200, 0.0), (0.0, 0.600, 0.0), (0.500, 0.600, 0.500)]):
    gdf_filtered[gdf_filtered['zone'] == zone].plot(ax=ax, color=color, linewidth=0.5, edgecolor='black', alpha=0.5)

new_layer.boundary.plot(ax=ax, color='black', linewidth=3.0, linestyle='--')
for group, style in category_styles.items():
    roads_in_group = road_network[road_network['highway'].isin(group_1) if group == 'group_1' else road_network['highway'].isin(group_2)]
    roads_in_group.plot(ax=ax, color=style['color'], linewidth=style['linewidth'])


legend_elements = [
    Patch(facecolor=(0.0, 0.200, 0.0), edgecolor='black', label='Core'),  # Elegant Dark Green
    Patch(facecolor=(0.0, 0.600, 0.0), edgecolor='black', label='Buffer'),  # Elegant Medium Green
    Patch(facecolor=(0.500, 0.600, 0.500), edgecolor='black', label='Transition'),  # Elegant Light Green
    Line2D([0], [0], color='black', linewidth=3, linestyle='--', label='GXTBR Borders'),
    Line2D([0], [0], color='blue', linewidth=1, label='Minor Roads (Group 1)'),
    Line2D([0], [0], color='red', linewidth=1, label='Major Roads (Group 2)'),
    Line2D([0], [0], color='white', linewidth=0, label=''),  # Separator
    Line2D([0], [0], color='white', linewidth=0, label='SOURCES: OSM (2024) & ICNF (2024)'),  # Custom text
    Line2D([0], [0], color='white', linewidth=0, label='DATUM: WGS 84, EPSG: 4326')  # Custom text
]


ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.4)


plt.show()


# Other Protected Natural Areas around and within the GXTBR.  
# Sources: OSM (2024), and ICNF (2024)
# 
# From OSM database two groups of roads were separated
# group_1 (or inor roads) = ['unclassified', 'living_street', 'pedestrian', 'path', 'steps', 'cycleway']
# group_2 (or major roads) = ['trunk', 'trunk_link', 'residential', 'tertiary', 'tertiary_link', 'secondary', 'primary', 'primary_link', 'secondary_link']
# 

# In[14]:


import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


road_network = gpd.read_file('~/Library/CloudStorage/OneDrive-Conicet/portugal database/Portugal Road Network/gx_osm/osmroads.shp').to_crs(epsg=4326)
anps_layer = gpd.read_file('~/Library/CloudStorage/OneDrive-Conicet/portugal database/gx/anps (osm)/anps_osm.gpkg').to_crs(epsg=4326)
new_layer = gpd.read_file('~/Library/CloudStorage/OneDrive-Conicet/portugal database/gx/gx/gx.shp').to_crs(epsg=4326)


category_styles = {
    'group_1': {'color': 'blue', 'linewidth': 1.0},
    'group_2': {'color': 'red', 'linewidth': 1.0}
}
group_1 = ['unclassified', 'living_street', 'pedestrian', 'path', 'steps', 'cycleway']
group_2 = ['trunk', 'trunk_link', 'residential', 'tertiary','tertiary_link', 'secondary', 'primary', 'primary_link', 'secondary_link',]



fig, ax = plt.subplots(figsize=(20, 20))

new_layer.boundary.plot(ax=ax, color='black', linewidth=3.0, linestyle='--')  # GXTBR borders
for group, style in category_styles.items():
    roads_in_group = road_network[road_network['highway'].isin(group_1) if group == 'group_1' else road_network['highway'].isin(group_2)]
    roads_in_group.plot(ax=ax, color=style['color'], linewidth=style['linewidth'])




anps_layer.plot(ax=ax, color='green', alpha=0.3)


legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Other Protected Natural Areas'),
    Line2D([0], [0], color='black', linewidth=3, linestyle='--', label='GXTBR Borders'),
    Line2D([0], [0], color='blue', linewidth=1, label='Minor Roads (Group 1)'),
    Line2D([0], [0], color='red', linewidth=1, label='Major Roads (Group 2)'),
    Line2D([0], [0], color='white', linewidth=0, label=''),  # Separator
    Line2D([0], [0], color='white', linewidth=0, label='SOURCES: OSM (2023) & ICNF (2024)'),  # Custom text
    Line2D([0], [0], color='white', linewidth=0, label='DATUM: WGS 84, EPSG: 4326')  # Custom text
]


ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.3)


plt.show()


# Other Protected Natural Areas around and within the GXTBR.  
# Sources: OSM (2024), and ICNF (2024)
# 
# From OSM database two groups of roads were separated
# group_1 (or inor roads) = ['unclassified', 'living_street', 'pedestrian', 'path', 'steps', 'cycleway']
# group_2 (or major roads) = ['trunk', 'trunk_link', 'residential', 'tertiary', 'tertiary_link', 'secondary', 'primary', 'primary_link', 'secondary_link']
# 

# In[18]:


import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from owslib.wfs import WebFeatureService


wfs_url = 'https://si.icnf.pt/wfs/zonamento_biosfera?service=wfs&version=2.0.0&request=GetCapabilities'
wfs = WebFeatureService(wfs_url)


response = wfs.getfeature(typename=['BDG:zonamento_biosfera'], outputFormat='application/json')
gdf = gpd.read_file(response)
gdf_filtered = gdf[gdf['nome'] == 'Geres']


gdf_filtered = gdf_filtered.to_crs(epsg=4326)


road_network = gpd.read_file('~/Library/CloudStorage/OneDrive-Conicet/portugal database/Portugal Road Network/gx_osm/osmroads.shp')
anps_layer = gpd.read_file('~/Library/CloudStorage/OneDrive-Conicet/portugal database/gx/anps (osm)/anps_osm.gpkg')
new_layer = gpd.read_file('~/Library/CloudStorage/OneDrive-Conicet/portugal database/gx/gx/gx.shp')

anps_layer = anps_layer.to_crs(epsg=4326)
new_layer = new_layer.to_crs(epsg=4326)


group_1 = ['trunk', 'trunk_link', 'unclassified', 'tertiary', 'tertiary_link', 'secondary', 'primary', 'primary_link','secondary_link']
group_2 = ['residential','living_street', 'pedestrian', 'path', 'steps', 'cycleway']

category_styles = {
    'group_1': {'color': 'red', 'linewidth': 1.0},
    'group_2': {'color': 'blue', 'linewidth': 1.0}
}


fig, axs = plt.subplots(1, 2, figsize=(20, 10))

for zone, color in zip(['Core', 'Buffer', 'Transition'], [(0, 0, 0), (0.3, 0.3, 0.3), (0.7, 0.7, 0.7)]):
    gdf_filtered[gdf_filtered['zone'] == zone].plot(ax=axs[0], color=color, linewidth=0.5, edgecolor='black', alpha=0.8)

new_layer.boundary.plot(ax=axs[0], color='black', linewidth=3.0, linestyle='--')  # Dashed line for GXTBR borders
for group, style in category_styles.items():
    roads_in_group = road_network[road_network['highway'].isin(group_1) if group == 'group_1' else road_network['highway'].isin(group_2)]
    roads_in_group.plot(ax=axs[0], color=style['color'], linewidth=style['linewidth'])

legend_elements_1 = [
    Patch(facecolor=(0, 0, 0), edgecolor='black', label='Core'),
    Patch(facecolor=(0.3, 0.3, 0.3), edgecolor='black', label='Buffer'),
    Patch(facecolor=(0.7, 0.7, 0.7), edgecolor='black', label='Transition'),
    Line2D([0], [0], color='black', linewidth=3, linestyle='--', label='GXTBR Borders'),  # Dashed line for GXTBR borders
    Line2D([0], [0], color='red', linewidth=1, label='Major Roads (Group 1)'),
    Line2D([0], [0], color='blue', linewidth=1, label='Minor Roads (Group 2)')
]

axs[0].legend(handles=legend_elements_1, loc='upper left', fontsize=10, framealpha=0.4)

anps_layer.plot(ax=axs[1], color='green', alpha=0.5)
new_layer.boundary.plot(ax=axs[1], color='black', linewidth=3.0, linestyle='--')  # Dashed line for GXTBR borders
for group, style in category_styles.items():
    roads_in_group = road_network[road_network['highway'].isin(group_1) if group == 'group_1' else road_network['highway'].isin(group_2)]
    roads_in_group.plot(ax=axs[1], color=style['color'], linewidth=style['linewidth'])

legend_elements_2 = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Other Protected Natural Areas'),
    Line2D([0], [0], color='black', linewidth=3, linestyle='--', label='GXTBR Borders'),  # Dashed line for GXTBR borders
    Line2D([0], [0], color='red', linewidth=1, label='Major Roads (Group 1)'),
    Line2D([0], [0], color='blue', linewidth=1, label='Minor Roads (Group 2)')
]

axs[1].legend(handles=legend_elements_2, loc='upper left', fontsize=10, framealpha=0.4)

plt.show()


# <div style="text-align: justify"> 
# </div>
# 

# This code reads road data from a GeoJSON file containing OSM (2024) and TomTom (2024) variables. It retains the segment length extension variable from OSM (2024) and the sample size collected for each segment from TomTom (2024), which serves as an indirect index of traffic density. Then, it calculates the length of each road segment and plots the distribution of sample sizes and total length by highway type, in a boxplot and in a barchart (double axis).

# In[25]:


import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import CategoricalDtype 

file_path = '~/Library/CloudStorage/OneDrive-Conicet/jupyter/roads/joined_output.geojson'

file_path = os.path.expanduser(file_path)

if os.path.exists(file_path):
    joined_gdf = gpd.read_file(file_path)

    joined_gdf = joined_gdf.to_crs(epsg=3395)

    joined_gdf['length_km'] = joined_gdf['geometry'].length / 1000  # Convert meters to kilometers

    joined_df = pd.DataFrame(joined_gdf)

    joined_df['highway'] = joined_df['highway'].fillna('unknown')

    total_lengths = joined_df.groupby('highway')['length_km'].sum().reset_index()

    total_lengths = total_lengths.sort_values('length_km', ascending=False)

    unique_highways = joined_df['highway'].unique()
    print(f"Unique values in 'highway' column: {unique_highways}")

    fig, ax1 = plt.subplots(figsize=(12, 8))
    sns.boxplot(x='highway', y='sampleSize', data=joined_df, ax=ax1, color='none', boxprops=dict(edgecolor='black', facecolor='none'), medianprops=dict(color='black'), width=0.6)

    ax2 = ax1.twinx()

    sns.barplot(x='highway', y='length_km', data=total_lengths, ax=ax2, color='cyan', alpha=0.5, edgecolor='darkcyan', order=total_lengths['highway'])

    
    # Fix for deprecation warning
    if isinstance(joined_df['highway'].dtype, CategoricalDtype):
        print("The column 'highway' is of categorical type.")

    ax1.set_title("Distribution of Sample Sizes and Total Length by Highway Type")
    ax1.set_xlabel("Highway Type")
    ax1.set_ylabel("Sample Size -boxplot-")
    ax2.set_ylabel("Total Length (km) -bar chart-")

    ax1.set_xticklabels(total_lengths['highway'], rotation=90)

    plt.show()

else:
    print(f"The file {file_path} does not exist. Please check the file path and try again.")


# In[5]:


import geopandas as gpd

file_path = '~/Library/CloudStorage/OneDrive-Conicet/jupyter/roads/joined_output.geojson'

gdf = gpd.read_file(file_path)

print("Variables (columns) in the GeoDataFrame:")
print(gdf.columns)

print("\nFirst rows of the GeoDataFrame:")
print(gdf.head())



# In[ ]:




