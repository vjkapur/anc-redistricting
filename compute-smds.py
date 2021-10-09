#!/usr/bin/env python3

import sys
import geopandas as gpd

smds = "data/Single_Member_District_from_2013.geojson"
smd_df = gpd.read_file(smds)
# ward5_df = smd_df.query('ANC_ID.str.contains("5")', engine='python')[['SMD_ID', 'geometry']]

cb10 = "data/Census_Blocks_in_2010.geojson"
cb10_df = gpd.read_file(cb10)[['BLOCK','P0010001','geometry']]
cb10_df.rename(columns={'P0010001':'population2010'}, inplace=True)

cb20 = "data/Census_Blocks_in_2020.geojson"
cb20_df = gpd.read_file(cb20)[['BLOCK','P0010001','geometry']]
cb20_df.rename(columns={'P0010001':'population2020'}, inplace=True)

# drop the unpopulated blocks
cb10_df = cb10_df.query("population2010>0")
cb20_df = cb20_df.query("population2020>0")

# drop the blocks down to centroids for smooth collection by imprecise SMD boundaries
cb10_df['geometry'] = cb10_df['geometry'].centroid
cb20_df['geometry'] = cb20_df['geometry'].centroid

cb10_with_smd = gpd.sjoin(cb10_df[['BLOCK','population2010','geometry']], smd_df[['SMD_ID', 'geometry']], how='left', op='within')
cb20_with_smd = gpd.sjoin(cb20_df[['BLOCK','population2020','geometry']], smd_df[['SMD_ID', 'geometry']], how='left', op='within')

smd_with_pop2010 = cb10_with_smd.groupby('SMD_ID')['population2010'].sum()
smd_with_pop2020 = cb20_with_smd.groupby('SMD_ID')['population2020'].sum()

results = smd_with_pop2010.to_frame().join(smd_with_pop2020.to_frame())

results.to_csv(r'smd-results.csv', index=True, header=True)
