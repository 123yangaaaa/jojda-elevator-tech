#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级解决方案分析器 - 深入分析解决方案流程
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
        logging.FileHandler('advanced_solution_analyzer.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedSolutionAnalyzer:
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
    
    def analyze_initial_form(self):
        """分析初始表单"""
        try:
            logger.info("分析初始表单...")
            
            # 等待页面变化
            time.sleep(5)
            
            # 保存页面源码
            page_source = self.driver.page_source
            with open("initial_form.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            
            # 保存截图
            self.driver.save_screenshot("initial_form.png")
            
            # 查找所有可点击元素
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            links = self.driver.find_elements(By.TAG_NAME, "a")
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            
            logger.info(f"找到 {len(buttons)} 个按钮, {len(links)} 个链接, {len(inputs)} 个输入框")
            
            # 分析按钮
            for i, button in enumerate(buttons):
                try:
                    button_text = button.text.strip()
                    button_id = button.get_attribute("id")
                    button_class = button.get_attribute("class")
                    button_disabled = button.get_attribute("disabled")
                    
                    if button_text or button_id or button_class:
                        logger.info(f"按钮 {i}: 文本='{button_text}', ID='{button_id}', 类='{button_class}', 禁用='{button_disabled}'")
                        
                        # 如果按钮有文本且不是禁用状态，尝试点击
                        if button_text and not button_disabled and button.is_displayed():
                            logger.info(f"尝试点击按钮: {button_text}")
                            
                            # 滚动到按钮位置
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                            time.sleep(1)
                            
                            # 点击按钮
                            self.driver.execute_script("arguments[0].click();", button)
                            time.sleep(3)
                            
                            # 保存点击后的页面
                            after_click_source = self.driver.page_source
                            with open(f"after_button_click_{i}.html", "w", encoding="utf-8") as f:
                                f.write(after_click_source)
                            
                            self.driver.save_screenshot(f"after_button_click_{i}.png")
                            
                            # 重新分析页面
                            self.analyze_page_after_button_click(i)
                            
                except Exception as e:
                    logger.warning(f"分析按钮 {i} 失败: {e}")
                    continue
            
            # 分析链接
            for i, link in enumerate(links):
                try:
                    link_text = link.text.strip()
                    link_href = link.get_attribute("href")
                    link_id = link.get_attribute("id")
                    link_class = link.get_attribute("class")
                    
                    if link_text or link_href or link_id or link_class:
                        logger.info(f"链接 {i}: 文本='{link_text}', href='{link_href}', ID='{link_id}', 类='{link_class}'")
                        
                        # 如果链接有文本且不是javascript:void(0)，尝试点击
                        if link_text and link_href and link_href != "javascript:void(0)" and link.is_displayed():
                            logger.info(f"尝试点击链接: {link_text}")
                            
                            # 滚动到链接位置
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", link)
                            time.sleep(1)
                            
                            # 点击链接
                            self.driver.execute_script("arguments[0].click();", link)
                            time.sleep(3)
                            
                            # 检查是否有新窗口打开
                            if len(self.driver.window_handles) > 1:
                                logger.info("检测到新窗口打开")
                                self.driver.switch_to.window(self.driver.window_handles[-1])
                                time.sleep(3)
                                
                                # 保存新窗口内容
                                new_page_source = self.driver.page_source
                                with open(f"new_window_{i}.html", "w", encoding="utf-8") as f:
                                    f.write(new_page_source)
                                
                                self.driver.save_screenshot(f"new_window_{i}.png")
                                
                                # 切回原窗口
                                self.driver.switch_to.window(self.driver.window_handles[0])
                            
                except Exception as e:
                    logger.warning(f"分析链接 {i} 失败: {e}")
                    continue
            
            # 分析输入框
            for i, input_elem in enumerate(inputs):
                try:
                    input_type = input_elem.get_attribute("type")
                    input_name = input_elem.get_attribute("name")
                    input_id = input_elem.get_attribute("id")
                    input_placeholder = input_elem.get_attribute("placeholder")
                    input_value = input_elem.get_attribute("value")
                    input_class = input_elem.get_attribute("class")
                    
                    if input_type or input_name or input_id or input_placeholder:
                        logger.info(f"输入框 {i}: 类型='{input_type}', 名称='{input_name}', ID='{input_id}', 占位符='{input_placeholder}', 值='{input_value}'")
                        
                        # 如果是单选按钮，尝试选择
                        if input_type == "radio" and input_elem.is_displayed():
                            logger.info(f"尝试选择单选按钮: {input_name}")
                            input_elem.click()
                            time.sleep(2)
                            
                            # 保存选择后的页面
                            after_radio_source = self.driver.page_source
                            with open(f"after_radio_{i}.html", "w", encoding="utf-8") as f:
                                f.write(after_radio_source)
                            
                            self.driver.save_screenshot(f"after_radio_{i}.png")
                            
                except Exception as e:
                    logger.warning(f"分析输入框 {i} 失败: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"分析初始表单失败: {e}")
    
    def analyze_page_after_button_click(self, button_index):
        """分析按钮点击后的页面"""
        try:
            logger.info(f"分析按钮 {button_index} 点击后的页面...")
            
            # 查找所有元素
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            
            logger.info(f"按钮点击后找到: {len(buttons)} 个按钮, {len(inputs)} 个输入框, {len(selects)} 个下拉框")
            
            # 分析输入框
            for i, input_elem in enumerate(inputs):
                try:
                    input_type = input_elem.get_attribute("type")
                    input_name = input_elem.get_attribute("name")
                    input_id = input_elem.get_attribute("id")
                    input_placeholder = input_elem.get_attribute("placeholder")
                    
                    if input_placeholder:  # 只关注有占位符的输入框
                        logger.info(f"输入框 {i}: 类型='{input_type}', 名称='{input_name}', ID='{input_id}', 占位符='{input_placeholder}'")
                        
                        # 尝试填写输入框
                        if input_placeholder.lower() in ["载重", "capacity", "速度", "speed", "高度", "rise", "宽度", "width", "深度", "depth"]:
                            value = "1000" if "载重" in input_placeholder.lower() or "capacity" in input_placeholder.lower() else "1.75"
                            
                            input_elem.clear()
                            input_elem.send_keys(value)
                            logger.info(f"填写 {input_placeholder}: {value}")
                            time.sleep(1)
                            
                except Exception as e:
                    logger.warning(f"分析输入框 {i} 失败: {e}")
                    continue
            
            # 分析下拉框
            for i, select_elem in enumerate(selects):
                try:
                    select_name = select_elem.get_attribute("name")
                    select_id = select_elem.get_attribute("id")
                    
                    # 获取选项
                    options = select_elem.find_elements(By.TAG_NAME, "option")
                    option_texts = [opt.text.strip() for opt in options if opt.text.strip()]
                    
                    logger.info(f"下拉框 {i}: 名称='{select_name}', ID='{select_id}', 选项={option_texts}")
                    
                    # 选择第一个非空选项
                    if option_texts:
                        for option_text in option_texts:
                            if option_text and option_text != "请选择":
                                # 使用JavaScript选择选项
                                self.driver.execute_script(f"arguments[0].value = '{option_text}';", select_elem)
                                logger.info(f"选择 {select_name}: {option_text}")
                                time.sleep(1)
                                break
                                
                except Exception as e:
                    logger.warning(f"分析下拉框 {i} 失败: {e}")
                    continue
            
            # 查找并测试提交按钮
            submit_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'btn-download') or contains(@class, 'submit') or contains(@class, 'generate')]")
            
            for i, button in enumerate(submit_buttons):
                try:
                    button_text = button.text.strip()
                    button_disabled = button.get_attribute("disabled")
                    
                    logger.info(f"提交按钮 {i}: 文本='{button_text}', 禁用='{button_disabled}'")
                    
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
                            with open(f"solution_result_button_{button_index}.html", "w", encoding="utf-8") as f:
                                f.write(new_page_source)
                            
                            self.driver.save_screenshot(f"solution_result_button_{button_index}.png")
                            
                            # 切回原窗口
                            self.driver.switch_to.window(self.driver.window_handles[0])
                        
                        # 保存点击后的页面
                        current_source = self.driver.page_source
                        with open(f"after_submit_button_{button_index}.html", "w", encoding="utf-8") as f:
                            f.write(current_source)
                        
                        self.driver.save_screenshot(f"after_submit_button_{button_index}.png")
                        
                        return True
                        
                except Exception as e:
                    logger.error(f"测试提交按钮 {i} 失败: {e}")
                    continue
            
            return False
            
        except Exception as e:
            logger.error(f"分析按钮点击后的页面失败: {e}")
            return False
    
    def run(self):
        """运行分析器"""
        try:
            logger.info("=== 高级解决方案分析器启动 ===")
            
            # 设置浏览器
            if not self.setup_driver():
                return False
            
            # 访问网站
            if not self.navigate_to_website():
                return False
            
            # 查找并点击产品
            if not self.find_and_click_product("ARISE"):
                return False
            
            # 分析初始表单
            self.analyze_initial_form()
            
            logger.info("=== 高级解决方案分析完成 ===")
            return True
            
        except Exception as e:
            logger.error(f"高级解决方案分析失败: {e}")
            return False
        
        finally:
            if self.driver:
                logger.info("关闭浏览器...")
                self.driver.quit()

def main():
    """主函数"""
    analyzer = AdvancedSolutionAnalyzer()
    success = analyzer.run()
    
    if success:
        print("✅ 高级解决方案分析完成")
        print("请查看生成的分析文件了解详细结果")
    else:
        print("❌ 高级解决方案分析失败")
    
    input("按Enter键退出...")

if __name__ == "__main__":
    main() 