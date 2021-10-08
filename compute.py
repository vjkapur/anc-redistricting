#!/usr/bin/env python3

import geopandas as gpd

smds = "data/Single_Member_District_from_2013.geojson"
smd_df = gpd.read_file(smds)
ward5_df = smd_df.query('ANC_ID.str.contains("5")', engine='python')[['SMD_ID', 'geometry']]

cb10 = "data/Census_Blocks_in_2010.geojson"
cb10_df = gpd.read_file(cb10)[['BLOCK','P0010001','geometry']]

# cb20 = "data/Census_Blocks_in_2020.geojson"
# cb20_df = gpd.read_file(cb20)[['BLOCK','P0010001','geometry']]

# spatial joins are creating duplication; need to revisit the method of assigning SMD to CB
cb10_with_smd = gpd.sjoin(cb10_df, ward5_df, how='inner', op='intersects')
smd_with_pop = cb10_with_smd.groupby('SMD_ID')['P0010001'].sum()

print(smd_with_pop)
