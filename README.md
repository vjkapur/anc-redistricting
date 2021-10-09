# anc-redistricting
work to gain early understanding of the ANC/SMD-level redistricting of Ward 5 in the District of Columbia

## background
The District of Columbia is split into eight wards. Each Ward is split into a variable number (4-7) of Advisory Neighborhood Commissions (ANCs) lettered A up to G, which are further split into a variable number ([2-12](https://twitter.com/ANCJonah/status/1444102088187908096?s=20)) of Single Member Districts (SMDs). ANCs are identified by Ward and letter (e.g. 5D for the nominally fourth of Ward 5) and SMDs are identified by ANC and SMD number (e.g. 5D03 for the third SMD within ANC 5D). The boundaries of all of these subdivisions are subject to change in response to each US Census.

Residents of SMDs elect ANC Commissioners who then serve within the SMD and on committee with the broader ANC. ANC Commissioner is a voluntary, unpaid, difficult, and important job. You can learn about it [here](https://anc.dc.gov/page/about-ancs) and [here](https://ggwash.org/view/43008/advisory-neighborhood-commissions-explained). Unfortunately, these positions often go vacant, or [worse](https://twitter.com/PritaPiekara/status/1445941469999730688?s=20).

2022 is a redistricting year. You can learn more about the redistricting process [here](https://planning.dc.gov/page/district-columbia-2021-ward-redistricting) and [here](https://dcist.com/story/21/05/25/as-d-c-kicks-off-redistricting-process-two-concerns-emerge-timing-and-parking/).

The TL;DR is:
- Ward-level districting is currently being debated and primarily concerns the contentious issue of shifting portions of Ward 6 into Wards 7 and 8.
- Population growth in Wards 1-5 is nontrivial, but tracks with the District as a whole, so significant Ward-level redistricting is unlikely.
- Ward-level redistricting will take a while, and only after that will ANC-level redistricting become a concern.
- ANCs are nonpartisan offices not subject to a primary, so ANC candidate sign-up only becomes a hard deadline in summer 2022. We might not know the final boundaries until then.

## purpose
The purpose of this repository is to explore available data and begin forming an understanding of the redistricting concerns communities will likely have. The scope may grow and shrink over time.

## data sources
All data is from [OpenDataDC](https://opendata.dc.gov) and must be downloaded as geojson placed in a `data` directory within the repo
- [SMDs from 2013](https://opendata.dc.gov/datasets/DCGIS::single-member-district-from-2013/about)
- [Census Blocks from 2010](https://opendata.dc.gov/datasets/DCGIS::census-blocks-in-2010/about)
- [Census Blocks from 2020](https://opendata.dc.gov/datasets/DCGIS::census-blocks-in-2020/about)

## methodology
### stuff that's done
**SMD-level population computations for pre-2022 boundaries:** To identify imbalances created by the [2020 Census numbers](https://planning.dc.gov/publication/2020-census-information-and-data), ''compute.py'' crunches the numbers using the existing (2013-2022) SMD boundaries against block-level Census data from 2010 and 2020. Because the boundaries don't align precisely, and it's assumed that a Census block would never be split by an ANC boundary, the calculation attributes a block's whole population to the SMD containing the block's centroid, or geographical center. This method could inadvertently modify ANCs on the boundaries for the 2020 numbers, because new blocks will reshape existing boundary contours in some places where new construction/infrastructure has created new blocks. In any case, the results do work out so that the sum of computed SMD populations match the District-level populations in sum.

### stuff that could be done
- better presentation for the SMD-level population numbers, like a table including population changes for Ward, ANC, and SMD boundaries and percent change.
- a visualization of the population change, possibly including block-level
- developing a tool to allow experimenting with different districts, similar to the [Ward-level tool](dcredistricting.esriemcs.com) maintained by DC

## usage
To run:
1. download the `geojson`-formatted files for the three **data sources** above and place them in a `data` folder in the repo
1. either use the included conda environment (requires Anaconda or [miniconda]) to pull package dependencies through an environment:

```shell
conda env create
conda activate anc-redistricting
```

or use `pip` (assumes python is already installed)

```shell
pip install geopandas
```

1. run `compute-smds.py`

```shell
python compute-smds.py
```
