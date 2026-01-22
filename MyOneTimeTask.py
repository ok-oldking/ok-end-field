import re
import time
import cv2

def ensure_cv2_windows_closed():
    try:
        cv2.destroyAllWindows()
    except:
        pass

from qfluentwidgets import FluentIcon

from src.tasks.MyBaseTask import MyBaseTask

class MyOneTimeTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "每日炒货当倒勾"
        self.description = "识别并买卖当天最赚钱的产品，请确保调度券充足"
        self.icon = FluentIcon.SYNC
        self.default_config.update({
            '下拉菜单选项': "第一",
            '是否选项默认支持': False,
            'int选项': 1,
            '文字框选项': "默认文字",
            '长文字框选项': "默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字",
            'list选项': ['第一', '第二', '第3'],
        })
        self.config_type["下拉菜单选项"] = {'type': "drop_down",
                                      'options': ['第一', '第二', '第3']}

    def run(self):
        """主运行方法"""
        self.log_info('每日炒货任务开始运行!', notify=True)

        # 第一步：检测坐标范围
        self.check_and_handle_start_screen()

        self.log_info('每日炒货任务运行完成!', notify=True)

    def check_and_handle_start_screen(self):
        # 确保所有cv2窗口都已关闭，避免影响find_one
        ensure_cv2_windows_closed()
        # 同时检测两个指定的图片
        is_friend_home = self.find_one('in_friend_home_or_not')
        is_in_domain = self.find_one('in_domain_or_not')
        # 如果检测到任意一个目标图片，按Esc键
        if is_friend_home or is_in_domain:
            self.do_send_key_down('esc')
            self.do_send_key_up('esc')
            # 按ESC后持续识别have_tech_or_not图片并按T
            self.wait_and_press_t_when_tech_found()
            # 根据检测到的图片类型记录要等待的退出图片
            target_leave_image = None
            if is_friend_home:
                self.log_info("检测到目标图片（in_friend_home_or_not），已按Esc键")
                target_leave_image = 'leave_friend_home'
            elif is_in_domain:
                self.log_info("检测到 in_domain_or_not 图片，已按Esc键")
                target_leave_image = 'leave_domain'
            # 等待对应的退出图片出现并点击
            if target_leave_image:
                self.wait_and_click_leave_image(target_leave_image)
        else:
            # 如果两个都没有检测到，按M键
            self.do_send_key_down('m')
            self.do_send_key_up('m')
            self.log_info("未检测到目标图片，已按M键")
            # 按M键后检测是否在地图中
            self.check_in_map_and_press_esc()

    def wait_and_click_leave_image(self, target_leave_image):
        self.log_info(f"开始等待退出图片: {target_leave_image}")

        # 设置超时时间
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            # 确保所有cv2窗口都已关闭，避免影响find_one
            ensure_cv2_windows_closed()
            # 检测指定区域是否出现退出图片
            leave_image_pos = self.find_one(target_leave_image)

            # 打印find_one的结果
            self.log_info(f"find_one('{target_leave_image}') 返回结果: {leave_image_pos}")

            if leave_image_pos:
                # 获取图片位置并点击
                self.log_info(f"检测到退出图片 {target_leave_image}")
                self.click_box(leave_image_pos)
                self.log_info(f"已点击退出图片: {target_leave_image}")
                # 点击退出图片后按M键并检测是否在地图中
                self.log_info("点击退出图片后按M键")
                self.do_send_key_down('m')
                self.do_send_key_up('m')
                self.check_in_map_and_press_esc()
                return True
        # 超时处理
        self.log_info(f"等待退出图片 {target_leave_image} 超时")
        return False

    def wait_for_start_images_gone_and_press_m(self):
        self.log_info("确认是否已完全退出...")

        # 设置超时时间（可以根据实际情况调整）
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            # 确保所有cv2窗口都已关闭，避免影响find_one
            ensure_cv2_windows_closed()
            # 同时检测两个指定的图片
            is_friend_home = self.find_one('in_friend_home_or_not')
            is_in_domain = self.find_one('in_domain_or_not')
            # 如果两个图片都不存在，按M键并返回
            if not is_friend_home and not is_in_domain:
                self.do_send_key_down('m')
                self.do_send_key_up('m')
                self.log_info("确认已完全退出，已按M键")
                # 按M键后检测是否在地图中
                self.check_in_map_and_press_esc()
                return True
        # 超时处理
        self.log_info("等待退出确认超时")
        return False
    
    def check_in_map_and_press_esc(self):
        """检测是否在地图中，如果是则按ESC键"""
        # 确保所有cv2窗口都已关闭，避免影响find_one
        ensure_cv2_windows_closed()
        # 检测是否存在in_map_or_not图片
        is_in_map = self.find_one('in_map_or_not')
        if is_in_map:
            self.log_info("检测到in_map_or_not图片，已按ESC键")
            self.do_send_key_down('esc')
            self.do_send_key_up('esc')
            # 按ESC后持续识别have_tech_or_not图片并按T
            self.wait_and_press_t_when_tech_found()
            return True
        else:
            self.log_info("未检测到in_map_or_not图片")
            return False
    
    def wait_and_press_t_when_tech_found(self):
        """持续识别图片have_tech_or_not，识别到后按T"""
        self.log_info("开始持续识别have_tech_or_not图片...")
        
        # 设置超时时间（可以根据实际情况调整）
        timeout = 30
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 确保所有cv2窗口都已关闭，避免影响find_one
            ensure_cv2_windows_closed()
            # 检测是否存在have_tech_or_not图片
            have_tech = self.find_one('have_tech_or_not')
            
            if have_tech:
                self.log_info("检测到have_tech_or_not图片，已按T键")
                self.do_send_key_down('t')
                self.do_send_key_up('t')
                # 按T后持续识别in_tech_or_not图片并点击
                self.wait_and_click_in_tech()
                return True
            
            # 短暂延迟后继续检测
            time.sleep(0.5)
        
        # 超时处理
        self.log_info("等待识别have_tech_or_not图片超时")
        return False
    
    def wait_and_click_in_tech(self):
        """持续识别图片in_tech_or_not，识别到后点击图片所在区域"""
        self.log_info("开始持续识别in_tech_or_not图片...")
        
        # 设置超时时间（可以根据实际情况调整）
        timeout = 30
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 确保所有cv2窗口都已关闭，避免影响find_one
            ensure_cv2_windows_closed()
            # 检测是否存在in_tech_or_not图片
            in_tech = self.find_one('in_tech_or_not')
            
            if in_tech:
                self.log_info("检测到in_tech_or_not图片，开始点击图片所在区域")
                self.click_box(in_tech)
                self.log_info("已点击in_tech_or_not图片所在区域")
                # 点击in_tech_or_not后，持续识别in_shop_or_not和arbitrage_time图片
                self.wait_and_click_arbitrage_time()
                return True
            
            # 短暂延迟后继续检测
            time.sleep(0.5)
        
        # 超时处理
        self.log_info("等待识别in_tech_or_not图片超时")
        return False
    
    def wait_and_click_arbitrage_time(self):
        """持续识别图片in_shop_or_not和arbitrage_time，识别到后点击arbitrage_time所在区域"""
        self.log_info("开始持续识别in_shop_or_not和arbitrage_time图片...")
        
        # 设置超时时间（可以根据实际情况调整）
        timeout = 30
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 确保所有cv2窗口都已关闭，避免影响find_one
            ensure_cv2_windows_closed()
            # 同时检测两个图片
            in_shop = self.find_one('in_shop_or_not')
            arbitrage = self.find_one('arbitrage_time')
            
            # 当同时检测到两张图片时，点击arbitrage_time所在区域
            if in_shop and arbitrage:
                self.log_info("同时检测到in_shop_or_not和arbitrage_time图片")
                self.log_info("开始点击arbitrage_time图片所在区域")
                self.click_box(arbitrage)
                self.log_info("已点击arbitrage_time图片所在区域")
                # 点击arbitrage_time后，持续识别arbitrage_time1图片并执行鼠标拖动
                self.wait_and_drag_arbitrage_time1()
                return True
            
            # 短暂延迟后继续检测
            time.sleep(0.5)
        
        # 超时处理
        self.log_info("等待识别in_shop_or_not和arbitrage_time图片超时")
        return False
    
    def wait_and_drag_arbitrage_time1(self):
        """持续识别图片arbitrage_time1，识别到后鼠标在屏幕最下方从下到上拖动到屏幕最上方两次"""
        self.log_info("开始持续识别arbitrage_time1图片...")
        
        # 设置超时时间（可以根据实际情况调整）
        timeout = 30
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 确保所有cv2窗口都已关闭，避免影响find_one
            ensure_cv2_windows_closed()
            # 检测是否存在arbitrage_time1图片
            arbitrage1 = self.find_one('arbitrage_time1')
            
            if arbitrage1:
                self.log_info("检测到arbitrage_time1图片")
                # 执行鼠标从屏幕底部拖动到顶部的操作两次
                for i in range(2):
                    self.log_info(f"开始第{i+1}次从屏幕底部拖动到顶部")
                    # 屏幕底部位置（假设屏幕坐标为0,0到1,1的相对坐标，具体等游戏公测了试验过再修）
                    start_x, start_y = 0.5, 0.9
                    # 屏幕顶部位置
                    end_x, end_y = 0.5, 0.1
                    
                    # 执行鼠标拖动操作
                    self.do_mouse_down(key='left')
                    time.sleep(0.1)
                    self.do_mouse_move(end_x, end_y)
                    time.sleep(0.5)  # 拖动持续时间
                    self.do_mouse_up(key='left')
                    self.log_info(f"完成第{i+1}次从屏幕底部拖动到顶部")
                    
                    # 两次拖动之间的延迟
                    time.sleep(0.5)
                
                # 上划完成后处理所有price1到price12的价格和套利
                self.process_all_prices()
                
                return True
            
            # 短暂延迟后继续检测
            time.sleep(0.5)
        
        # 超时处理
        self.log_info("等待识别arbitrage_time1图片超时")
        return False
    
    def do_mouse_move(self, x, y):
        """移动鼠标到指定位置"""
        self.executor.interaction.do_mouse_move(x, y)
    
    def recognize_price_digits(self, price_number):
        """识别priceX图片位置的数字并记录，然后点击该位置
        :param price_number: 价格图片的编号，如1, 2, ..., 12
        :return: 识别到的数字
        """
        price_name = f'price{price_number}'
        self.log_info(f"开始识别{price_name}图片位置的数字...")
        
        # 确保所有cv2窗口都已关闭，避免影响识别
        ensure_cv2_windows_closed()
        
        # 查找priceX图片位置
        price_img = self.find_one(price_name)
        if not price_img:
            self.log_info(f"未找到{price_name}图片")
            return None
        
        # 获取priceX图片的位置信息
        bbox = price_img.bbox
        x, y, width, height = bbox
        
        # 获取屏幕分辨率
        screen_width, screen_height = self.executor.interaction.get_screen_resolution()
        
        # 将像素坐标转换为相对坐标（OCR需要的格式）
        x1 = x / screen_width
        y1 = y / screen_height
        x2 = (x + width) / screen_width
        y2 = (y + height) / screen_height
        
        # 可以根据实际需求适当扩大识别区域
        expand_ratio = 0.05  # 扩大5%
        x1 = max(0, x1 - expand_ratio)
        y1 = max(0, y1 - expand_ratio)
        x2 = min(1, x2 + expand_ratio)
        y2 = min(1, y2 + expand_ratio)
        
        # 使用OCR在priceX图片位置区域识别数字
        result = self.ocr(x1, y1, x2, y2, match=re.compile(r'\d+'), log=True)
        
        if result:
            # 提取识别到的数字并记录
            price_value = result[0].name
            attr_name = f'price_{price_number}'
            setattr(self, attr_name, price_value)
            self.log_info(f"成功识别到{price_name}位置的数字: {price_value}")
            
            # 点击priceX图片的位置
            self.log_info(f"点击{price_name}图片的位置")
            self.click_box(price_img)
            
            # 持续识别go_to_friend_price图片并点击
            self.wait_and_click_go_to_friend_price(price_number)
            
            return price_value
        else:
            self.log_info(f"在{price_name}图片位置未识别到数字")
            return None
    
    def wait_and_click_go_to_friend_price(self, current_price_number):
        """持续识别图片go_to_friend_price，识别到之后点击图片所在区域
        :param current_price_number: 当前正在处理的价格图片编号，如1, 2, ..., 12
        :return: True if successfully clicked, False otherwise
        """
        self.log_info("开始持续识别go_to_friend_price图片...")
        
        # 设置超时时间（可以根据实际情况调整）
        timeout = 30
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 确保所有cv2窗口都已关闭，避免影响find_one
            ensure_cv2_windows_closed()
            # 检测是否存在go_to_friend_price图片
            go_to_friend_price = self.find_one('go_to_friend_price')
            
            if go_to_friend_price:
                self.log_info("检测到go_to_friend_price图片，开始点击图片所在区域")
                self.click_box(go_to_friend_price)
                self.log_info("已点击go_to_friend_price图片所在区域")
                
                # 点击后等待一会儿，确保页面加载完成
                time.sleep(1.0)
                
                # 识别friend_price位置的数字并计算套利
                self.recognize_friend_price_digits(current_price_number)
                
                return True
            
            # 短暂延迟后继续检测
            time.sleep(0.5)
        
        # 超时处理
        self.log_info("等待识别go_to_friend_price图片超时")
        return False
    
    def recognize_friend_price_digits(self, current_price_number):
        """识别friend_price图片位置的数字并计算当前priceX的套利
        :param current_price_number: 当前正在处理的价格图片编号，如1, 2, ..., 12
        :return: 计算出的套利值
        """
        self.log_info("开始识别friend_price图片位置的数字...")
        
        # 确保所有cv2窗口都已关闭，避免影响识别
        ensure_cv2_windows_closed()
        
        # 查找friend_price图片位置
        friend_price = self.find_one('friend_price')
        if not friend_price:
            self.log_info("未找到friend_price图片")
            return None
        
        # 获取friend_price图片的位置信息
        bbox = friend_price.bbox
        x, y, width, height = bbox
        
        # 获取屏幕分辨率
        screen_width, screen_height = self.executor.interaction.get_screen_resolution()
        
        # 将像素坐标转换为相对坐标（OCR需要的格式）
        x1 = x / screen_width
        y1 = y / screen_height
        x2 = (x + width) / screen_width
        y2 = (y + height) / screen_height
        
        # 可以根据实际需求适当扩大识别区域
        expand_ratio = 0.05  # 扩大5%
        x1 = max(0, x1 - expand_ratio)
        y1 = max(0, y1 - expand_ratio)
        x2 = min(1, x2 + expand_ratio)
        y2 = min(1, y2 + expand_ratio)
        
        # 使用OCR在friend_price图片位置区域识别数字
        result = self.ocr(x1, y1, x2, y2, match=re.compile(r'\d+'), log=True)
        
        if result:
            # 提取识别到的数字并记录
            friend_price_value = result[0].name
            self.log_info(f"成功识别到friend_price位置的数字: {friend_price_value}")
            
            # 确保当前正在处理的priceX已存在
            price_attr = f'price_{current_price_number}'
            if not hasattr(self, price_attr) or getattr(self, price_attr) is None:
                self.log_info(f"{price_attr}不存在或为None，无法计算套利")
                return None
            
            try:
                # 获取当前priceX的价格
                price_x_value = getattr(self, price_attr)
                
                # 转换为整数计算套利
                price_x_int = int(price_x_value)
                friend_price_int = int(friend_price_value)
                
                # 计算套利：friend_price - price_x
                arbitrage_value = friend_price_int - price_x_int
                
                # 记录套利值
                arbitrage_attr = f'arbitrage{current_price_number}'
                setattr(self, arbitrage_attr, arbitrage_value)
                
                # 记录套利对应的图片位置
                if not hasattr(self, 'arbitrage_positions'):
                    self.arbitrage_positions = {}
                self.arbitrage_positions[arbitrage_attr] = f'price{current_price_number}'
                
                self.log_info(f"计算出price{current_price_number}位置的套利: {arbitrage_attr} = friend_price - price_{current_price_number} = {friend_price_value} - {price_x_value} = {arbitrage_value}")
                
                return arbitrage_value
            except ValueError:
                self.log_info("价格转换为整数失败，无法计算套利")
                return None
        else:
            self.log_info("在friend_price图片位置未识别到数字")
            return None
    
    def process_all_prices(self):
        """处理所有price1到price12的价格识别和套利计算"""
        self.log_info("开始处理所有price1到price12的价格和套利...")
        
        # 初始化存储套利位置的字典
        self.arbitrage_positions = {}
        
        # 遍历处理price1到price12
        for price_number in range(1, 13):
            self.log_info(f"===== 开始处理price{price_number} =====")
            
            # 识别当前priceX的数字并点击
            price_value = self.recognize_price_digits(price_number)
            
            if price_value:
                self.log_info(f"成功处理price{price_number}，价格为: {price_value}")
            else:
                self.log_info(f"处理price{price_number}失败")

            # 这里需要添加从friend_price界面返回到price列表的代码
            
            # 短暂延迟后处理下一个price
            time.sleep(1.0)
        
        # 处理完成后输出所有套利信息
        self.log_all_arbitrages()
        
        # 找出最大的套利值并点击对应的price图片
        self.find_and_click_max_arbitrage()
        
        return True
    
    def log_all_arbitrages(self):
        """输出所有计算出的套利信息"""
        self.log_info("\n===== 所有套利信息汇总 =====")
        
        # 遍历输出所有套利值
        for price_number in range(1, 13):
            arbitrage_attr = f'arbitrage{price_number}'
            if hasattr(self, arbitrage_attr):
                arbitrage_value = getattr(self, arbitrage_attr)
                self.log_info(f"arbitrage{price_number} = {arbitrage_value} (对应图片位置: price{price_number})")
            else:
                self.log_info(f"arbitrage{price_number}: 未计算")
        
        # 输出套利位置映射
        if hasattr(self, 'arbitrage_positions'):
            self.log_info("\n套利对应的图片位置:")
            for arbitrage, position in self.arbitrage_positions.items():
                self.log_info(f"{arbitrage} -> {position}")
        
        self.log_info("===== 套利信息汇总结束 =====")
    
    def find_and_click_max_arbitrage(self):
        """比较arbitrage1到12的大小，找出最大的那个数字并点击对应的price图片"""
        self.log_info("\n===== 开始寻找最大套利 =====")
        
        max_arbitrage = None
        max_arbitrage_number = None
        
        # 遍历所有arbitrage1到12，找出最大值
        for price_number in range(1, 13):
            arbitrage_attr = f'arbitrage{price_number}'
            if hasattr(self, arbitrage_attr):
                arbitrage_value = getattr(self, arbitrage_attr)
                
                # 比较找出最大值
                if max_arbitrage is None or arbitrage_value > max_arbitrage:
                    max_arbitrage = arbitrage_value
                    max_arbitrage_number = price_number
        
        # 如果找到最大值
        if max_arbitrage_number is not None:
            self.log_info(f"找到最大套利: arbitrage{max_arbitrage_number} = {max_arbitrage}")
            
            # 点击对应的price图片
            price_name = f'price{max_arbitrage_number}'
            self.log_info(f"开始寻找并点击对应的{price_name}图片")
            
            # 确保所有cv2窗口都已关闭，避免影响find_one
            ensure_cv2_windows_closed()
            
            # 查找对应的price图片
            price_img = self.find_one(price_name)
            if price_img:
                self.log_info(f"找到{price_name}图片，开始点击")
                self.click_box(price_img)
                self.log_info(f"已点击{price_name}图片")
                return max_arbitrage_number, max_arbitrage
            else:
                self.log_info(f"未找到{price_name}图片")
                return None, None
        else:
            self.log_info("没有计算出任何套利值，无法找到最大值")
            return None, None






    def find_some_text_on_bottom_right(self):
        return self.ocr(box="bottom_right",match="商城", log=True) #指定box以提高ocr速度

    def find_some_text_with_relative_box(self):
        return self.ocr(0.5, 0.5, 1, 1, match=re.compile("招"), log=True) #指定box以提高ocr速度

    def test_find_one_feature(self):
        return self.find_one('box_battle_1')

    def test_find_feature_list(self):
        return self.find_feature('box_battle_1')

    def run_for_5(self):
        self.operate(lambda: self.do_run_for_5())

    def do_run_for_5(self):
        self.do_send_key_down('w')
        self.sleep(0.1)
        self.do_mouse_down(key='right')
        self.sleep(0.1)
        self.do_mouse_up(key='right')
        self.sleep(5)
        self.do_send_key_up('w')
