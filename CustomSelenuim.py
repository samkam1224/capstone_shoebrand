from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from random import randint , choice
from bs4 import BeautifulSoup
from datetime import datetime

import pandas as pd
import undetected_chromedriver as uc
import sys,shutil, os,time ,multiprocessing






class customselenium():
    __ver__ = '2.0' #Version of Custom Selenium 
    __dev__ = 'Sameer K' # Developed By 


    def __init__(self) -> None:      
        self.wait = None
        self.x = 0
        self.y = 0
        self.driver = None
        self.file = self.__class__.__name__
        self.random_user_agent = self.random_user() 
        self.chrome_ext = None
        self.lock =  multiprocessing.Manager().Lock()
        
    def intialize_driver(self):
        if self.driver is None:
            self.driver = self.browser()
            self.wait = WebDriverWait(self.driver,30)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
    
    def readFile(self,file):
        file,ext = file.split('.')
        data_frame = pd.DataFrame()
        try:
            if ext == 'csv':
                data_frame = pd.read_csv(f"{file}.{ext}")
            elif ext == 'xlsx':
                data_frame = pd.read_excel(f"{file}.{ext}")
        except Exception as ex:
            pass

        return data_frame         
   
    def browser(self,head=False):                  
        options = uc.ChromeOptions()
        
        # options.add_argument(f"--headers={headers}")
        options.add_argument("--disable-popup-blocking")
        # options.add_argument("--force-device-scale-factor=0.8")

        # options.add_experimental_option('prefs' ,{
        #     "download.default_directory": os.path.join(os.getcwd() , "CaptchaImage")
        # })

        # if not os.path.exists(os.path.join(os.getcwd() , "CaptchaImage")):
        #     os.mkdir(os.path.join(os.getcwd() , "CaptchaImage"))

        if self.chrome_ext is not None:
            options.add_argument(f'--load-extension={self.chrome_ext}')  

        # browser_executable_path = ".\Google\Chrome\Application\chrome.exe"

        # if not os.path.exists(browser_executable_path):
        #     print('Chrome Folder Missing, make sure chrome folder exist in current working directory.')
        #     input()
        #     sys.exit(0)
            

        try:
            driver = uc.Chrome(
                options=options,
                use_subprocess=True,
                headless=head,
                # browser_executable_path=browser_executable_path
            )            
        except Exception as ex:            
            print('Chrome Intializing Error...probably Version error \n') 
            input()          
            sys.exit(0)   

        driver.maximize_window()
        print('Chrome Intialized...')
        return driver
            
    def get_Xpath_value(self,xpath_Id,all_elements=False,wait_time = 15):        
        self.wait = WebDriverWait(self.driver,wait_time)
        if all_elements:
            locate_element = EC.presence_of_all_elements_located
        else:
            locate_element = EC.presence_of_element_located        
        try:
            value = self.wait.until(locate_element((By.XPATH, xpath_Id)))
        except Exception as ex:
            value = None   
        return value    
    
    def datime(self):
        return datetime.today().timestamp()   
    
    def chunk_list(self, data, num_chunks):
        chunk_size, remainder = divmod(len(data), num_chunks)
        chunks = []
        start = 0

        for i in range(num_chunks):
            if i < remainder:
                end = start + chunk_size + 1
            else:
                end = start + chunk_size

            chunks.append(data[start:end])
            start = end

        return chunks
    
    def remove_file(self):
        try:
            os.remove(f"{self.file}") if "xlsx" in self.file else os.remove(f"{self.file}.xlsx")    
        except Exception as ex:
            pass
    
    def randomSleep(self,start,end):        
        time.sleep(randint(start,end))

    def openNewWindow(self):
        try:
            self.driver.execute_script("window.open(arguments[0], '_blank')")
            self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception as ex:
            print(ex)
            print("Driver is not available. Make sure the driver is started.")
        return self.driver
    
    def save(self,name = None,trig=False,**kwargs):
        if name:
            self.file = name  

        try:
            dataframe = pd.read_excel(f"{self.file}.xlsx")
        except FileNotFoundError:
            dataframe = pd.DataFrame()        
        
        if trig:
            dataframe1 = pd.DataFrame(kwargs)
        else:
            dataframe1 = pd.DataFrame([kwargs])

        dataframe = pd.concat([dataframe,dataframe1],ignore_index=True)
        dataframe.to_excel(f"{self.file}.xlsx",index=False)

    def click(self,xpath,wait_time=15):
        self.wait = WebDriverWait(self.driver,wait_time)
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
            self.scrollToElement(element=element)
            self.randomSleep(2,3)
            element.click()
            return True
        except Exception as ex:
            return False
            
    def get_page_source(self,element=None):
        try:
            if element:
                source = element.get_attribute("innerHTML")
            else:
                source = self.driver.page_source              
            soup = BeautifulSoup(source,'lxml')            
        except Exception as ex : 
            soup = None
        
        return soup

    def scrollToElement(self,element):     

            
        try:
            self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});",
                    element,
            )
            

            
            x = element.location.get('x')
            y = element.location.get('y')
            
            if (self.x == x) and (self.y == y) :
                return False
        
            self.x = x
            self.y = y   
            
            return True
        except:
            return False
        
        
    
    def random_user(self):
        browsers = (
            "Mozilla",
            "Opera",
            "Internet Explorer",
            "Chrome",
            "Safari",
        )

        operating_system = (
            "Windows NT 10.0; Win64; x64",
            "Windows NT 6.1; WOW64",
            "Macintosh; Intel Mac OS X 10_15_4",
            "X11; Linux x86_64",
            "Android 10.0; Mobile",
            "iOS 13.4; iPhone",
        )

        version = {
            "Mozilla": f"{randint(3, 15)}.0",
            "Opera": f"{randint(3, 15)}.80",
            "Internet Explorer": f"{randint(3, 15)}.0",
            "Chrome": f"{randint(70, 110)}.0.3987.{randint(100, 999)}",
            "Safari": f"{randint(500, 550)}.36",
        }

        browser = choice(browsers)
        os = choice(operating_system)
        browser_version = version[browser]

        user_agent = f"{browser}/{browser_version} ({os})"

        return user_agent
    
    def validateData(self,element):
        if element :
            return element.text
        return None
        
    def load_extension(self,name,version):
        self.chrome_ext = os.path.join(os.getcwd(),name,version)
    
    def close_extension_tab(self):
        try:
            self.get_Xpath_value(xpath_Id='//p[@class="installed-loading__lead-paragraph"]')
            self.driver.switch_to.window(self.driver.window_handles[-1])  
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
        except:
            print('Disk Full ....Free Up Some Space')
            sys.exit(0)
    
    # Multi Processing Execute Function
            
    def stop_exc(self,mesg=None):
        print(mesg)
        input()
        self.close()
        sys.exit(0)
    
    def execute(self):        
        try:
            links = pd.read_excel(f"{self.file}_link.xlsx")['Links']
            self.file = f"{self.file}_link.xlsx"
            print("\nExtraction Resumes...")
        except:
            links = pd.DataFrame()
            self.scrape_links()

        self.driver.close()        
        
        if links.size == 0:
            links = pd.read_excel(f"{self.file}.xlsx")['Links']

        if links.size > 10 and links.size < 20:
            num_processes = 2
        elif links.size <= 5:
            num_processes = 1
        else:
            num_processes = int(multiprocessing.cpu_count()) // 2
            num_processes += 2
        
        num_processes = 1
        
        if links.size == 0:
            print("No Links Found To Extract Data.....")
            return        

        url_chunks = self.chunk_list(links,num_processes)        
        instance = self.__class__()

        print("Relax Now ...Extracting Data From the Links.\n")

        with multiprocessing.Pool(processes=num_processes) as pool:            
            pool.starmap(instance.scrape_data, [(instance, url_chunk) for url_chunk in url_chunks])

        print("Extraction Completed\n")
        self.remove_file()
        self.clean_temp()
        # self.collateTemfiles()

    def clean_temp(self):
        temp_path = os.environ.get('TMP')
        temp_files  = os.listdir(temp_path)
        if temp_files:
            for file in temp_files:
                try:                  
                    if os.path.isdir(os.path.join(temp_path,file)):
                        shutil.rmtree(os.path.join(temp_path,file))
                    else:
                        os.remove(os.path.join(temp_path,file))
                except Exception as ex:
                    continue                   

    def collateTemfiles(self):
        list_of_xl_dataframe = list()
        path = os.path.join(os.getcwd(),'Data')
        list_dir = os.listdir(path)

        for file in list_dir:
            list_of_xl_dataframe.append(pd.read_excel(f"{path}/{file}"))
        
        col_xl = pd.concat(list_of_xl_dataframe,ignore_index=True)
        col_xl.to_excel(f"Data/{self.file}",index=False)

        shutil.rmtree(path=path)




