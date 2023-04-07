from api import cdsapi_p

# step1. Init client and set keys
keys = ["111111:xxxxxx", "211111:xxxxxx"]
c = cdsapi_p(keys=keys)

# step2. Add tasks to client
for year in range(1990, 2010):
    param = (
        "reanalysis-era5-single-levels",
        {
            "product_type": "reanalysis",
            "variable": "2m_temperature",
            "year": year,
            "month": [
                "01",
                "02",
            ],
            "day": [
                "01",
                "02",
                "03",
                "04",
                "05",
            ],
            "time": ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00"],
            "area": [
                55,
                70,
                15,
                140,
            ],
            "format": "netcdf",
        },
        f"D:/temp/{year}.nc",
    )

    c.add(param)

# step3. (optional) Check tasks amount
c.count()

# step4. Run tasks
## overwrite: If True, skip existed file
c.run(overwrite=True)
