#!/usr/bin/env python3

import sys
import geopandas as gpd

wards12 = "data/Ward_from_2012.geojson"
wards12_df = gpd.read_file(wards12)[['WARD', 'geometry']]
wards12_df.rename(columns={'WARD':'Ward'}, inplace=True)

wards22 = "data/Ward_from_2022.geojson"
wards22_df = gpd.read_file(wards22)[['WARD', 'geometry']]
wards22_df.rename(columns={'WARD':'Ward'}, inplace=True)

smds = "data/Single_Member_District_from_2013.geojson"
smd_df = gpd.read_file(smds)
smd_df.rename(columns={'SMD_ID':'SMD'}, inplace=True)

council10 = "data/SMDPopulation.csv"
council10_df = gpd.read_file(council10)[['SMD', 'Population']]
council10_df.rename(columns={'Population':'council2010'}, inplace=True)
council10_df['council2010'] = council10_df['council2010'].astype(int)

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

cb10_with_smd = gpd.sjoin(cb10_df[['BLOCK','population2010','geometry']], smd_df[['SMD', 'geometry']], how='left', op='within')
cb20_with_smd = gpd.sjoin(cb20_df[['BLOCK','population2020','geometry']], smd_df[['SMD', 'geometry']], how='left', op='within')

smd_with_pop2010 = cb10_with_smd.groupby('SMD')['population2010'].sum()
smd_with_pop2020 = cb20_with_smd.groupby('SMD')['population2020'].sum()

smd_results = smd_with_pop2010.to_frame().join(smd_with_pop2020.to_frame())
smd_results = council10_df.join(smd_results, on=["SMD"], how="inner")

# calculate the delta of block approximation for 2010
smd_results['block-approx miscount (2010)'] = smd_results['population2010']-smd_results['council2010']

# calculate percent change and render as a percent
smd_results['block-approx change'] = (smd_results['population2020']-smd_results['population2010'])/smd_results['population2010']
smd_results['block-approx change'] = ["%.2f%%" % elem for elem in (smd_results['population2020']-smd_results['population2010'])/smd_results['population2010']*100]

# make presentable headers
smd_results.rename(columns={"council2010": "official 2010 population", "population2010": "block-approx 2010 population", "population2020": "block-approx 2020 population"}, inplace=True)
smd_results.to_csv(r'smd-results-2021.csv', index=True, header=True)

# now sum SMDs to output ANC counts
anc_results = smd_results
anc_results['ANC'] = smd_results['SMD'].str.slice(start=0, stop=2, step=1)
smd_counts = anc_results.groupby('ANC')['SMD'].count()
anc_results = anc_results.groupby('ANC')[['official 2010 population', 'block-approx 2010 population', 'block-approx 2020 population', 'block-approx miscount (2010)']].sum()

# add helpful stats
anc_results['2013 SMD count'] = smd_counts
anc_results['2020 pop / 1900'] = ["%.2f" % elem for elem in (anc_results['block-approx 2020 population']/1900)]
anc_results['2020 pop / 2000'] = ["%.2f" % elem for elem in (anc_results['block-approx 2020 population']/2000)]
anc_results.to_csv(r'anc-results-2021.csv', index=True, header=True)

# consider the 2022 landscape, wherein Ward boundaries may split districts
cb20_with_ward_smd = gpd.sjoin(cb20_with_smd[['BLOCK','population2020','SMD','geometry']], wards22_df[['Ward', 'geometry']], how='left', op='within')
cb20_with_ward_smd['Ward-qualified SMD'] = cb20_with_ward_smd['Ward'].astype(str).str.cat(cb20_with_ward_smd['SMD'], sep='/')
smd22_results = cb20_with_ward_smd.groupby('Ward-qualified SMD')[['population2020']].sum()
smd22_results.rename(columns={"population2020": "block-approx 2020 population"}, inplace=True)
smd22_results.to_csv(r'smd-results-2022.csv', index=True, header=True)
