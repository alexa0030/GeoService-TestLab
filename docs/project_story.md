# 项目叙事：城市空间数据服务自动化测试与性能评测平台

## 项目背景

城乡规划与城市空间研究经常需要在 Web 地图中交互式浏览建筑、道路、公共设施等
大规模空间数据。传统接口测试只验证“能否返回”，却很难回答三个实际问题：服务升级后
瓦片接口是否仍然正确、不同 Vector Tile 服务在相同数据与负载下有何差异，以及并发增长时
延迟、吞吐量和错误率如何变化。因此，本项目以公开许可的上海中心城区 OpenStreetMap 数据
为研究对象，在同一套 PostGIS 数据、容器资源和测试场景下，对 Martin 与 pg_tileserv 建立
可重复的功能回归与性能对比基线。

## 要解决的问题

1. 将数据库、两种瓦片服务和测试程序编排成一套可一键复现的环境。
2. 验证服务目录、正常瓦片、边界参数、异常输入和跨服务回归行为。
3. 在不同图层、Zoom、单/多 Tile 和并发档位下采集可比较的性能指标。
4. 让每次代码变更都能自动重建环境、执行测试并留下日志、CSV 和图表证据。

## 实现方案

项目使用 PostgreSQL/PostGIS 管理空间数据，以 Docker Compose 同时部署 Martin 和
pg_tileserv；使用 Python、pytest、requests 封装统一 API Client，通过 fixture 和参数化用例
覆盖功能、边界、异常及 Regression 场景；使用 Apache JMeter 构造分层并发负载，再由
Python/pandas 聚合 Average、P95、Throughput 和 Error Rate；最后通过 GitHub Actions
自动启动完整环境、执行测试并上传结果。上海数据采用 ODbL 1.0 许可的 OpenStreetMap
建筑、道路与公共设施 POI，并在仓库中保留数据范围、来源及署名信息。

## 当前可验证成果

- Docker 集成环境中 29 条自动化用例全部通过。
- 完成 2 个服务、4 类瓦片场景、3 个并发档位，共 24 组 JMeter 基准实验。
- 实际执行 9,760 个请求样本，错误率为 0%。
- 50 并发下，Martin 四场景平均 P95 为 6.0 ms，pg_tileserv 为 10.5 ms；平均吞吐量
  分别为 1,184.0 req/s 与 1,094.18 req/s。
- 测试结果、聚合 CSV、可视化图表和失败日志均由 CI 自动生成并可追溯。

以上结果来自 GitHub 托管 Runner 和当前测试数据，仅用于相同环境下的服务对比，不代表
生产环境容量。上海公开数据扩展实验完成后，将补充真实要素规模、多图层及重复实验结果。

## 简历版项目描述

面向城乡空间研究中建筑、道路及公共设施数据的在线浏览需求，基于 PostgreSQL/PostGIS、
Martin 与 pg_tileserv 构建可复现的 Vector Tile 测试环境，解决空间服务升级后接口正确性
难回归、不同服务性能难量化的问题。使用 Python + pytest + requests 设计 29 条功能、边界、
异常及跨服务回归用例；使用 Apache JMeter 完成 24 组并发基准实验和 9,760 次请求，通过
Python 自动统计 P95、Throughput、Error Rate 并生成对比图。在 GitHub Actions 中实现环境
自动拉起、Regression Test、性能测试及结果归档；当前实测错误率 0%，50 并发下 Martin
平均 P95 较 pg_tileserv 低 42.9%，平均吞吐量高 8.2%。
