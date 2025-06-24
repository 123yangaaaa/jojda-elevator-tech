#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版调试下载器 - 详细跟踪每个步骤
"""

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_driver():
    """设置Chrome浏览器"""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 下载设置
    download_dir = os.path.join(os.getcwd(), "otis_solutions")
    os.makedirs(download_dir, exist_ok=True)
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def take_screenshot(driver, filename):
    """保存截图"""
    driver.save_screenshot(f"debug_{filename}.png")
    logger.info(f"截图已保存: debug_{filename}.png")

def save_page_source(driver, filename):
    """保存页面源码"""
    with open(f"debug_{filename}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    logger.info(f"页面源码已保存: debug_{filename}.html")

def check_for_components(driver, stage):
    """检查页面上的关键组件"""
    logger.info(f"=== 检查组件 - {stage} ===")
    
    components_to_check = [
        ("iaa-dimensions-shell", "//iaa-dimensions-shell"),
        ("iaa-product-listing", "//iaa-product-listing"), 
        ("modal或弹窗", "//div[contains(@class, 'modal') and contains(@class, 'show')]"),
        ("按钮数量", "//button"),
        ("表单", "//form"),
        ("下载相关按钮", "//button[contains(@class, 'btn-download')]")
    ]
    
    for name, selector in components_to_check:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            logger.info(f"  {name}: 找到 {len(elements)} 个")
            if name == "iaa-dimensions-shell" and elements:
                logger.info("  🎯 找到了iaa-dimensions-shell组件！")
                return True
        except Exception as e:
            logger.warning(f"  检查 {name} 时出错: {e}")
    
    return False

def try_multiple_interactions(driver):
    """尝试多种交互方式"""
    logger.info("=== 尝试多种交互方式 ===")
    
    # 1. 查找所有可点击的元素
    clickable_elements = driver.find_elements(By.XPATH, "//a | //button | //input[@type='submit']")
    logger.info(f"找到 {len(clickable_elements)} 个可点击元素")
    
    # 2. 查找包含特定文本的元素
    text_patterns = ["标准图纸", "绘图", "规格", "配置", "定制"]
    for pattern in text_patterns:
        try:
            elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{pattern}')]")
            if elements:
                logger.info(f"找到包含'{pattern}'的元素: {len(elements)}个")
                for i, elem in enumerate(elements[:3]):  # 只检查前3个
                    try:
                        if elem.is_displayed() and elem.tag_name in ['a', 'button']:
                            logger.info(f"  可点击元素{i}: {elem.tag_name} - '{elem.text[:50]}'")
                            logger.info(f"    尝试点击...")
                            driver.execute_script("arguments[0].click();", elem)
                            time.sleep(3)
                            
                            # 检查是否出现了iaa-dimensions-shell
                            if check_for_components(driver, f"点击{pattern}后"):
                                return True
                            
                    except Exception as e:
                        logger.warning(f"    点击失败: {e}")
        except Exception as e:
            logger.warning(f"搜索'{pattern}'时出错: {e}")
    
    return False

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 30)
    
    try:
        logger.info("=== 增强版调试下载器启动 ===")
        
        # 1. 访问网站
        logger.info("访问奥的斯网站...")
        driver.get("https://www.otiscreate.com/product-finder/zh/cn")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(5)
        
        take_screenshot(driver, "01_initial_page")
        save_page_source(driver, "01_initial_page")
        check_for_components(driver, "初始页面")
        
        # 2. 找到并点击ARISE解决方案按钮
        logger.info("寻找ARISE产品的解决方案按钮...")
        arise_selectors = [
            "//div[contains(@class, 'product')]//div[contains(text(), 'ARISE')]//ancestor::div[contains(@class, 'product')]//a[@id='create']",
            "//div[contains(., 'ARISE')]//following-sibling::*//a[@id='create']",
            "//div[@class='product-name' and text()='ARISE']//ancestor::div[contains(@class, 'product')]//a[@id='create']"
        ]
        
        arise_button = None
        for selector in arise_selectors:
            try:
                arise_button = driver.find_element(By.XPATH, selector)
                logger.info(f"找到ARISE解决方案按钮: {selector}")
                break
            except:
                continue
        
        if not arise_button:
            logger.error("未找到ARISE解决方案按钮")
            return
        
        # 3. 点击解决方案按钮
        logger.info("滚动到并点击ARISE解决方案按钮...")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", arise_button)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", arise_button)
        logger.info("已点击解决方案按钮")
        
        # 4. 等待并检查变化
        for wait_time in [5, 10, 15, 20]:
            logger.info(f"等待 {wait_time} 秒...")
            time.sleep(5)
            
            take_screenshot(driver, f"02_after_click_{wait_time}s")
            if check_for_components(driver, f"点击后{wait_time}秒"):
                logger.info("✅ 找到iaa-dimensions-shell组件！")
                break
        else:
            logger.warning("❌ 未找到iaa-dimensions-shell组件，尝试其他交互...")
            
            # 5. 尝试多种交互方式
            if try_multiple_interactions(driver):
                logger.info("✅ 通过其他交互找到了组件！")
            else:
                logger.error("❌ 所有尝试都失败了")
        
        # 6. 最终尝试寻找下载按钮
        logger.info("=== 最终尝试寻找下载按钮 ===")
        
        download_selectors = [
            "/html/body/iaa-root/div[2]/iaa-dimensions-shell/main/div/div[1]/div[1]/form/div[2]/div/div[3]/button",
            "//iaa-dimensions-shell//form//button[last()]",
            "//iaa-dimensions-shell//button[@type='submit']",
            "//button[.//img[contains(@src, 'Download.svg')]]"
        ]
        
        for selector in download_selectors:
            try:
                button = driver.find_element(By.XPATH, selector)
                if button.is_displayed():
                    logger.info(f"✅ 找到下载按钮: {selector}")
                    logger.info(f"按钮文本: '{button.text}'")
                    logger.info(f"按钮HTML: {button.get_attribute('outerHTML')[:200]}")
                    
                    # 尝试点击
                    driver.execute_script("arguments[0].click();", button)
                    logger.info("✅ 成功点击下载按钮！")
                    time.sleep(10)
                    break
            except Exception as e:
                logger.debug(f"选择器 {selector} 失败: {e}")
        
        take_screenshot(driver, "03_final_state")
        save_page_source(driver, "03_final_state")
        
        input("按回车键关闭浏览器...")
        
    except Exception as e:
        logger.error(f"发生错误: {e}")
        take_screenshot(driver, "error")
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 