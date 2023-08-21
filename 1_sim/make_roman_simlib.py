"""make_roamn_simlib.py

Makes Roman High-Latitude simlib for SNANA
"""

from math import pi, floor

###################
# SURVEY DEFINITION
###################
SIMLIB_NAME = "rose21_20_percent.simlib"
START_MJD = 61000  # approx
SURVEY_LENGTH = 365 * 2  # days
CADENCE = 5  # days
WIDE_FILTERS = ["R", "Z", "Y", "J"]
WIDE_TILES = 68
WIDE_TILES_wPRISM = 12
DEEP_FILTERS = ["Y", "J", "H", "F"]
DEEP_TILES = 15
DEEP_TILES_wPRISM = 4

#############
# NOISE & ZP
############
# read noise assumes exposure times hard coded in the HEADER documentation
WIDE_READ_NOISE = {
    "R": 10.33,
    "Z": 12.38,
    "Y": 12.38,
    "J": 12.38,
    "H": float("nan"),
    "F": float("nan"),
}
WIDE_SKYSIG = {
    "R": 8.29,
    "Z": 6.78,
    "Y": 6.86,
    "J": 6.63,
    "H": float("nan"),
    "F": float("nan"),
}
WIDE_ZPTAVG = {
    "R": 32.500,
    "Z": 31.390,
    "Y": 31.410,
    "J": 31.350,
    "H": float("nan"),
    "F": float("nan"),
}
DEEP_READ_NOISE = {
    "R": float("nan"),
    "Z": float("nan"),
    "Y": 8.33,
    "J": 8.33,
    "H": 8.33,
    "F": 6.32,
}
DEEP_SKYSIG = {
    "R": float("nan"),
    "Z": float("nan"),
    "Y": 11.87,
    "J": 11.49,
    "H": 11.62,
    "F": 19.90,
}
DEEP_ZPTAVG = {
    "R": float("nan"),
    "Z": float("nan"),
    "Y": 32.603,
    "J": 32.543,
    "H": 32.603,
    "F": 33.346,
}


#####################################
# General Instrament Characterizatoin
#####################################

PIXELS = {"R": 0.663, "Z": 0.663, "Y": 0.711, "J": 0.767, "H": 0.891, "F": 0.990}
FOCAL_PLANE_ACTIVE_AREA = 0.281  # sq-deg
nvisits = floor(SURVEY_LENGTH / CADENCE)
steradian = (180 / pi) ** 2  # sq-deg to steradian conversion factor
solid_angle = (WIDE_TILES + DEEP_TILES) * FOCAL_PLANE_ACTIVE_AREA / steradian  # in str
slew_time = 70    # seconds
total_time = 


##################
# Template strings
##################

HEADER = f"""DOCUMENTATION:
    PURPOSE:      Roman High Latitude Extragalactic Time Domain Reference Survey
    INTENT:       Forcasting observed transients
    USAGE_KEY:    SIMLIB_FILE 
    USAGE_CODE:   snlc_sim.exe 
    TIME_TOTAL:   144  # total survey time (photometry only), days (80% of 6 months is ~144 days)
    TIME_VISIT:   {CADENCE}  # time between visits, days
    TIME_SLEW:    70   # slew time, seconds 
    TIERS:  # bands ntile nvisit Area  NLIBID  zMatch  t_expose
      - WIDE  {"".join(WIDE_FILTERS)}   {WIDE_TILES}     {nvisits}  {WIDE_TILES*FOCAL_PLANE_ACTIVE_AREA: 2.2f}   {WIDE_TILES:3d}  0.80  160.0 100.0 100.0 100.0 
      - DEEP  {"".join(DEEP_FILTERS)}   {DEEP_TILES}     {nvisits}   {WIDE_TILES*FOCAL_PLANE_ACTIVE_AREA: 2.2f}  {DEEP_TILES:3d}  1.70  300.0 300.0 300.0 900.0 
    # WIDE is set at RA: 61.24 DEC: -48.42532 (Euclid DF South, https://www.cosmos.esa.int/web/euclid/euclid-survey)
    # DEEP is centered at RA: 76.24 DEC: -48.42532 (Euclid DF South + 1hr)
    REFERENCE: Rose et al. 2021, arXiv:2111.03081
    NOTE: simlib make by Ben Rose with make_roman_simlib.py
DOCUMENTATION_END:

# ---------------------------------- 

SURVEY:   NGRST
FILTERS:  RHFJYZ 
PIXSIZE:  0.11  # arcsec 
SOLID_ANGLE:  {solid_angle:.7}  # (sr) sum of all tiers
TEMPLATE_TEXPOSE_SPECTROGRAPH: 510.9  #exposure-time for template (sec)
BEGIN LIBGEN 

"""

