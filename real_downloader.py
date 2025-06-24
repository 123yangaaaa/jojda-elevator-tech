#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真正能下载文件的奥的斯产品下载器
基于深度分析结果，直接下载PDF样本文件
"""

import os
import time
import json
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, unquote

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('real_downloader.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RealOtisDownloader:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.download_dir = "otis_products"
        self.setup_download_dir()
        
        # 基于分析结果的产品样本链接
        self.product_brochures = {
            "ARISE": "https://assets.otiscreate.com/iaastorage/ProductDirectory/Translation/Brochure/CL_37/P_102/Arise_Brochure_OCL_002(0618)%20(1).pdf",
            "Gen3 MRL": "https://assets.otiscreate.com/iaastorage/ProductDirectory/Translation/Brochure/CL_37/P_13/Gen3%20Brochure_002(0521).pdf",
            "Gen3 MR": "https://assets.otiscreate.com/iaastorage/ProductDirectory/Translation/Brochure/CL_37/P_12/Gen3%20Brochure_002(0521).pdf"
        }
        
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
            time.sleep(5)
            
            logger.info("成功访问奥的斯网站")
            return True
            
        except Exception as e:
            logger.error(f"访问网站失败: {e}")
            return False
    
    def download_brochure_direct(self, product_name):
        """直接下载产品样本PDF"""
        try:
            if product_name not in self.product_brochures:
                logger.warning(f"未找到 {product_name} 的样本链接")
                return False
            
            url = self.product_brochures[product_name]
            logger.info(f"开始下载 {product_name} 样本: {url}")
            
            # 使用requests下载文件
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()
            
            # 从URL中提取文件名
            parsed_url = urlparse(url)
            filename = unquote(os.path.basename(parsed_url.path))
            if not filename.endswith('.pdf'):
                filename = f"{product_name}_样本.pdf"
            
            filepath = os.path.join(self.download_dir, filename)
            
            # 保存文件
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"✅ {product_name} 样本下载成功: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"下载 {product_name} 样本失败: {e}")
            return False
    
    def find_and_click_download_button(self, product_name):
        """查找并点击真正的下载按钮"""
        try:
            logger.info(f"查找 {product_name} 的下载按钮...")
            
            # 查找产品卡片
            product_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product"))
            )
            
            for card in product_cards:
                try:
                    name_element = card.find_element(By.CSS_SELECTOR, ".product-name")
                    title = name_element.text.strip()
                    
                    if product_name.lower() in title.lower():
                        logger.info(f"找到产品: {title}")
                        
                        # 点击解决方案按钮
                        solution_button = card.find_element(By.ID, "create")
                        logger.info("点击解决方案按钮...")
                        self.driver.execute_script("arguments[0].click();", solution_button)
                        time.sleep(5)
                        
                        # 查找下载按钮
                        download_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn-download")
                        logger.info(f"找到 {len(download_buttons)} 个下载按钮")
                        
                        for i, button in enumerate(download_buttons):
                            try:
                                button_id = button.get_attribute("id")
                                button_class = button.get_attribute("class")
                                button_text = button.text.strip()
                                
                                logger.info(f"下载按钮 {i}: ID='{button_id}', 类='{button_class}', 文本='{button_text}'")
                                
                                # 点击下载按钮
                                if button.is_displayed() and button.is_enabled():
                                    logger.info(f"点击下载按钮 {i}...")
                                    self.driver.execute_script("arguments[0].click();", button)
                                    time.sleep(3)
                                    
                                    # 检查是否有新窗口打开
                                    if len(self.driver.window_handles) > 1:
                                        logger.info("检测到新窗口打开")
                                        self.driver.switch_to.window(self.driver.window_handles[-1])
                                        time.sleep(3)
                                        
                                        # 保存新窗口内容
                                        new_page_source = self.driver.page_source
                                        with open(f"download_window_{product_name}.html", "w", encoding="utf-8") as f:
                                            f.write(new_page_source)
                                        
                                        self.driver.save_screenshot(f"download_window_{product_name}.png")
                                        
                                        # 切回原窗口
                                        self.driver.switch_to.window(self.driver.window_handles[0])
                                    
                                    return True
                                    
                            except Exception as e:
                                logger.warning(f"点击下载按钮 {i} 失败: {e}")
                                continue
                        
                        logger.warning(f"未找到可点击的下载按钮")
                        return False
                        
                except NoSuchElementException:
                    continue
            
            logger.warning(f"未找到产品: {product_name}")
            return False
            
        except Exception as e:
            logger.error(f"查找下载按钮失败: {e}")
            return False
    
    def download_all_products(self):
        """下载所有产品"""
        try:
            logger.info("=== 开始下载所有产品 ===")
            
            success_count = 0
            
            # 方法1: 直接下载样本PDF
            logger.info("方法1: 直接下载样本PDF")
            for product_name in self.product_brochures.keys():
                logger.info(f"下载 {product_name} 样本...")
                if self.download_brochure_direct(product_name):
                    success_count += 1
            
            # 方法2: 通过网站下载按钮
            logger.info("方法2: 通过网站下载按钮")
            for product_name in self.product_brochures.keys():
                logger.info(f"通过网站下载 {product_name}...")
                if self.find_and_click_download_button(product_name):
                    success_count += 1
                    time.sleep(3)  # 等待下载完成
            
            logger.info(f"=== 下载完成，成功处理 {success_count} 个产品 ===")
            return success_count
            
        except Exception as e:
            logger.error(f"下载所有产品失败: {e}")
            return 0
    
    def run(self):
        """运行下载器"""
        try:
            logger.info("=== 真正下载器启动 ===")
            
            # 设置浏览器
            if not self.setup_driver():
                return False
            
            # 访问网站
            if not self.navigate_to_website():
                return False
            
            # 下载所有产品
            success_count = self.download_all_products()
            
            logger.info(f"=== 下载完成，成功处理 {success_count} 个产品 ===")
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
    downloader = RealOtisDownloader()
    success = downloader.run()
    
    if success:
        print("✅ 真正下载任务完成")
        print("请检查 otis_products 目录中的下载文件")
    else:
        print("❌ 真正下载任务失败")
    
    input("按Enter键退出...")

if __name__ == "__main__":
    main() 