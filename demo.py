from api import cdsapi_p, cdsapi_s

# cdsapi_p
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


# cdsapi_s
c = cdsapi_s(keys=keys)

func = "retrieve"
name = "reanalysis-era5-single-levels"

for year in range(2000, 2010):
    param = {
        "product_type": "reanalysis",
        "variable": "2m_temperature",
        "year": year,
        "month": [
            "01",
            "02",
            "03",
        ],
        "day": [
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
        ],
        "time": [
            "00:00",
            "01:00",
            "02:00",
            "03:00",
            "04:00",
            "05:00",
            "06:00",
            "07:00",
            "08:00",
        ],
        "area": [
            60,
            70,
            10,
            140,
        ],
        "format": "netcdf",
    }
    outfile = f"D:/temp/{year}.nc"

    c.add(func, name, param, outfile)

c.count()

c.run()
