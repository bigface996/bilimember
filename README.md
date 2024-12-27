# b站硬核会员答题脚本
python学习过程中的不成熟之作。主要使用PaddleOCR和GLM-4 AI模型，MuMU模拟器安装B站**实际验证可用**
**开发环境：windows+vs code+python** 

### 需要依赖
```
numpy
paddlepaddle
paddleocr==2.9.1
pyautogui
pygetwindow
zhipuai
```
**快速安装**
`pip install -r requirements.txt`

### 使用说明
在MuMU模拟器中安装B站客户端。
需要在代码中填写自己的APIkey，在[智谱AI开放平台](https://www.bigmodel.cn/console/overviewm)查看  
```python
    client = ZhipuAI(api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")  # 填写APIKey
    response = client.chat.completions.create(
        model="glm-4-air",  # 填写需要调用的模型名称
```

推荐使用**glm-4-air**模型，新账号注册送tokens  
~~原本计划使用免费的glm-4-flash模型，但经过测试错误率太高，最终得分只有27，真是答得又快，又快的~~  
有条件的大佬也可用调用别的ai模型

PaddleOCR调用**CPU**进行，适合更多人  
运行脚本前进入硬核会员答题界面，建议选择**文史**分类  
**脚本运行期间保持模拟器窗口在前台并且不要移动**  
大概3-4秒一题,循环100次也就是答100题,不过可能不太稳定少答几题,只能麻烦各位手动点几下了XD  

### 存在问题
部分题目存在敏感字词会被GLM检测并报错,导致脚本被打断