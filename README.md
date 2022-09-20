# my_own
个人记录
training_dataset：居民小区二次供水需求预测 
文件名	介绍
daily_dataset.csv	每日间隔流量数据集，含6个小区（01-06），多个表格间对于小区的编码一致
hourly_dataset.csv	每小时间隔流量数据集，含20个小区（01-20），多个表格间对于小区的编码一致
per5min_dataset.csv	每5分钟间隔流量数据集，含20个小区（01-20），多个表格间对于小区的编码一致
sample_submission.csv	提交样例，仅供参考。
test_public.csv	测试集（小时单位），须提交20个小区、4个不连续周的供水量。也即672（小时数） x 20（小区数）的矩阵。
weather.csv	深圳市天气数据，测试集部分假定未知。
epidemic.csv	深圳市疫情数据，测试集部分假定未知。