LIBID_HEADER = """# =========================================== 
LIBID: {libid}
FIELD: {field_name}    RA: 76.24   DEC: -48.42532    
NOBS: {nobs}
#                          READ          PSFSIG1,2  
#     MJD  IDEXPT FLT GAIN NOISE SKYSIG (pixels) RATIO  ZPTAVG ZPTERR  MAG 
"""

LIBID_ENTRY = "S: {mjd}  {id_expt:3d} {flt} {GAIN:.1f} {read_noise} {skysig} {pixels} {RATIO:.1f} {RATIO:.1f} {zptavg} {ZPTERR} {MAG}"

# SNANA keys that don't change
GAIN = 1.0
RATIO = 0.0
ZPTERR = 0.001
MAG = 99


##############
# Build simlib
##############

with open(SIMLIB_NAME, "w") as simlib:
    simlib.write(HEADER)

    # write wide libs
    nobs = nvisits * len(WIDE_FILTERS)
    for libid in range(1, WIDE_TILES + 1):  # 1 index libids
        if libid <= WIDE_TILES_wPRISM:
            field_name = "WIDE-PRISM"
        else:
            field_name = "WIDE"
        simlib.write(LIBID_HEADER.format(libid=libid, field_name=field_name, nobs=nobs))

        id_expt = 0
        for vist in range(1, nvisits + 1):  # SNANA loves 1 indexed lists.
            mjd = START_MJD + (vist - 1) * CADENCE
            for flt in WIDE_FILTERS:
                id_expt = id_expt + 1
                read_noise = WIDE_READ_NOISE[flt]
                skysig = WIDE_SKYSIG[flt]
                pixels = PIXELS[flt]
                zptavg = WIDE_ZPTAVG[flt]
                simlib.write(
                    LIBID_ENTRY.format(
                        mjd=mjd,
                        id_expt=id_expt,
                        flt=flt,
                        GAIN=GAIN,
                        read_noise=read_noise,
                        skysig=skysig,
                        pixels=pixels,
                        RATIO=RATIO,
                        zptavg=zptavg,
                        ZPTERR=ZPTERR,
                        MAG=MAG,
                    )
                )
                simlib.write("\n")
        simlib.write(f"\nEND_LIBID: {libid}\n\n")

    # write deep libs
    nobs = nvisits * len(DEEP_FILTERS)
    for libid in range(WIDE_TILES + 1, WIDE_TILES + DEEP_TILES + 1):  # 1 index libids
        if libid <= WIDE_TILES + DEEP_TILES_wPRISM:
            field_name = "DEEP-PRISM"
        else:
            field_name = "DEEP"
        simlib.write(LIBID_HEADER.format(libid=libid, field_name=field_name, nobs=nobs))

        id_expt = 0
        for vist in range(1, nvisits + 1):  # SNANA loves 1 indexed lists.
            mjd = START_MJD + (vist - 1) * CADENCE
            for flt in DEEP_FILTERS:
                id_expt = id_expt + 1
                read_noise = DEEP_READ_NOISE[flt]
                skysig = DEEP_SKYSIG[flt]
                pixels = PIXELS[flt]
                zptavg = DEEP_ZPTAVG[flt]
                simlib.write(
                    LIBID_ENTRY.format(
                        mjd=mjd,
                        id_expt=id_expt,
                        flt=flt,
                        GAIN=GAIN,
                        read_noise=read_noise,
                        skysig=skysig,
                        pixels=pixels,
                        RATIO=RATIO,
                        zptavg=zptavg,
                        ZPTERR=ZPTERR,
                        MAG=MAG,
                    )
                )
                simlib.write("\n")
        simlib.write(f"\nEND_LIBID: {libid}\n\n")

    simlib.write("END_OF_SIMLIB:")
