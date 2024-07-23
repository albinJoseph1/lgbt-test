# Required Packages
from datetime import datetime
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
        self.companyName = "Aston University"
        self.ownerUsername = "astonuniversity"
        self.scrapPageURL = "https://jobs.aston.ac.uk/vacancies.aspx?cat=-1"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL, True)
        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#maincontentwidgets #maincontent"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            container = self.chrome.find_element_by_css_selector("#maincontentwidgets #maincontent")
            jobContainers = container.find_elements_by_css_selector("ul li")
            for jobContainer in jobContainers:
                link = jobContainer.find_element_by_css_selector("a").get_attribute("href")
                self.job.setLink(link)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                WebDriverWait(self.chrome, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#maincontent"))
                )

                title = str(self.chrome.find_element_by_css_selector("#maincontent h1").text)
                self.jobs[currentJobIndex].setTitle(title)

                jobDetails = self.chrome.find_elements_by_css_selector(".advertdetailstable tbody tr")
                for detail in jobDetails:
                    if 'Location' in detail.text:
                        location = detail.find_element_by_css_selector("td:nth-child(2)").text
                        self.jobs[currentJobIndex].setLocation(location)
                    elif 'Closing Date' in detail.text:
                        expire = str(detail.find_element_by_css_selector("td:nth-child(2)").text)
                        expire = expire.split()
                        expire = expire[-3] + ' ' + expire[-2] + ' ' + expire[-1]
                        try:
                            expire = datetime.strptime(expire, '%d %B %Y').strftime('%Y-%m-%d')
                            self.jobs[currentJobIndex].setExpireDate(expire)
                        except Exception as e:
                            exception_message = str(title) + ' : ' + str(e) + "\n"
                            self.exceptionLogging('warning', exception_message)
                    elif 'Salary' in detail.text:
                        salary = detail.find_element_by_css_selector("td:nth-child(2)").text
                        self.jobs[currentJobIndex].setSalary(salary,"£(\d{1,3}(?:,\d{3})*) to £(\d{1,3}(?:,\d{3})*) per annum",is_salary_text=True)
                    elif 'Contract Type' in detail.text:
                        contract = detail.find_element_by_css_selector("td:nth-child(2)").text
                        self.jobs[currentJobIndex].setContract(contract) 

                elementsToRemove = []
                elementsToBeRemoved = ['table', 'h1', 'h4', 'style', '#divSocialMediaFacebook',
                                       '#divSocialMediaTwitter', '#divSocialMediaLinkedIn', 'img']
                for element in elementsToBeRemoved:
                    hasElement = bool(self.chrome.find_elements_by_css_selector("#maincontent " + element))
                    if hasElement:
                        elementObjects = self.chrome.find_elements_by_css_selector("#maincontent " + element)
                        for objectToRemove in elementObjects:
                            elementsToRemove.append(objectToRemove)
                hasViewAllLink = bool(self.chrome.find_elements_by_css_selector("#maincontent a:first-child"))
                if hasViewAllLink:
                    viewAllLink = self.chrome.find_element_by_css_selector("#maincontent a:first-child")
                    elementsToRemove.append(viewAllLink)

                self.sanitizeElementsForDescription(elementsToRemove)

                description = self.chrome.find_element_by_css_selector("#maincontent").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False
