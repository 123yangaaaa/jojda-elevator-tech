#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终解决方案下载器 - 精确模拟用户截图操作
"""

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
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
        logging.FileHandler('final_solution_downloader.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FinalSolutionDownloader:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.download_dir = os.path.abspath("otis_solutions")
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
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # 自动下载ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 设置等待时间
            self.wait = WebDriverWait(self.driver, 30)
            
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
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product")))
            time.sleep(3)
            
            logger.info("成功访问奥的斯网站")
            return True
            
        except Exception as e:
            logger.error(f"访问网站失败: {e}")
            return False
    
    def download_solution(self, product_name):
        """下载指定产品的解决方案图纸"""
        try:
            logger.info(f"开始为产品 '{product_name}' 下载解决方案图纸")
            
            # 1. 查找并点击产品卡片上的"解决方案"按钮
            product_cards = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product")))
            product_found = False
            for card in product_cards:
                name_element = card.find_element(By.CSS_SELECTOR, ".product-name")
                if product_name.lower() in name_element.text.strip().lower():
                    product_found = True
                    logger.info(f"找到产品: {name_element.text.strip()}")
                    solution_button = card.find_element(By.ID, "create")
                    self.driver.execute_script("arguments[0].click();", solution_button)
                    logger.info("已点击'解决方案'按钮")
                    break
            
            if not product_found:
                logger.error(f"未找到产品: {product_name}")
                return False
            
            # 首先确保左侧的"电梯"产品类型被选中
            try:
                logger.info("确保'电梯'产品类型被选中...")
                elevator_type = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "productType1"))
                )
                self.driver.execute_script("arguments[0].click();", elevator_type)
                logger.info("已选中'电梯'产品类型")
                time.sleep(2)
            except TimeoutException:
                logger.warning("无法找到'电梯'产品类型选项，继续执行...")

            # 滚动到ARISE产品，确保完全可见
            logger.info("滚动到ARISE产品...")
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", solution_button)
            time.sleep(2)

            # 点击解决方案按钮
            logger.info("点击'解决方案'按钮...")
            self.driver.execute_script("arguments[0].click();", solution_button)
            logger.info("已点击'解决方案'按钮")

            # 等待更长时间并保存调试信息
            logger.info("等待界面变化...")
            time.sleep(15)  # 等待15秒，给足时间加载
            
            # 等待iaa-dimensions-shell组件加载
            try:
                logger.info("等待iaa-dimensions-shell组件加载...")
                dimensions_shell = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "iaa-dimensions-shell"))
                )
                logger.info("✅ iaa-dimensions-shell组件已加载")
                time.sleep(5)  # 再等待组件内容加载
            except TimeoutException:
                logger.warning("未检测到iaa-dimensions-shell组件")
            
            # 保存当前状态
            self.driver.save_screenshot(f"after_solution_click_{product_name}.png")
            with open(f"after_solution_click_{product_name}.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            logger.info("已保存当前页面状态")

            # 检查是否有任何模态框、弹出框或新内容出现
            potential_selectors = [
                "//button[contains(text(), '下载绘图')]",
                "//button[contains(@class, 'btn-download')]",
                "//button[contains(text(), '下载')]",
                "//*[contains(text(), '载重')]",
                "//*[contains(text(), '速度')]",
                "//*[contains(text(), '标准图纸')]",
                "//div[contains(@class, 'modal')]",
                "//div[contains(@class, 'popup')]",
                "//iframe"
            ]
            
            found_elements = []
            for selector in potential_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        found_elements.append(f"{selector}: {len(elements)}个元素")
                        logger.info(f"找到元素: {selector} ({len(elements)}个)")
                except:
                    pass
            
            if not found_elements:
                logger.error("点击'解决方案'按钮后，没有检测到任何新的界面元素！")
                logger.info("尝试重新点击...")
                
                # 尝试不同的点击方式
                try:
                    # 方法1：直接点击
                    solution_button.click()
                    time.sleep(5)
                    logger.info("尝试了直接点击")
                except:
                    pass
                
                try:
                    # 方法2：使用Actions
                    from selenium.webdriver.common.action_chains import ActionChains
                    ActionChains(self.driver).move_to_element(solution_button).click().perform()
                    time.sleep(5)
                    logger.info("尝试了ActionChains点击")
                except:
                    pass
                
                # 最后一次检查
                try:
                    download_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '下载绘图')]")
                    logger.info("最终找到了下载绘图按钮！")
                except:
                    logger.error("所有尝试均失败，无法找到下载按钮")
                    self.driver.save_screenshot(f"final_failure_{product_name}.png")
                    return False

            # 尝试寻找并点击下载按钮
            try:
                logger.info("寻找'下载绘图'按钮...")
                
                # 使用更精确的选择器，基于用户提供的HTML结构
                download_selectors = [
                    "/html/body/iaa-root/div[2]/iaa-dimensions-shell/main/div/div[1]/div[1]/form/div[2]/div/div[3]/button",  # 用户提供的精确XPath
                    "//iaa-dimensions-shell//form//button[last()]",  # 表单中的最后一个按钮
                    "//iaa-dimensions-shell//button[contains(@class, 'btn-download')]",  # dimensions-shell中的下载按钮
                    "//iaa-dimensions-shell//button[@type='submit']",  # dimensions-shell中的提交按钮
                    "//button[.//img[contains(@src, 'Download.svg')]]",
                    "//button[.//img[contains(@src, '/assets/img/Download.svg')]]",
                    "//button[contains(@class, 'btn sunset-btn btn-download ml-0') and @type='submit']",
                    "//button[contains(@class, 'sunset-btn') and contains(@class, 'btn-download') and contains(@class, 'ml-0') and @type='submit']",
                    "//button[@type='submit' and contains(@class, 'btn-download') and @data-hover='sample']",
                    "//button[contains(@class, 'sunset-btn') and contains(@class, 'btn-download') and contains(., '下载绘图')]",
                    "//button[contains(@class, 'btn-download') and contains(., '下载绘图')]",
                    "//button[@type='submit' and contains(., '下载绘图')]",
                    "//button[contains(text(), '下载绘图')]",
                    "//button[.//img[@alt='download-icon-mobile_image']]"
                ]
                
                download_button = None
                for selector in download_selectors:
                    try:
                        button = self.driver.find_element(By.XPATH, selector)
                        if button.is_displayed() and button.is_enabled():
                            download_button = button
                            logger.info(f"找到'下载绘图'按钮: {selector}")
                            break
                    except:
                        continue
                
                if download_button:
                    logger.info("找到'下载绘图'按钮，正在点击...")
                    self.driver.execute_script("arguments[0].click();", download_button)
                    logger.info("已点击'下载绘图'按钮")
                    
                    # 等待文件下载
                    logger.info("等待文件下载完成...")
                    download_success = self.wait_for_download()
                    if download_success:
                        logger.info(f"✅ 成功下载 {product_name} 的解决方案图纸！")
                        return True
                    else:
                        logger.error("下载超时或失败")
                        return False
                else:
                    raise Exception("未找到下载绘图按钮")
                    
            except Exception as e:
                logger.error(f"寻找下载绘图按钮时发生错误: {e}")
                # 尝试寻找其他可能的下载按钮
                logger.info("尝试寻找替代下载按钮...")
                alternative_selectors = [
                    "//button[contains(@class, 'btn-download')]",
                    "//button[contains(text(), '下载')]",
                    "//*[contains(@class, 'download')]//button",
                    "//a[contains(text(), '下载')]",
                    "//input[@type='submit']"
                ]
                
                for selector in alternative_selectors:
                    try:
                        button = self.driver.find_element(By.XPATH, selector)
                        logger.info(f"找到替代下载按钮: {selector}")
                        button.click()
                        time.sleep(3)
                        if self.wait_for_download():
                            logger.info(f"✅ 通过替代按钮成功下载 {product_name} 的解决方案图纸！")
                            return True
                    except:
                        continue

        except Exception as e:
            logger.error(f"下载解决方案图纸时发生未知错误: {e}")
            self.driver.save_screenshot(f"fatal_error_{product_name}.png")
            return False
            
    def run(self):
        """运行下载器"""
        try:
            logger.info("=== 最终解决方案下载器启动 ===")
            
            if not self.setup_driver() or not self.navigate_to_website():
                return

            # 下载 'ARISE' 产品的图纸作为示例
            self.download_solution("ARISE")
            
        except Exception as e:
            logger.error(f"运行下载器失败: {e}")
        
        finally:
            if self.driver:
                logger.info("关闭浏览器...")
                self.driver.quit()

def main():
    """主函数"""
    downloader = FinalSolutionDownloader()
    downloader.run()
    
if __name__ == "__main__":
    main() 