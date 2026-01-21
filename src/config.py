import os

import numpy as np
from ok import ConfigOption

version = "dev"
#不需要修改version, Github Action打包会自动修改

key_config_option = ConfigOption('Game Hotkey Config', { #全局配置示例
    'Echo Key': 'q',
    'Liberation Key': 'r',
    'Resonance Key': 'e',
    'Tool Key': 't',
}, description='In Game Hotkey for Skills')


def make_bottom_right_black(frame): #可选. 某些游戏截图时遮挡UID使用
    """
    Changes a portion of the frame's pixels at the bottom right to black.

    Args:
        frame: The input frame (NumPy array) from OpenCV.

    Returns:
        The modified frame with the bottom-right corner blackened.  Returns the original frame
        if there's an error (e.g., invalid frame).
    """
    try:
        height, width = frame.shape[:2]  # Get height and width

        # Calculate the size of the black rectangle
        black_width = int(0.13 * width)
        black_height = int(0.025 * height)

        # Calculate the starting coordinates of the rectangle
        start_x = width - black_width
        start_y = height - black_height

        # Create a black rectangle (NumPy array of zeros)
        black_rect = np.zeros((black_height, black_width, frame.shape[2]), dtype=frame.dtype)  # Ensure same dtype

        # Replace the bottom-right portion of the frame with the black rectangle
        frame[start_y:height, start_x:width] = black_rect

        return frame
    except Exception as e:
        print(f"Error processing frame: {e}")
        return frame

config = {
    'debug': False,  # Optional, default: False
    'use_gui': True, # 目前只支持True
    'config_folder': 'configs', #最好不要修改
    'global_configs': [key_config_option],
    'screenshot_processor': make_bottom_right_black, # 在截图的时候对frame进行修改, 可选
    'gui_icon': 'icons/icon.png', #窗口图标, 最好不需要修改文件名
    'wait_until_before_delay': 0,
    'wait_until_check_delay': 0,
    'wait_until_settle_time': 0, #调用 wait_until时候, 在第一次满足条件的时候, 会等待再次检测, 以避免某些滑动动画没到预定位置就在动画路径中被检测到
    'ocr': { #可选, 使用的OCR库
        'lib': 'onnxocr',
        'params': {
            'use_openvino': True,
        }
    },
    'windows': {  # Windows游戏请填写此设置
        'exe': ['Endfield.exe'],
        # 'hwnd_class': 'UnrealWindow', #增加重名检查准确度
        'interaction': 'Genshin', # Genshin:某些操作可以后台, 部分游戏支持 PostMessage:可后台点击, 极少游戏支持 ForegroundPostMessage:前台使用PostMessage Pynput/PyDirect:仅支持前台使用
        'capture_method': ['WGC', 'BitBlt_RenderFull'],  # Windows版本支持的话, 优先使用WGC, 否则使用BitBlt_Full. 支持的capture有 BitBlt, WGC, BitBlt_RenderFull, DXGI
        'check_hdr': True, #当用户开启AutoHDR时候提示用户, 但不禁止使用
        'force_no_hdr': False, #True=当用户开启AutoHDR时候禁止使用
        'require_bg': True # 要求使用后台截图
    },
    'start_timeout': 60,  # default 60
    'window_size': { #ok-script窗口大小
        'width': 1200,
        'height': 800,
        'min_width': 600,
        'min_height': 450,
    },
    'supported_resolution': {
        'ratio': '16:9', #支持的游戏分辨率
        'min_size': (1280, 720), #支持的最低游戏分辨率
        'resize_to': [(2560, 1440), (1920, 1080), (1600, 900), (1280, 720)], #可选, 如果非16:9自动缩放为 resize_to
    },
    'links': { # 关于里显示的链接, 可选
            'default': {
                'github': 'https://github.com/ok-oldking/ok-end-field',
                'discord': 'https://discord.gg/vVyCatEBgA',
                'sponsor': 'https://www.paypal.com/ncp/payment/JWQBH7JZKNGCQ',
                'qq_group': 'https://qm.qq.com/q/NcWHQU6q8k',
                'share': 'Download from https://github.com/ok-oldking/ok-end-field',
                'faq': 'https://github.com/ok-oldking/ok-end-field',
                'qq_channel': 'https://pd.qq.com/s/djmm6l44y',
            }
        },
    'screenshots_folder': "screenshots", #截图存放目录, 每次重新启动会清空目录
    'gui_title': 'ok-ef',  #窗口名
    # 'template_matching': { # 可选, 如使用OpenCV的模板匹配
    #     'coco_feature_json': os.path.join('assets', 'result.json'), #coco格式标记, 需要png图片, 在debug模式运行后, 会对进行切图仅保留被标记部分以减少图片大小
    #     'default_horizontal_variance': 0.002, #默认x偏移, 查找不传box的时候, 会根据coco坐标, match偏移box内的
    #     'default_vertical_variance': 0.002, #默认y偏移
    #     'default_threshold': 0.8, #默认threshold
    # },
    'version': version, #版本
    'my_app': ['src.globals', 'Globals'], #可选. 全局单例对象, 可以存放加载的模型, 使用og.my_app调用
    'onetime_tasks': [  # 用户点击触发的任务
        ["src.tasks.DailyTask", "DailyTask"],        
        ["ok", "DiagnosisTask"],
    ],
    'trigger_tasks':[ # 不断执行的触发式任务
        ["src.tasks.AutoLoginTask", "AutoLoginTask"],
    ]
}
