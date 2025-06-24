#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度分析脚本 - 分析奥的斯网站的真正下载机制
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
        logging.FileHandler('deep_analysis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DeepAnalysis:
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
    
    def analyze_page_after_click(self):
        """分析点击解决方案按钮后的页面"""
        try:
            logger.info("分析点击后的页面...")
            
            # 等待页面变化
            time.sleep(5)
            
            # 保存页面源码
            page_source = self.driver.page_source
            with open("page_after_solution_click.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            
            # 保存截图
            self.driver.save_screenshot("page_after_solution_click.png")
            
            # 分析页面中的所有按钮和链接
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            links = self.driver.find_elements(By.TAG_NAME, "a")
            
            logger.info(f"找到 {len(buttons)} 个按钮和 {len(links)} 个链接")
            
            # 分析按钮
            button_info = []
            for i, button in enumerate(buttons):
                try:
                    text = button.text.strip()
                    class_name = button.get_attribute("class")
                    button_id = button.get_attribute("id")
                    onclick = button.get_attribute("onclick")
                    
                    if text or class_name or button_id:
                        button_info.append({
                            "index": i,
                            "text": text,
                            "class": class_name,
                            "id": button_id,
                            "onclick": onclick
                        })
                        logger.info(f"按钮 {i}: 文本='{text}', 类='{class_name}', ID='{button_id}'")
                except Exception as e:
                    continue
            
            # 分析链接
            link_info = []
            for i, link in enumerate(links):
                try:
                    text = link.text.strip()
                    href = link.get_attribute("href")
                    class_name = link.get_attribute("class")
                    link_id = link.get_attribute("id")
                    
                    if text or href or class_name or link_id:
                        link_info.append({
                            "index": i,
                            "text": text,
                            "href": href,
                            "class": class_name,
                            "id": link_id
                        })
                        logger.info(f"链接 {i}: 文本='{text}', href='{href}', 类='{class_name}', ID='{link_id}'")
                except Exception as e:
                    continue
            
            # 保存分析结果
            analysis_result = {
                "buttons": button_info,
                "links": link_info,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open("page_analysis_result.json", "w", encoding="utf-8") as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)
            
            logger.info("页面分析完成，结果已保存")
            return button_info, link_info
            
        except Exception as e:
            logger.error(f"分析页面失败: {e}")
            return [], []
    
    def test_download_buttons(self, buttons, links):
        """测试所有可能的下载按钮"""
        try:
            logger.info("开始测试下载按钮...")
            
            # 测试按钮
            for button in buttons:
                try:
                    text = button.get("text", "").lower()
                    if any(keyword in text for keyword in ["下载", "download", "生成", "generate", "创建", "create", "绘图", "drawing"]):
                        logger.info(f"测试按钮: {button}")
                        
                        # 查找对应的按钮元素
                        button_elements = self.driver.find_elements(By.XPATH, f"//button[contains(text(), '{button['text']}')]")
                        if button_elements:
                            button_element = button_elements[0]
                            
                            # 滚动到按钮位置
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", button_element)
                            time.sleep(1)
                            
                            # 点击按钮
                            logger.info(f"点击按钮: {button['text']}")
                            self.driver.execute_script("arguments[0].click();", button_element)
                            
                            # 等待并分析结果
                            time.sleep(5)
                            
                            # 检查是否有新窗口打开
                            if len(self.driver.window_handles) > 1:
                                logger.info("检测到新窗口打开")
                                # 切换到新窗口
                                self.driver.switch_to.window(self.driver.window_handles[-1])
                                time.sleep(3)
                                
                                # 保存新窗口的页面
                                new_page_source = self.driver.page_source
                                with open(f"new_window_{button['text']}.html", "w", encoding="utf-8") as f:
                                    f.write(new_page_source)
                                
                                # 保存新窗口截图
                                self.driver.save_screenshot(f"new_window_{button['text']}.png")
                                
                                # 切回原窗口
                                self.driver.switch_to.window(self.driver.window_handles[0])
                            
                            # 检查网络请求
                            logs = self.driver.get_log('performance')
                            for log in logs:
                                if 'Network.responseReceived' in log['message']:
                                    logger.info(f"网络响应: {log['message']}")
                            
                            # 保存当前页面状态
                            current_source = self.driver.page_source
                            with open(f"after_click_{button['text']}.html", "w", encoding="utf-8") as f:
                                f.write(current_source)
                            
                            self.driver.save_screenshot(f"after_click_{button['text']}.png")
                            
                except Exception as e:
                    logger.error(f"测试按钮失败: {e}")
                    continue
            
            # 测试链接
            for link in links:
                try:
                    text = link.get("text", "").lower()
                    href = link.get("href", "").lower()
                    
                    if any(keyword in text for keyword in ["下载", "download", "生成", "generate", "创建", "create", "绘图", "drawing"]) or \
                       any(keyword in href for keyword in ["download", "generate", "create", "drawing"]):
                        logger.info(f"测试链接: {link}")
                        
                        # 查找对应的链接元素
                        link_elements = self.driver.find_elements(By.XPATH, f"//a[contains(text(), '{link['text']}')]")
                        if link_elements:
                            link_element = link_elements[0]
                            
                            # 获取链接的href
                            href_url = link_element.get_attribute("href")
                            logger.info(f"链接URL: {href_url}")
                            
                            # 如果是外部链接，直接访问
                            if href_url and href_url.startswith("http"):
                                logger.info(f"访问外部链接: {href_url}")
                                self.driver.execute_script(f"window.open('{href_url}', '_blank');")
                                time.sleep(3)
                                
                                # 切换到新窗口
                                if len(self.driver.window_handles) > 1:
                                    self.driver.switch_to.window(self.driver.window_handles[-1])
                                    time.sleep(3)
                                    
                                    # 保存新窗口内容
                                    new_page_source = self.driver.page_source
                                    with open(f"external_link_{link['text']}.html", "w", encoding="utf-8") as f:
                                        f.write(new_page_source)
                                    
                                    self.driver.save_screenshot(f"external_link_{link['text']}.png")
                                    
                                    # 切回原窗口
                                    self.driver.switch_to.window(self.driver.window_handles[0])
                            
                            # 点击链接
                            logger.info(f"点击链接: {link['text']}")
                            self.driver.execute_script("arguments[0].click();", link_element)
                            time.sleep(5)
                            
                            # 保存点击后的页面
                            current_source = self.driver.page_source
                            with open(f"after_link_click_{link['text']}.html", "w", encoding="utf-8") as f:
                                f.write(current_source)
                            
                            self.driver.save_screenshot(f"after_link_click_{link['text']}.png")
                            
                except Exception as e:
                    logger.error(f"测试链接失败: {e}")
                    continue
            
            logger.info("下载按钮测试完成")
            
        except Exception as e:
            logger.error(f"测试下载按钮失败: {e}")
    
    def run(self):
        """运行深度分析"""
        try:
            logger.info("=== 深度分析启动 ===")
            
            # 设置浏览器
            if not self.setup_driver():
                return False
            
            # 访问网站
            if not self.navigate_to_website():
                return False
            
            # 查找并点击第一个产品
            if not self.find_and_click_product("ARISE"):
                return False
            
            # 分析点击后的页面
            buttons, links = self.analyze_page_after_click()
            
            # 测试下载按钮
            self.test_download_buttons(buttons, links)
            
            logger.info("=== 深度分析完成 ===")
            return True
            
        except Exception as e:
            logger.error(f"深度分析失败: {e}")
            return False
        
        finally:
            if self.driver:
                logger.info("关闭浏览器...")
                self.driver.quit()

def main():
    """主函数"""
    analyzer = DeepAnalysis()
    success = analyzer.run()
    
    if success:
        print("✅ 深度分析完成")
    else:
        print("❌ 深度分析失败")
    
    input("按Enter键退出...")

if __name__ == "__main__":
    main() 