# 软著申请源代码工具

名称释义： `cccode`

- cc -> [中国版权保护中心](http://www.ccopyright.com.cn/)（**CC**opyright）
- cc -> see see
- code -> source code

功能：

- 软著申请要求提供软件源码前后各30页（60页共计3000行）
- 该工具根据要求，遍历指定项目目录所有源码文件，删除注释及空行。

## 使用方法

- 第一步：复制 `config.ini` 为 `config.custom.ini`，根据需要调整设置
- 第二步：执行
  - `python app.py`
  - 或 `make walk`
- 将在 output 目录下生成包含项目名及时间戳的源码汇总清单文件。
