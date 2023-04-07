# cdsapi_p

一个 cdsapi 多线程下载器。由于 cds 限制了一个账号只能同时处理一个文件，但可以通过多账号分发任务，从而提高下载速度。

---

## 用法

```python
from api import cdsapi_p

# step1. Init client and set keys
# 第一步 添加不同账户的key
keys = ["111111:xxxxxx", "211111:xxxxxx"]
c = cdsapi_p(keys=keys)

# step2. Add tasks to client
# 第二步 添加任务
for year in range(2000, 2010):
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
            "time": "14:00",
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
# 第三步 （可选） 查看任务数量
c.count()

# step4. Run tasks
# 第四步 开始任务
c.run(overwrite=True) # If overwrite == True, skip existed file
```

## TODO

- [x] 提升代码鲁棒性（线程复活机制、错误处理）
- [x] 添加 Toolbox 支持
