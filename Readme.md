# Simulating Roman Transients with SNANA

```
   ___                         _____  __ 
  / _ \___  __ _  ___ ____    / __/ |/ /
 / , _/ _ \/  ' \/ _ `/ _ \  _\ \/    /
/_/|_|\___/_/_/_/\_,_/_//_/ /___/_/|_/
```

These are the input files for [SNANA]/[Pippin] catalog-level simulations of the Roman High-Latitude Time Domain reference survey as presented in [2111.03081](https://ui.adsabs.harvard.edu/abs/2021arXiv211103081R/abstract). They allow for the simulations of extra-galactic transients, as may be observed by the Roman Space Telescope.

## Usage

The intened use, for most people, is to analyse the resulting simulations (data release to come) rather than modify the input files themselves themeselves. Though, if you intened to look at variations in the simulations, you can use these input files wherever you have access to SNANA. I would recommend running on Midway (operated by U. Chicago) or contacting one of the (contributors)[#Contributors] and asking them to run the simulations.

1. Change the name of the .yml file to avoid overwriting other simulations., e.g. 'BR-ROMAN_TRANS.yml --> {your initials}-ROMAN_TRANS.yml'
2. Check the config file before launching with 
```
pippin.sh -c {your initials}-ROMAN_TRANS.yml
```
3. Read the Pippin [best practices](https://pippin.readthedocs.io/en/latest/usage.html#best-practice).
4. Run pipeline with
```
pippin.sh {your initials}-ROMAN_TRANS.yml
```

## Support

Currently there should be a minimal expectation of support. In time, we hope to make this releasable with a full support structure. For now, these exist publically more as a reference than for broad usage.

## Project Structure

These files follow the SNANA pipeline nomenclature as defined by PIPPIN. 

- 1_sim/ - simulating
   - searcheff/roamn_deep+subaru - 
   - roman_ref.simlib - input to recreate Rose+ 2021
   - sim_foundation.input - information regarding the Foundation survey and instruments.
   - sim_roman.input - information regarding the Roman instrument/survey
   - simgen_*.input - files about how each transient should be simulated (i.e., links to the SEDs, rate as a function of redshift, ...)
- 2_lcfit/ - Light-curve fitting
   - global.yml - a list of systemics to test/change as a part of the light curve fitting and covariance steps
   - SIMFIT_*.nml - survey sepcific LC fitting settings.
- 3_clas/ - files realted to photometric classification of transients
   - models/ - contains the trained classifiers, one folder per classifier
   - train/ - contains PIPPIN pipelines to train (and validate the training) of photometric classifiers to work with Roman data.
- 6_biascor/
   - BBC_ROMAN.input - settings for the BBC step in the SN cosmology pipeline.
- BR-ROMAN_TRANS.yml - Pippin pipeline file used to run these simulations.

### Simulations files that are stored outside this folder

- `/project2/rkessler/SURVEYS/LSST/ROOT/PLASTICC/model_libs/SIMSED_BINARIES/`
   - Binaries of the transient SEDs (built for a given survey/filter set)
- `/project2/rkessler/SURVEYS/DES/ROOT/analysis_photoIa_5yr/base/foundation/sims_ia/found_yse.simlib`
   - Definition of the Foundation survey's observations
- `/project2/rkessler/SURVEYS/WFIRST/ROOT/SALT3-NIR_dev/SALT3.P22-NIR`
   - Currently using a SALT model that is not packaged with SNANA.
- `/project2/rkessler/SURVEYS/WFIRST/ROOT/kcor/H19/kcor_WFIRST_CYCLE8_IMGPRISM_2021v3.fits`
   - Filters (and prism) definitions
- `/project2/rkessler/SURVEYS/WFIRST/ROOT/starterKits/sim_host_redshift/3dhst_sim_input_cat_v1.7.hostlib`
   - host galaxy population/
- /project2/rkessler/SURVEYS/WFIRST/ROOT/models/searcheff/SEARCHEFF_PIPELINE_LOGIC.DAT
- /project2/rkessler/SURVEYS/WFIRST/ROOT/models/searcheff/SEARCHEFF_PIPELINE_WFIRST.DAT
- /project2/rkessler/SURVEYS/WFIRST/ROOT/starterKits/sim_host_redshift/AKARI+specbasis_v1.5.1.WGTMAP
- Several files in sim_foundation.input


### (Re-)Creating SIMSED_BINARIES

This needs to be redone with every update to the filters (the kcor file) or the simulation (the simlib file).

- go to `/project2/rkessler/SURVEYS/LSST/ROOT/PLASTICC/model_libs/SIMSED_BINARIES/config_NGRST`
- run `make_simsed_binaries.py make_simsed_binaries_NGRST.yaml >& make_simsed_binaries_NGRST.LOG`
- check that all the new SIMSED binary files have been created
- cp them one folder up

## Contributors

- Ben Rose
- Maria Vincenzi
- Rebekah Hounsell
- Phil Macias
- Rick Kessler
