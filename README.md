# 心率监测项目

## 项目简介
这是一个简单的心率监测应用程序，使用Python开发，提供了用户友好的界面来监测和记录心率数据。

## 功能特点
- 实时心率监测
- 心率数据可视化
- 历史数据记录与查询
- 心率异常警报
- 简洁直观的用户界面

## 安装说明
### 前提条件
- Python 3.9或更高版本
- 所需依赖库（见下方）

### 从源码安装
1. 克隆仓库
```bash
git clone https://github.com/yourusername/heart_rate.git
cd heart_rate
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行应用
```bash
python heart_rate.py
```
4. 打包程序
```bash
pyinstaller -F -w -i 1.ico heart_rate.py

```


## 使用说明
1. 启动应用程序
2. 连接心率监测设备（如果有）
3. 点击"开始监测"按钮开始实时监测
4. 监测数据将实时显示在界面上
5. 可以通过"导出数据"按钮将历史数据保存为CSV格式




## 许可证
[MIT许可证](LICENSE) - 开源免费使用

## 联系方式
如有问题或建议，请联系: [your.email@example.com]