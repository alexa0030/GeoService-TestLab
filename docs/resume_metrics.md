# Resume-ready project description

## 城市空间数据服务自动化测试与性能评测平台

**科研 / 软件测试项目**

**项目背景：** 面向城乡空间研究中的在线空间数据服务需求，基于
PostgreSQL/PostGIS 搭建可复现的 Vector Tile 测试环境，对 Martin、
pg_tileserv 两类服务开展功能、接口、回归及性能验证。

**自动化测试：** 基于 Python + pytest + requests 封装统一 API Client，
使用 fixture 与参数化设计正常请求、参数边界、异常输入及跨服务回归场景；
累计落地 **29 条自动化用例**，GitHub Actions Docker 集成环境中实现
**29/29 通过**。

**环境与调试：** 基于 Linux + Docker Compose 编排 PostGIS、Martin 与
pg_tileserv 三个核心服务，通过数据库健康检查与 HTTP 重试解决容器启动时序
问题；结合 Actions 日志定位并修复 Python 导入路径、服务 Source ID、空瓦片
状态码及 MVT 字节级断言等真实问题。

**性能测试：** 使用 Apache JMeter 5.6.3 构建 **2 服务 × 4 场景 × 3 并发档位
= 24 组**性能矩阵，覆盖 Zoom 0/6/10、单 Tile/多 Tile 与 1/10/50 并发，
累计执行 **9,760 个请求样本，错误率 0%**；通过 Python/pandas 自动汇总
Average、P95、Throughput 与 Error Rate，并使用 matplotlib 生成对比图。
在本次 GitHub-hosted Runner 的 50 并发实测中，Martin 四场景平均 P95 为
**6.0 ms**，较 pg_tileserv 的 **10.5 ms 降低 42.9%**；平均吞吐量为
**1,184.0 req/s**，较 **1,094.18 req/s 提升 8.2%**。

**持续集成：** 建立 GitHub Actions 双流水线：代码更新自动拉起 Docker 环境
并执行 29 条 Regression Test，性能 Workflow 自动安装 JMeter、执行 24 组
基准测试、生成 CSV/图表并上传 artifact；最新功能与性能任务均执行成功。

## Metric provenance

- Functional CI run: 29 tests collected and passed.
- Performance run: GitHub Actions run `35974710369`, Ubuntu hosted runner.
- Raw JTL files: retained in the workflow artifact for 30 days.
- Aggregated source: `reports/benchmark_summary.csv`.
- Results are environment-specific and should not be presented as production
  capacity or a universal ranking of the two services.
