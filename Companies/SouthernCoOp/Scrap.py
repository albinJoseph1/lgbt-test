# Required Packages
import time

from Resource import htmlmin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
   def __init__(self, chrome, storage = None):
       super().__init__()
       self.chrome = chrome
       self.storage = storage
       self.jobs = []
       self.sourceJobCount = 0

       #     Company Details Start
       self.companyName = "Southern Co-op"
       self.ownerUsername = "southerncoop"
       self.scrapPageURL = "https://www.southernco-opjobs.co.uk/jobs/vacancy/find/results/ajaxaction/posbrowser_gridhandler/?movejump=1&movejump_page=1&pagestamp=d361d7ad-07c0-4bdc-911c-ab6a973b42f3"
       self.feedType = self.feedTypeWebScrap
       self.count = 1
       self.totalPages = ""
       #     Company Details End

   def loadScrapPage(self):
       self.chrome.getComplete(self.scrapPageURL)

       WebDriverWait(self.chrome, 100).until(
           EC.presence_of_element_located((By.CSS_SELECTOR, ".rowLabel"))
       )


   def nextPage(self):
       if int(self.count) == int(self.totalPages):
           return False
       else:
           self.count = self.count + 1
           self.scrapPageURL = "https://www.southernco-opjobs.co.uk/jobs/vacancy/find/results/ajaxaction/posbrowser_gridhandler/?movejump=1&movejump_page="+str(self.count)+"&pagestamp=d361d7ad-07c0-4bdc-911c-ab6a973b42f3"
           self.loadScrapPage()
           return True


   def loadJobs(self):

       self.loadScrapPage()
       totalPages = self.chrome.find_element_by_css_selector(".pagingText").text
       self.totalPages = totalPages.split("Page 1 of ")[1]

       try:

           while True:

               jobContainers = self.chrome.find_elements_by_css_selector(".ListGridContainer .rowContainerHolder")
               for jobContainer in jobContainers:
                   title = jobContainer.find_element_by_css_selector(".rowLabel").text
                   self.job.setTitle(title)

                   link = jobContainer.find_element_by_css_selector(".rowLabel a").get_attribute('href')
                   self.job.setLink(link)

                   self.job.setCompanyName(self.companyName)
                   self.job.setOwnnerUsername(self.ownerUsername)
                   self.addToJobs()

               if self.nextPage():
                   pass
               else:
                   break

           for currentJobIndex, job in enumerate(self.jobs):
               self.chrome.getComplete(job.getLink())

               descriptionProperties = self.chrome.find_elements_by_css_selector(".posdescriptionPropertyBox .jobSum .jobSumItem")
               for descriptionProperty in descriptionProperties:
                   propertyValue = descriptionProperty.text
                   if 'Salary' in propertyValue:
                       salary = propertyValue.split(":")[1]
                       salary = salary.replace('"', '')
                       self.jobs[currentJobIndex].setSalary(salary)
                       continue

                   if 'Location' in propertyValue:
                       location = propertyValue.split(":")[1]
                       self.jobs[currentJobIndex].setLocation(location)
                       continue

                   if 'Contract Type' in propertyValue:
                       contract = propertyValue.split(":")[1]
                       self.jobs[currentJobIndex].setContract(contract)
                       continue

               description = self.chrome.find_element_by_css_selector(".PosDescriptionText").get_attribute("innerHTML")
               self.jobs[currentJobIndex].setDescription(description)

           return True
       except:
           self.exceptionLogging()
           return False
