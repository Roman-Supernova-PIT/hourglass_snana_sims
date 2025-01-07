# Simulating the Roman High Latitude Time Domain Survey with SNANA

```
   ___                         _____  __ 
  / _ \___  __ _  ___ ____    / __/ |/ /
 / , _/ _ \/  ' \/ _ `/ _ \  _\ \/    /
/_/|_|\___/_/_/_/\_,_/_//_/ /___/_/|_/
```

These are the input files for [SNANA]/[Pippin] catalog-level simulations of the Roman High-Latitude Time Domain reference survey as presented in [2111.03081](https://ui.adsabs.harvard.edu/abs/2021arXiv211103081R/abstract). They allow for the simulations of extra-galactic transients as may be observed by the Roman Space Telescope. These simulations allow for both the creation of a full transient catalog and a supernova cosmology pipeline.

[SNANA]: https://github.com/RickKessler/SNANA
[Pippin]: https://github.com/dessn/Pippin

## Usage

To generate a full transient (>12 types) catalog, run
```
pippin.sh {your initials}-ROMAN-TRANS.yml
```

I recommend that you read the Pippin [best practices](https://pippin.readthedocs.io/en/latest/usage.html#best-practice) and follow those when running these simulations.

The intended use, for most people, is to analyses the resulting simulations via a data release, rather than modify the input files themselves themselves. Though, if you intend to look at variations in the simulations, you can use these input files wherever you have access to SNANA. I would recommend running on Midway (operated by U. Chicago), NERSC, or contacting one of the (contributors)[#Contributors] and asking them to run the simulations.

### Requirements

* [SNANA]
* [Pippin]
* git

### Set up

Full set up:

1. Download via `git clone https://github.com/benjaminrose/roman_snana_sims.git`
1. Change the name of PIPPIN_ROMAN_TRANS.yml to avoid overwriting other simulations., e.g. PIPPIN_ROMAN_TRANS.yml --> {your initials}_ROMAN_TRANS.yml
1. update all instances of `/project2/rkessler/SURVEYS/ROMAN/USERS/brose3/roman` to the root of the repo. You can find this string in ...
   1. PIPPIN_ROMAN_TRANS.yml
   1. 1_sim/*.input
1. Ensure you are running in a working SNANA/Pippin environment with environment variables like $SBATCH_TEMPLATES defined.
1. Check the pipeline files before launching simulations with `pippin.sh -c {your initials}_ROMAN_TRANS.yml`.
1. Run with `pippin.sh -v {your initials}_ROMAN_TRANS.yml`.

For a list of PIPPIN best practices, read https://pippin.readthedocs.io/en/latest/usage.html#best-practice

## Support

Currently there should be a minimal expectation of support. In time, we hope to make this releasable with a full support structure. For now, these exist publicly more as a reference than for broad usage.

## Project Structure

These files follow the SNANA pipeline nomenclature as defined by PIPPIN. 

- 1_sim/ - simulating
   - make_roman_simlib.py - python utility to make *.simlib files
   - rose21_25_percent.simlib - input to recreate Rose+ 2021
   - sim_roman.input - information regarding the Roman instrument/survey
   - simgen_*.input - files about how each transient should be simulated (i.e., links to the SEDs, rate as a function of redshift, ...)
- 3_clas/ - files realted to photometric classification of transients
   - models/ - contains the trained classifiers, one folder per classifier
   - train/ - contains PIPPIN pipelines to train (and validate the training) of photometric classifiers to work with Roman data.
- PIPPIN_ROMAN_TRANS.yml - Pippin pipeline file used to run these simulations.

### Simulations files that are stored outside this folder

All external files are found in `/project2/rkessler/SURVEYS/ROMAN/ROOT/` or `/project2/rkessler/SURVEYS/LSST/ROOT/` or `/project2/rkessler/PRODUCTS/SNDATA_ROOT/` on Midway and use the standard SNANA environment variables to ensure portability across SNANA instances.

## Contributors

- Ben Rose
- Maria Vincenzi
- Rebekah Hounsell
- Phil Macias
- Rick Kessler
