# 臺灣校園 3D 地圖（系列首頁）

https://andreajang0223-ops.github.io/

系列入口頁，連到各學制的 3D 校園地圖：

| 學制 | 狀態 | 網址 |
|---|---|---|
| 大專院校 | 已上線 | https://andreajang0223-ops.github.io/taiwan-campus-3d/ |
| 高中職 | 已上線 | https://andreajang0223-ops.github.io/taiwan-highschool-3d/ |
| 國中 | 建置中 | — |
| 國小 | 規劃中 | — |

右側地圖的點是大專院校（琥珀橘）與高中職（青綠）實際位置，滑過左邊卡片會只亮該學制。

## 重新產生

各網站的學校名單更新後，重跑一次即可更新校數與地圖上的點：

```
python3 tools/build_portal.py ../taiwan-campus-3d/index.html ../taiwan-highschool-3d/index.html index.html
```

國中、國小網站上線後，在 `tools/template.html` 把對應卡片的 `<div class="card … soon">` 改成 `<a class="card …" href="…">`，並在 `build_portal.py` 加上該學制的點。
