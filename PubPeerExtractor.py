import io
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException,TimeoutException
import time


class PubPeerExtractor:
    
    def __init__(self,doisOrPmidsList: list,driverPath: str):

        self.doisOrPmidsList = doisOrPmidsList
        self.driver = webdriver.Firefox(executable_path=driverPath)
        self._bsInstanceDict = dict()

    def exTractFromPubpeer(self,WriteToFileSameTime: bool = False,saveScreenShot: bool = True)-> None:

        for item in self.doisOrPmidsList:
            
            print(" checking ===> ", item)
            try:
                self.driver.get(f"https://pubpeer.com/search?q={item}")
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'publication-list')))
            except WebDriverException as err:
                print(err)
            except TimeoutException as err:
                print(err)
                
            time.sleep(4)
            htmlSoupInstance = BeautifulSoup(self.driver.page_source, 'html.parser')
            self._bsInstanceDict[item] = htmlSoupInstance
            print(f"{item} ==> is ok")
            
            if  saveScreenShot:
                name = item.replace("/","-")
                self.driver.save_screenshot(f"./{name}.png")

    def writeToFile(self,fileName : str = "Results")-> None:
        try:
            with io.open(f"{fileName}.txt","a",encoding="utf-8") as file:
                for doi,html in self.bsInstanceDict.items():
                    elementList = html.find_all(class_='feedback')
                    if elementList:
                        line = "\t".join([doi,elementList[0].get_text()])
                        file.write(line)
                        print("Writing to file ... =>  "+ line)
                    
        except Exception as error:
            print(error)
            
    @property
    def results(self):
        return self._bsInstanceDict