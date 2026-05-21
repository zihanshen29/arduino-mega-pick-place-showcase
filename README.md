# Arduino Mega 取放分拣机器人展示仓库

这是一个面向简历和面试展示的 Arduino Mega 2560 移动取放/分拣机器人 showcase 仓库。仓库用合成传感器日志和简化状态机复刻项目工程结构，展示有限状态机、巡线修正、超声波目标确认、颜色识别、舵机抓取和任务指标分析流程。

## 仓库定位

该仓库是公开展示版，不是原始课程/团队项目的完整私有代码。仓库中的日志、指标和图表均为 synthetic/demo 数据，用于说明工程拆解、控制流程和测试思路，不代表真实硬件验收结果。

固件目录中的 Arduino sketch 是 sanitized skeleton，用于展示状态机组织方式和接口边界，不是完整现场调参版本，也不包含私有传感器标定、真实硬件日志或不可公开路径。

## 项目背景

原项目方向是工业危险废物自主管理机器人系统开发，平台为 Arduino Mega 2560，包含直流电机驱动、灰度巡线传感器、HC-SR04 超声波、颜色传感器、LCD、语音模块、ESP8266/Serial1 遥测和舵机机械臂等模块。公开版只保留可讲解的控制架构和合成数据分析流程。

## 展示能力

- 使用有限状态机描述离开仓位、巡线、目标确认、抓取、颜色识别、分类投放和回程复位。
- 用合成日志展示 line error、PWM 修正、超声波距离、颜色置信度、舵机角度和状态切换事件。
- 用 Python 脚本生成 sample logs、解析日志、计算任务完成步数、状态占比、巡线误差和分类成功率。
- 提供一份脱敏 Arduino C/C++ demo firmware skeleton，展示状态机组织方式。
- 提供中文 GitHub Pages 项目页和面试讲解材料。

## 快速运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[test]"
python scripts\run_demo_pipeline.py
pytest
```

生成文件会写到 `data/sample_logs/` 和 `outputs/`，这些都是本地 demo 产物。

## 仓库结构

```text
arduino-mega-pick-place-showcase/
|-- README.md
|-- docs/
|   |-- index.html
|   |-- architecture.md
|   `-- interview_notes.md
|-- firmware/
|   `-- robot_controller_demo/
|       `-- robot_controller_demo.ino
|-- src/
|   `-- arduino_showcase/
|-- scripts/
|-- tests/
|-- data/
`-- outputs/
```

## 边界说明

- 不包含真实私有硬件日志、原始课程仓库、账号信息、内部路径或不可公开资料。
- Arduino sketch 是 sanitized skeleton，用于说明状态机结构，不是完整现场调参版本。
- Python 仿真是简化 demo，不是物理动力学模型。
- 所有 metrics 均来自合成 demo 数据。
