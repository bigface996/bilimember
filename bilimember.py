import pygetwindow as gw
import pyautogui
import time
from paddleocr import PaddleOCR
import numpy as np
from zhipuai import ZhipuAI

# 加载 OCR 模型
ocr = PaddleOCR(lang='ch')
# 查找窗口
windows = gw.getWindowsWithTitle('MuMu模拟器')
if not windows:
    print("Error: 'MuMu模拟器' window not found.")
    exit(1)
window = windows[0]
# 确保窗口在前台
window.activate()
time.sleep(1)  # 等待
# 调整窗口大小至720*1080
window.resizeTo(500, 960)
time.sleep(1)  # 等待
# 获取位置
left, top, width, height = window.left, window.top, window.width, window.height


def process_screenshot_and_ocr():
    screenshot = pyautogui.screenshot(region=(left, top + 250, width, height - 380))  # 截图范围
    img_array = np.array(screenshot)
    result = ocr.ocr(img_array, cls=False)  # OCR 识别

    result = result[0]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]

    # 过滤掉"本题"开头的文本
    filtered = [(t, b) for t, b in zip(txts, boxes) 
        if not t.startswith("本题")]
    txts, boxes = zip(*filtered) if filtered else ([], [])

    # 合并距离小于10的文本框
    merged_txts = []
    merged_boxes = []
    for i, box in enumerate(boxes):
        if i == 0 or abs(box[0][1] - merged_boxes[-1][2][1]) >= 10:
            merged_txts.append(txts[i])
            merged_boxes.append(box)
        else:
            merged_txts[-1] += txts[i]
            merged_boxes[-1][2:] = box[2:]

    questionBody = "\n".join(merged_txts)

    client = ZhipuAI(api_key="xxxxxxxxxxxxxxxxxxxxxxxx")  # 填写APIKey
    response = client.chat.completions.create(
        model="glm-4-air",  # 填写需要调用的模型名称
        messages=[
                {
                    "content": "- 你是一个通晓古今的百科全书，拥有丰富的学识和答题经验。现在需要你根据用户输入的<Question>问题以及选项选出一个最合适的选项 <Answer>，然后输出选项的内容。\n- 需要注意，你的答案仅能是从选项中选择，不能自由发挥。\n- 题目类型都是选择题，一部分是问题选项，另一部分需要你从选项中选出一个最合适的填补题目的空缺。题目的空缺会用连续的下划线__表示。\n- 你只需要回答你认为正确的选项，不需要做出任何解释。你的答案需要有理论依据，不可以回答虚构的答案。\n",
                    "role": "system"
                },
                {
                    "content": "<Question>最古老的文学体裁是什么？\n诗歌\n小说\n散文\n戏剧",
                    "role": "user"
                },
                {
                    "content": "诗歌",
                    "role": "assistant"
                },
                {
                    "content": f'<Question>{questionBody}',
                    "role": "user"
                }
        ],
    )
    answer = response.choices[0].message.content

    # 找到匹配的文本框位置
    for i, txt in enumerate(txts):
        if txt == answer:
            box = boxes[i]
            x, y = box[0]
            # 将全局坐标转换为窗口内的相对坐标
            pyautogui.click(window.left + x, window.top + y + 250)
            pyautogui.moveTo(left,top)

for _ in range(50):
    process_screenshot_and_ocr()
    time.sleep(1)  # 等待