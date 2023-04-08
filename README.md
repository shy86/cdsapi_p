# cdsapi_p

一个 cdsapi 多线程下载器。由于 cds 限制了一个账号只能同时处理一个文件，但可以通过多账号分发任务，从而提高下载速度。

---

## 用法
`cdsapi_p`是重构的api，将请求、查询状态、下载流程分离为不同线程，处理更为及时。但目前仅支持`retrieve`
（即下载数据）。
```python
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
```
`cdsapi_s`是`cdsapi`的二次包装，在原api基础上实现了多线程，因此兼容性最好，支持原api全部操作，例如`retrieve`, `service`。
```python
from api import cdsapi_s

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

    # func is cdsapi attribute, the others are args passed to func.
    # cdsapi.Client.func(name, param, outfile)
    c.add(func, name, param, outfile)

c.count()

c.run()
```
## TODO

- [ ] 提升代码鲁棒性（线程复活机制、错误处理）
- [ ] 添加 Toolbox 支持
