# anc-redistricting
work to gain early understanding of the ANC/SMD-level redistricting in the District of Columbia

## background
The District of Columbia is split into eight wards. Each Ward is split into a variable number (4-7) of Advisory Neighborhood Commissions (ANCs) lettered A up to G, which are further split into a variable number ([2-12](https://twitter.com/ANCJonah/status/1444102088187908096?s=20)) of Single Member Districts (SMDs). ANCs are identified by Ward and letter (e.g. 5D for the nominally fourth of Ward 5) and SMDs are identified by ANC and SMD number (e.g. 5D03 for the third SMD within ANC 5D). The boundaries of all of these subdivisions are subject to change in response to each US Census.

Residents of each SMD elect an ANC Commissioner who then serves within the SMD and on committee with the broader ANC. ANC Commissioner is a voluntary, unpaid, difficult, and important job. You can learn about it [here](https://anc.dc.gov/page/about-ancs) and [here](https://ggwash.org/view/43008/advisory-neighborhood-commissions-explained). Unfortunately, these positions often go vacant, or [worse](https://twitter.com/PritaPiekara/status/1445941469999730688?s=20).

2022 is a redistricting year. You can learn more about the redistricting process [here](https://planning.dc.gov/page/district-columbia-2021-ward-redistricting), [here](https://www.elissasilverman.com/redistricting), and [here](https://dcist.com/story/21/05/25/as-d-c-kicks-off-redistricting-process-two-concerns-emerge-timing-and-parking/).

The TL;DR is:
- Ward-level districting is currently being debated and primarily concerns the contentious issue of shifting portions of Ward 6 into Wards 7 and 8.
- Population growth in Wards 1-5 is nontrivial, but tracks with the District as a whole, so significant Ward-level redistricting is unlikely.
- Ward-level redistricting will take a while, and only after that will ANC-level redistricting become a concern.
- ANCs are nonpartisan offices not subject to a primary, so ANC candidate sign-up only becomes a hard deadline in summer 2022. We might not know the final boundaries until then.

## purpose
The purpose of this repository is to explore available data and begin forming an understanding of the redistricting concerns communities will likely have. The scope may grow and shrink over time.

## data sources
Most data is from [OpenDataDC](https://opendata.dc.gov)
- [SMDs from 2013](https://opendata.dc.gov/datasets/DCGIS::single-member-district-from-2013/about)
- [Census Blocks from 2010](https://opendata.dc.gov/datasets/DCGIS::census-blocks-in-2010/about)
- [Census Blocks from 2020](https://opendata.dc.gov/datasets/DCGIS::census-blocks-in-2020/about)

The official SMD-level population counts come [courtesy of ANC Commissioner Corey Holman](https://twitter.com/coreyholman/status/1468403875375951872?s=20) who transcribed them from [the 2012 Council report](https://lims.dccouncil.us/downloads/LIMS/26284/Committee_Report/B19-0528-COMMITTEEREPORT.pdf):
- [SMD populations, 2012 Council report](https://coreyholman.com/wp-content/uploads/2021/12/SMDPopulation.csv).

## methodology
### stuff that's done
**SMD-level population computations for pre-2022 boundaries:** To identify imbalances created by the [2020 Census numbers](https://planning.dc.gov/publication/2020-census-information-and-data), `compute-districts.py` crunches the numbers using the existing (2013-2022) SMD boundaries against block-level Census data from 2010 and 2020. The calculation attributes a block's whole population to the SMD containing the block's centroid, or geographical center. [ANC/SMD boundaries do not respect Census blocks](https://twitter.com/coreyholman/status/1426168813628833796?s=20), so these block-level approximations are not entirely accurate for either 2010 or 2020. The Council's official population counts, which presumably account for block-splitting, are also included in the results for reference. Some additional block-splitting likely occurs for 2020, because new block boundaries will intersect existing political boundaries in some places where new construction/infrastructure has created new blocks. In any case, the results do work out so that the sum of computed SMD populations match the District-level populations for both Census years, and 2010 approximations usually come out close to the official 2010 numbers (with some glaring exceptions).

**ANC-level population computations for pre-2022 boundaries:** Because ANC redistricting may begin at the ANC level rather than the SMD level, as advocated by Conor Shaw in [this piece](https://ggwash.org/view/83332/why-we-should-increase-the-number-of-ward-5-advisory-neighborhood-commissions), `compute-districts.py` will also output ANC-level population counts.

### stuff that could be done
- recomputing pre-2022 SMD and ANC populations against 2022 Ward boundaries (with fractionally transferred districts forking between Wards)
- better presentation for the SMD-level population numbers, like a table including population changes for Ward, ANC, and SMD boundaries and percent change.
- a visualization of the population change, possibly including block-level
- better accounting for blocksplitting, either by adding data or imputing from existing miscount calculations
- developing a tool to allow experimenting with and algorithmically generating different districts, possibly tying into the  [official redistricting tool](https://dcredistricting.esriemcs.com) maintained by DC. This tool can be used for ANC districting using some common techniques (using Ward designations as ANC/SMD proxies), but they're limiting (cannot easily edit/add defined districts, cannot split blocks)

## usage
To run:
1. download the `geojson`-formatted files for the three **OpenDataDC data sources** above, plus the CSV of transcribed Council report data, and place them in a `data` folder in the repo
1. either use the included conda environment (requires Anaconda or [miniconda](https://docs.conda.io/en/latest/miniconda.html)) to pull package dependencies through an environment:

   ```shell
   conda env create
   conda activate anc-redistricting
   ```

   or use `pip` (assumes python is already installed)

   ```shell
   pip install geopandas
   ```

1. run `compute-districts.py`

   ```shell
   python compute-districts.py
   ```
