#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案分析器 - 专门分析如何获取定制图纸
"""

import os
import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('solution_analyzer.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SolutionAnalyzer:
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """设置Chrome浏览器"""
        try:
            logger.info("正在设置Chrome浏览器...")
            
            # Chrome选项
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 启用网络日志
            chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            
            # 自动下载ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 设置等待时间
            self.wait = WebDriverWait(self.driver, 20)
            
            # 执行反检测脚本
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("Chrome浏览器启动成功")
            return True
            
        except Exception as e:
            logger.error(f"设置Chrome浏览器失败: {e}")
            return False
    
    def navigate_to_website(self):
        """导航到奥的斯网站"""
        try:
            url = "https://www.otiscreate.com/product-finder/zh/cn"
            logger.info(f"正在访问: {url}")
            self.driver.get(url)
            
            # 等待页面加载
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(5)
            
            logger.info("成功访问奥的斯网站")
            return True
            
        except Exception as e:
            logger.error(f"访问网站失败: {e}")
            return False
    
    def find_and_click_product(self, product_name):
        """查找并点击产品"""
        try:
            logger.info(f"查找产品: {product_name}")
            
            # 查找产品卡片
            product_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product"))
            )
            
            logger.info(f"找到 {len(product_cards)} 个产品卡片")
            
            for i, card in enumerate(product_cards):
                try:
                    name_element = card.find_element(By.CSS_SELECTOR, ".product-name")
                    title = name_element.text.strip()
                    
                    if product_name.lower() in title.lower():
                        logger.info(f"找到产品: {title}")
                        
                        # 点击解决方案按钮
                        solution_button = card.find_element(By.ID, "create")
                        logger.info("找到解决方案按钮，准备点击...")
                        
                        # 滚动到按钮位置
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", solution_button)
                        time.sleep(1)
                        
                        # 点击按钮
                        self.driver.execute_script("arguments[0].click();", solution_button)
                        time.sleep(3)
                        logger.info("已点击解决方案按钮")
                        return True
                        
                except NoSuchElementException as e:
                    continue
            
            logger.warning(f"未找到产品: {product_name}")
            return False
            
        except Exception as e:
            logger.error(f"查找产品失败: {e}")
            return False
    
    def analyze_specification_form(self):
        """分析规格表单"""
        try:
            logger.info("分析规格表单...")
            
            # 等待页面变化
            time.sleep(5)
            
            # 保存页面源码
            page_source = self.driver.page_source
            with open("specification_form.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            
            # 保存截图
            self.driver.save_screenshot("specification_form.png")
            
            # 查找所有输入字段
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            
            logger.info(f"找到 {len(inputs)} 个输入框和 {len(selects)} 个下拉框")
            
            # 分析输入框
            input_info = []
            for i, input_elem in enumerate(inputs):
                try:
                    input_type = input_elem.get_attribute("type")
                    input_name = input_elem.get_attribute("name")
                    input_id = input_elem.get_attribute("id")
                    input_placeholder = input_elem.get_attribute("placeholder")
                    input_value = input_elem.get_attribute("value")
                    input_class = input_elem.get_attribute("class")
                    
                    if input_type or input_name or input_id or input_placeholder:
                        input_info.append({
                            "index": i,
                            "type": input_type,
                            "name": input_name,
                            "id": input_id,
                            "placeholder": input_placeholder,
                            "value": input_value,
                            "class": input_class
                        })
                        logger.info(f"输入框 {i}: 类型='{input_type}', 名称='{input_name}', ID='{input_id}', 占位符='{input_placeholder}', 值='{input_value}'")
                except Exception as e:
                    continue
            
            # 分析下拉框
            select_info = []
            for i, select_elem in enumerate(selects):
                try:
                    select_name = select_elem.get_attribute("name")
                    select_id = select_elem.get_attribute("id")
                    select_class = select_elem.get_attribute("class")
                    
                    # 获取选项
                    options = select_elem.find_elements(By.TAG_NAME, "option")
                    option_texts = [opt.text.strip() for opt in options if opt.text.strip()]
                    
                    select_info.append({
                        "index": i,
                        "name": select_name,
                        "id": select_id,
                        "class": select_class,
                        "options": option_texts
                    })
                    logger.info(f"下拉框 {i}: 名称='{select_name}', ID='{select_id}', 选项={option_texts}")
                except Exception as e:
                    continue
            
            # 查找表单提交按钮
            submit_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'btn-download') or contains(@class, 'submit') or contains(@class, 'generate')]")
            logger.info(f"找到 {len(submit_buttons)} 个提交按钮")
            
            for i, button in enumerate(submit_buttons):
                try:
                    button_text = button.text.strip()
                    button_id = button.get_attribute("id")
                    button_class = button.get_attribute("class")
                    button_disabled = button.get_attribute("disabled")
                    
                    logger.info(f"提交按钮 {i}: 文本='{button_text}', ID='{button_id}', 类='{button_class}', 禁用='{button_disabled}'")
                except Exception as e:
                    continue
            
            # 保存分析结果
            analysis_result = {
                "inputs": input_info,
                "selects": select_info,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open("specification_analysis.json", "w", encoding="utf-8") as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)
            
            logger.info("规格表单分析完成")
            return input_info, select_info
            
        except Exception as e:
            logger.error(f"分析规格表单失败: {e}")
            return [], []
    
    def fill_specifications_and_test(self, inputs, selects):
        """填写规格并测试提交"""
        try:
            logger.info("开始填写规格并测试...")
            
            # 填写输入框
            for input_info in inputs:
                try:
                    if input_info.get("placeholder"):
                        placeholder = input_info["placeholder"].lower()
                        
                        # 根据占位符填写相应的值
                        if "载重" in placeholder or "capacity" in placeholder:
                            value = "1000"
                        elif "速度" in placeholder or "speed" in placeholder:
                            value = "1.75"
                        elif "高度" in placeholder or "rise" in placeholder:
                            value = "30"
                        elif "宽度" in placeholder or "width" in placeholder:
                            value = "2000"
                        elif "深度" in placeholder or "depth" in placeholder:
                            value = "2500"
                        else:
                            continue
                        
                        # 查找对应的输入框
                        input_elements = self.driver.find_elements(By.XPATH, f"//input[@placeholder='{input_info['placeholder']}']")
                        if input_elements:
                            input_element = input_elements[0]
                            input_element.clear()
                            input_element.send_keys(value)
                            logger.info(f"填写 {input_info['placeholder']}: {value}")
                            time.sleep(1)
                            
                except Exception as e:
                    logger.warning(f"填写输入框失败: {e}")
                    continue
            
            # 选择下拉框选项
            for select_info in selects:
                try:
                    if select_info.get("options"):
                        # 选择第一个非空选项
                        for option_text in select_info["options"]:
                            if option_text and option_text != "请选择":
                                # 查找对应的下拉框
                                select_elements = self.driver.find_elements(By.XPATH, f"//select[@name='{select_info['name']}']")
                                if select_elements:
                                    select_element = select_elements[0]
                                    # 使用JavaScript选择选项
                                    self.driver.execute_script(f"arguments[0].value = '{option_text}';", select_element)
                                    logger.info(f"选择 {select_info['name']}: {option_text}")
                                    time.sleep(1)
                                break
                                
                except Exception as e:
                    logger.warning(f"选择下拉框失败: {e}")
                    continue
            
            # 等待表单更新
            time.sleep(3)
            
            # 保存填写后的页面
            page_source = self.driver.page_source
            with open("after_filling_specs.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            
            self.driver.save_screenshot("after_filling_specs.png")
            
            # 查找并测试提交按钮
            submit_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'btn-download') or contains(@class, 'submit') or contains(@class, 'generate')]")
            
            for i, button in enumerate(submit_buttons):
                try:
                    button_text = button.text.strip()
                    button_disabled = button.get_attribute("disabled")
                    
                    logger.info(f"测试提交按钮 {i}: 文本='{button_text}', 禁用='{button_disabled}'")
                    
                    # 如果按钮没有被禁用，尝试点击
                    if not button_disabled and button.is_displayed() and button.is_enabled():
                        logger.info(f"点击提交按钮: {button_text}")
                        
                        # 滚动到按钮位置
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        time.sleep(1)
                        
                        # 点击按钮
                        self.driver.execute_script("arguments[0].click();", button)
                        time.sleep(5)
                        
                        # 检查是否有新窗口打开
                        if len(self.driver.window_handles) > 1:
                            logger.info("检测到新窗口打开")
                            self.driver.switch_to.window(self.driver.window_handles[-1])
                            time.sleep(3)
                            
                            # 保存新窗口内容
                            new_page_source = self.driver.page_source
                            with open(f"solution_result_{i}.html", "w", encoding="utf-8") as f:
                                f.write(new_page_source)
                            
                            self.driver.save_screenshot(f"solution_result_{i}.png")
                            
                            # 切回原窗口
                            self.driver.switch_to.window(self.driver.window_handles[0])
                        
                        # 检查网络请求
                        logs = self.driver.get_log('performance')
                        for log in logs:
                            if 'Network.responseReceived' in log['message']:
                                logger.info(f"网络响应: {log['message']}")
                        
                        # 保存点击后的页面
                        current_source = self.driver.page_source
                        with open(f"after_submit_{i}.html", "w", encoding="utf-8") as f:
                            f.write(current_source)
                        
                        self.driver.save_screenshot(f"after_submit_{i}.png")
                        
                        return True
                        
                except Exception as e:
                    logger.error(f"测试提交按钮 {i} 失败: {e}")
                    continue
            
            logger.warning("未找到可点击的提交按钮")
            return False
            
        except Exception as e:
            logger.error(f"填写规格并测试失败: {e}")
            return False
    
    def run(self):
        """运行分析器"""
        try:
            logger.info("=== 解决方案分析器启动 ===")
            
            # 设置浏览器
            if not self.setup_driver():
                return False
            
            # 访问网站
            if not self.navigate_to_website():
                return False
            
            # 查找并点击产品
            if not self.find_and_click_product("ARISE"):
                return False
            
            # 分析规格表单
            inputs, selects = self.analyze_specification_form()
            
            # 填写规格并测试
            success = self.fill_specifications_and_test(inputs, selects)
            
            if success:
                logger.info("✅ 成功测试解决方案流程")
            else:
                logger.warning("⚠️ 解决方案流程测试未完成")
            
            logger.info("=== 解决方案分析完成 ===")
            return True
            
        except Exception as e:
            logger.error(f"解决方案分析失败: {e}")
            return False
        
        finally:
            if self.driver:
                logger.info("关闭浏览器...")
                self.driver.quit()

def main():
    """主函数"""
    analyzer = SolutionAnalyzer()
    success = analyzer.run()
    
    if success:
        print("✅ 解决方案分析完成")
        print("请查看生成的分析文件了解详细结果")
    else:
        print("❌ 解决方案分析失败")
    
    input("按Enter键退出...")

if __name__ == "__main__":
    main() 