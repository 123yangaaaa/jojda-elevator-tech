#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版奥的斯产品图纸下载器
基于页面分析结果，修复XPath选择器问题
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
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('otis_downloader.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FixedOtisDownloader:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.download_dir = "otis_products"
        self.setup_download_dir()
        
    def setup_download_dir(self):
        """设置下载目录"""
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logger.info(f"创建下载目录: {self.download_dir}")
    
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
            
            # 设置下载目录
            prefs = {
                "download.default_directory": os.path.abspath(self.download_dir),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
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
            time.sleep(3)
            
            logger.info("成功访问奥的斯网站")
            return True
            
        except Exception as e:
            logger.error(f"访问网站失败: {e}")
            return False
    
    def find_product(self, product_name):
        """查找指定产品"""
        try:
            logger.info(f"查找产品: {product_name}")
            
            # 等待产品卡片加载
            product_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card"))
            )
            
            for card in product_cards:
                try:
                    title_element = card.find_element(By.CSS_SELECTOR, ".product-title, h3, h4")
                    title = title_element.text.strip()
                    
                    if product_name.lower() in title.lower():
                        logger.info(f"找到产品: {title}")
                        return card
                        
                except NoSuchElementException:
                    continue
            
            logger.warning(f"未找到产品: {product_name}")
            return None
            
        except Exception as e:
            logger.error(f"查找产品失败: {e}")
            return None
    
    def click_solution_button(self, product_card):
        """点击解决方案按钮"""
        try:
            logger.info("查找解决方案按钮...")
            
            # 基于分析结果，查找id为"create"的按钮
            solution_button = product_card.find_element(By.ID, "create")
            
            if solution_button:
                logger.info("找到解决方案按钮，准备点击...")
                self.driver.execute_script("arguments[0].click();", solution_button)
                time.sleep(3)
                logger.info("已点击解决方案按钮")
                return True
            
            logger.warning("未找到解决方案按钮")
            return False
            
        except NoSuchElementException:
            logger.warning("未找到解决方案按钮")
            return False
        except Exception as e:
            logger.error(f"点击解决方案按钮失败: {e}")
            return False
    
    def wait_for_specification_form(self):
        """等待规格表单出现"""
        try:
            logger.info("等待规格表单加载...")
            
            # 等待载重、速度等规格字段出现
            spec_selectors = [
                "//div[contains(text(), '载重')]",
                "//div[contains(text(), 'Capacity')]",
                "//div[contains(text(), '速度')]",
                "//div[contains(text(), 'Speed')]",
                "//input[@placeholder*='载重']",
                "//input[@placeholder*='速度']"
            ]
            
            for selector in spec_selectors:
                try:
                    element = self.wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                    logger.info(f"找到规格元素: {element.text}")
                    return True
                except TimeoutException:
                    continue
            
            logger.warning("未找到规格表单")
            return False
            
        except Exception as e:
            logger.error(f"等待规格表单失败: {e}")
            return False
    
    def fill_specifications(self):
        """填写规格参数"""
        try:
            logger.info("开始填写规格参数...")
            
            # 基于分析结果，设置默认规格
            specs = {
                "载重": "1000",  # kg
                "速度": "1.75",  # m/s
                "提升高度": "30"  # m
            }
            
            # 查找并填写载重
            try:
                capacity_input = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, '载重') or contains(@placeholder, 'Capacity')]")
                capacity_input.clear()
                capacity_input.send_keys(specs["载重"])
                logger.info(f"填写载重: {specs['载重']} kg")
            except NoSuchElementException:
                logger.warning("未找到载重输入框")
            
            # 查找并填写速度
            try:
                speed_input = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, '速度') or contains(@placeholder, 'Speed')]")
                speed_input.clear()
                speed_input.send_keys(specs["速度"])
                logger.info(f"填写速度: {specs['速度']} m/s")
            except NoSuchElementException:
                logger.warning("未找到速度输入框")
            
            # 查找并填写提升高度
            try:
                height_input = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, '高度') or contains(@placeholder, 'Rise')]")
                height_input.clear()
                height_input.send_keys(specs["提升高度"])
                logger.info(f"填写提升高度: {specs['提升高度']} m")
            except NoSuchElementException:
                logger.warning("未找到提升高度输入框")
            
            time.sleep(2)
            logger.info("规格参数填写完成")
            return True
            
        except Exception as e:
            logger.error(f"填写规格参数失败: {e}")
            return False
    
    def find_download_button(self):
        """查找下载按钮"""
        try:
            logger.info("查找下载按钮...")
            
            # 基于分析结果，查找可能的下载按钮
            download_selectors = [
                "//button[contains(text(), '下载')]",
                "//a[contains(text(), '下载')]",
                "//button[contains(text(), 'Download')]",
                "//a[contains(text(), 'Download')]",
                "//button[contains(text(), '绘图')]",
                "//a[contains(text(), '绘图')]",
                "//button[contains(@class, 'download')]",
                "//a[contains(@class, 'download')]",
                "//button[contains(@id, 'download')]",
                "//a[contains(@id, 'download')]"
            ]
            
            for selector in download_selectors:
                try:
                    download_button = self.driver.find_element(By.XPATH, selector)
                    logger.info(f"找到下载按钮: {download_button.text}")
                    return download_button
                except NoSuchElementException:
                    continue
            
            logger.warning("未找到下载按钮")
            return None
            
        except Exception as e:
            logger.error(f"查找下载按钮失败: {e}")
            return None
    
    def download_drawing(self, product_name):
        """下载产品图纸"""
        try:
            logger.info(f"开始下载 {product_name} 的图纸...")
            
            # 查找产品
            product_card = self.find_product(product_name)
            if not product_card:
                return False
            
            # 点击解决方案按钮
            if not self.click_solution_button(product_card):
                return False
            
            # 等待规格表单
            if not self.wait_for_specification_form():
                logger.warning("规格表单未出现，尝试继续...")
            
            # 填写规格
            self.fill_specifications()
            
            # 查找下载按钮
            download_button = self.find_download_button()
            if not download_button:
                logger.error("未找到下载按钮")
                return False
            
            # 点击下载
            logger.info("点击下载按钮...")
            self.driver.execute_script("arguments[0].click();", download_button)
            
            # 等待下载完成
            time.sleep(5)
            logger.info(f"{product_name} 图纸下载完成")
            return True
            
        except Exception as e:
            logger.error(f"下载 {product_name} 图纸失败: {e}")
            return False
    
    def download_all_products(self):
        """下载所有产品图纸"""
        try:
            # 产品列表（基于页面分析结果）
            products = [
                "ARISE",
                "Gen3",
                "Gen3 MR",
                "Gen3 MRL"
            ]
            
            logger.info(f"开始批量下载 {len(products)} 个产品的图纸...")
            
            success_count = 0
            for i, product in enumerate(products, 1):
                logger.info(f"进度: {i}/{len(products)} - 处理产品: {product}")
                
                try:
                    if self.download_drawing(product):
                        success_count += 1
                        logger.info(f"✅ {product} 下载成功")
                    else:
                        logger.error(f"❌ {product} 下载失败")
                    
                    # 等待一段时间再处理下一个产品
                    time.sleep(3)
                    
                except Exception as e:
                    logger.error(f"处理 {product} 时出错: {e}")
                    continue
            
            logger.info(f"批量下载完成: {success_count}/{len(products)} 成功")
            return success_count
            
        except Exception as e:
            logger.error(f"批量下载失败: {e}")
            return 0
    
    def save_page_analysis(self):
        """保存页面分析结果"""
        try:
            # 保存页面源码
            page_source = self.driver.page_source
            with open("current_page_analysis.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            
            # 保存截图
            self.driver.save_screenshot("current_page_analysis.png")
            
            logger.info("页面分析结果已保存")
            
        except Exception as e:
            logger.error(f"保存页面分析失败: {e}")
    
    def run(self):
        """运行下载器"""
        try:
            logger.info("=== 修复版奥的斯下载器启动 ===")
            
            # 设置浏览器
            if not self.setup_driver():
                return False
            
            # 访问网站
            if not self.navigate_to_website():
                return False
            
            # 保存初始页面分析
            self.save_page_analysis()
            
            # 批量下载
            success_count = self.download_all_products()
            
            logger.info(f"=== 下载完成，成功下载 {success_count} 个产品 ===")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"运行下载器失败: {e}")
            return False
        
        finally:
            if self.driver:
                logger.info("关闭浏览器...")
                self.driver.quit()

def main():
    """主函数"""
    downloader = FixedOtisDownloader()
    success = downloader.run()
    
    if success:
        print("✅ 下载任务完成")
    else:
        print("❌ 下载任务失败")
    
    input("按Enter键退出...")

if __name__ == "__main__":
    main() 