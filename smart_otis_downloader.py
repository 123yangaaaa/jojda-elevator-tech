#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能奥的斯下载器 - 处理模态框和动态内容
专门处理奥的斯网站的复杂交互模式
"""

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SmartOtisDownloader:
    def __init__(self, download_dir="otis_products"):
        self.base_url = "https://www.otiscreate.com/product-finder/zh/cn"
        self.driver = None
        self.wait = None
        self.download_dir = download_dir
        
    def setup_driver(self):
        """设置Chrome浏览器"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # 设置下载目录
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
        
        download_prefs = {
            "download.default_directory": os.path.abspath(self.download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", download_prefs)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            logger.info("Chrome浏览器启动成功")
            return True
        except Exception as e:
            logger.error(f"启动浏览器失败: {e}")
            return False
    
    def click_solution_and_analyze(self, product_name):
        """点击解决方案按钮并全面分析响应"""
        try:
            logger.info("访问奥的斯网站...")
            self.driver.get(self.base_url)
            time.sleep(10)
            
            # 查找产品卡片
            logger.info(f"查找产品: {product_name}")
            product_xpath = f"//div[contains(@class, 'product') and .//div[@class='product-name' and contains(text(), '{product_name}')]]"
            product_card = self.wait.until(EC.presence_of_element_located((By.XPATH, product_xpath)))
            logger.info(f"找到产品卡: {product_name}")
            
            # 保存点击前的页面状态
            self.save_page_state("before_click")
            
            # 点击解决方案按钮
            solution_xpath = ".//div[contains(@class, 'action-buttons')]//div[contains(@class, 'action-items')]//a[@id='create']"
            solution_link = product_card.find_element(By.XPATH, solution_xpath)
            
            logger.info("点击解决方案按钮...")
            solution_link.click()
            
            # 等待并分析响应
            self.comprehensive_wait_and_analyze()
            
            return True
            
        except Exception as e:
            logger.error(f"点击解决方案按钮失败: {e}")
            return False
    
    def save_page_state(self, prefix):
        """保存页面状态"""
        try:
            page_source = self.driver.page_source
            with open(f"{prefix}_page.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            
            self.driver.save_screenshot(f"{prefix}_page.png")
            logger.info(f"已保存 {prefix} 页面状态")
        except Exception as e:
            logger.error(f"保存页面状态失败: {e}")
    
    def comprehensive_wait_and_analyze(self):
        """综合等待和分析"""
        logger.info("开始综合分析...")
        
        # 等待多种可能的响应
        for i in range(15):  # 等待30秒，每2秒检查一次
            time.sleep(2)
            logger.info(f"检查第 {i+1} 次...")
            
            # 保存当前状态
            if i == 5:  # 10秒后保存一次
                self.save_page_state("after_10sec")
            elif i == 10:  # 20秒后保存一次
                self.save_page_state("after_20sec")
            
            # 检查各种可能的变化
            changes = self.detect_page_changes()
            if changes:
                logger.info(f"检测到页面变化: {changes}")
                break
        
        # 最终保存页面状态
        self.save_page_state("final")
        
        # 全面分析当前页面
        self.full_page_analysis()
    
    def detect_page_changes(self):
        """检测页面变化"""
        changes = []
        
        try:
            # 检查1: 新的输入框
            text_inputs = self.driver.find_elements(By.XPATH, "//input[@type='text' or @type='number'] | //select | //textarea")
            visible_inputs = [inp for inp in text_inputs if inp.is_displayed()]
            if len(visible_inputs) > 2:
                changes.append(f"发现 {len(visible_inputs)} 个输入框")
            
            # 检查2: 模态框或弹窗
            modals = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'modal') or contains(@class, 'popup') or contains(@class, 'dialog')]")
            visible_modals = [m for m in modals if m.is_displayed()]
            if visible_modals:
                changes.append(f"发现 {len(visible_modals)} 个模态框")
            
            # 检查3: 新的iframe
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            visible_iframes = [f for f in iframes if f.is_displayed()]
            if visible_iframes:
                changes.append(f"发现 {len(visible_iframes)} 个iframe")
            
            # 检查4: 下载相关按钮
            download_buttons = self.driver.find_elements(By.XPATH, "//*[contains(text(), '下载') or contains(text(), '绘图') or contains(text(), 'download')] and (self::button or self::a)")
            visible_downloads = [d for d in download_buttons if d.is_displayed()]
            if visible_downloads:
                changes.append(f"发现 {len(visible_downloads)} 个下载按钮")
            
            # 检查5: URL变化
            current_url = self.driver.current_url
            if "create" in current_url.lower() or "spec" in current_url.lower():
                changes.append(f"URL包含创建/规格关键词: {current_url}")
            
            # 检查6: 页面标题变化
            title = self.driver.title
            if "spec" in title.lower() or "create" in title.lower():
                changes.append(f"页面标题变化: {title}")
                
        except Exception as e:
            logger.error(f"检测页面变化时出错: {e}")
        
        return changes
    
    def full_page_analysis(self):
        """全面分析页面"""
        logger.info("=" * 60)
        logger.info("开始全面页面分析")
        logger.info("=" * 60)
        
        # 分析1: 所有输入元素
        self.analyze_input_elements()
        
        # 分析2: 所有按钮和链接
        self.analyze_clickable_elements()
        
        # 分析3: 隐藏元素
        self.analyze_hidden_elements()
        
        # 分析4: JavaScript生成的内容
        self.analyze_dynamic_content()
        
        # 分析5: 可能的iframe内容
        self.analyze_iframes()
        
        logger.info("=" * 60)
        logger.info("页面分析完成")
        logger.info("=" * 60)
    
    def analyze_input_elements(self):
        """分析输入元素"""
        logger.info("分析输入元素...")
        
        input_selectors = [
            "//input",
            "//select", 
            "//textarea",
            "//button[@type='submit']"
        ]
        
        all_inputs = []
        for selector in input_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for elem in elements:
                    try:
                        info = {
                            "tag": elem.tag_name,
                            "type": elem.get_attribute("type"),
                            "name": elem.get_attribute("name"),
                            "id": elem.get_attribute("id"),
                            "placeholder": elem.get_attribute("placeholder"),
                            "class": elem.get_attribute("class"),
                            "visible": elem.is_displayed(),
                            "enabled": elem.is_enabled()
                        }
                        all_inputs.append(info)
                    except:
                        pass
            except:
                pass
        
        logger.info(f"总共找到 {len(all_inputs)} 个输入元素:")
        for i, inp in enumerate(all_inputs):
            if inp["visible"]:
                logger.info(f"  可见输入 {i+1}: {inp}")
        
        # 保存到文件
        with open("input_analysis.json", "w", encoding="utf-8") as f:
            json.dump(all_inputs, f, ensure_ascii=False, indent=2)
    
    def analyze_clickable_elements(self):
        """分析可点击元素"""
        logger.info("分析可点击元素...")
        
        clickable_selectors = [
            "//button",
            "//a",
            "//input[@type='submit']",
            "//input[@type='button']",
            "//*[@onclick]"
        ]
        
        all_clickable = []
        for selector in clickable_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for elem in elements:
                    try:
                        text = elem.text.strip()
                        if elem.is_displayed() and text:
                            info = {
                                "tag": elem.tag_name,
                                "text": text,
                                "id": elem.get_attribute("id"),
                                "class": elem.get_attribute("class"),
                                "href": elem.get_attribute("href"),
                                "onclick": elem.get_attribute("onclick")
                            }
                            all_clickable.append(info)
                    except:
                        pass
            except:
                pass
        
        logger.info(f"找到 {len(all_clickable)} 个可点击元素:")
        for i, elem in enumerate(all_clickable):
            logger.info(f"  可点击 {i+1}: {elem}")
        
        # 保存到文件
        with open("clickable_analysis.json", "w", encoding="utf-8") as f:
            json.dump(all_clickable, f, ensure_ascii=False, indent=2)
    
    def analyze_hidden_elements(self):
        """分析隐藏元素"""
        logger.info("分析隐藏元素...")
        
        hidden_selectors = [
            "//*[@style and contains(@style, 'display: none')]",
            "//*[@style and contains(@style, 'visibility: hidden')]",
            "//*[@hidden]",
            "//*[contains(@class, 'hidden')]"
        ]
        
        hidden_count = 0
        for selector in hidden_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                if elements:
                    logger.info(f"选择器 '{selector}' 找到 {len(elements)} 个隐藏元素")
                    hidden_count += len(elements)
            except:
                pass
        
        logger.info(f"总共找到 {hidden_count} 个隐藏元素")
    
    def analyze_dynamic_content(self):
        """分析动态内容"""
        logger.info("分析动态内容...")
        
        # 执行JavaScript来查找动态生成的内容
        try:
            # 查找所有包含特定关键词的元素
            script = """
            var keywords = ['载重', '速度', '高度', '宽度', '深度', 'kg', 'm/s', 'mm', '下载', '绘图'];
            var results = [];
            
            keywords.forEach(function(keyword) {
                var xpath = "//*[contains(text(), '" + keyword + "')]";
                var elements = document.evaluate(xpath, document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
                for (var i = 0; i < elements.snapshotLength; i++) {
                    var elem = elements.snapshotItem(i);
                    results.push({
                        keyword: keyword,
                        tag: elem.tagName,
                        text: elem.textContent.trim(),
                        visible: elem.offsetParent !== null
                    });
                }
            });
            
            return results;
            """
            
            results = self.driver.execute_script(script)
            logger.info(f"JavaScript分析找到 {len(results)} 个相关元素:")
            for result in results:
                if result["visible"]:
                    logger.info(f"  动态元素: {result}")
            
            # 保存到文件
            with open("dynamic_analysis.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"JavaScript分析失败: {e}")
    
    def analyze_iframes(self):
        """分析iframe内容"""
        logger.info("分析iframe内容...")
        
        try:
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            logger.info(f"找到 {len(iframes)} 个iframe")
            
            for i, iframe in enumerate(iframes):
                try:
                    if iframe.is_displayed():
                        src = iframe.get_attribute("src")
                        logger.info(f"  iframe {i+1}: src={src}, 可见=True")
                        
                        # 尝试切换到iframe并分析内容
                        self.driver.switch_to.frame(iframe)
                        
                        # 在iframe中查找输入元素
                        iframe_inputs = self.driver.find_elements(By.XPATH, "//input | //select | //textarea")
                        iframe_buttons = self.driver.find_elements(By.XPATH, "//button | //a")
                        
                        logger.info(f"    iframe {i+1} 包含 {len(iframe_inputs)} 个输入元素, {len(iframe_buttons)} 个按钮")
                        
                        # 切换回主页面
                        self.driver.switch_to.default_content()
                    else:
                        logger.info(f"  iframe {i+1}: 不可见")
                except Exception as e:
                    logger.error(f"分析iframe {i+1} 时出错: {e}")
                    # 确保切换回主页面
                    self.driver.switch_to.default_content()
                    
        except Exception as e:
            logger.error(f"分析iframe失败: {e}")
    
    def run_comprehensive_analysis(self, product_name="ARISE"):
        """运行全面的分析流程"""
        logger.info(f"===== 开始全面分析产品 '{product_name}' =====")
        
        if not self.setup_driver():
            return False
        
        try:
            # 执行点击和分析
            success = self.click_solution_and_analyze(product_name)
            
            if success:
                logger.info("✅ 分析完成，请查看生成的文件:")
                logger.info("  - before_click_page.html/png")
                logger.info("  - after_10sec_page.html/png") 
                logger.info("  - after_20sec_page.html/png")
                logger.info("  - final_page.html/png")
                logger.info("  - input_analysis.json")
                logger.info("  - clickable_analysis.json")
                logger.info("  - dynamic_analysis.json")
            else:
                logger.error("❌ 分析失败")
            
            return success
            
        except Exception as e:
            logger.error(f"全面分析过程出错: {e}")
            return False
        finally:
            if self.driver:
                input("按Enter键关闭浏览器...")
                self.driver.quit()
                logger.info("浏览器已关闭")

def main():
    downloader = SmartOtisDownloader()
    downloader.run_comprehensive_analysis("ARISE")

if __name__ == "__main__":
    main() 