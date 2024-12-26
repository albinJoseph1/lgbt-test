# Required Packages
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
        self.companyName = "Teach First"
        self.ownerUsername = "teachfirst"
        self.scrapPageURL = "https://www.teachfirst.org.uk/working-teach-first/vacancies"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, ".view-featured-content"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector(".view-featured-content .views-row")
            for jobContainer in jobContainers:
                title = jobContainer.find_element_by_css_selector(".vacancies-title").text
                title = title.strip()
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector(".vacancies-apply a").get_attribute("href")
                self.job.setLink(link)

                location = jobContainer.find_element_by_css_selector(".vacancies-info--description > div:nth-child(2) > span:nth-child(2)").text
                self.job.setLocation(location)

                salary = jobContainer.find_element_by_css_selector(".vacancies-info--description > div:nth-child(3) > span:nth-child(2)").text
                self.job.setSalary(salary, "£?(\d+(?:,?|:\.)\d+)",is_salary_text=True)

                expireDate = jobContainer.find_element_by_css_selector(".vacancies-info--description > div:nth-child(1) > span:nth-child(2)").text
                possibleExpiryDateFormats = [
                    "%d %B %Y"
                ]
                for possibleExpireDate in possibleExpiryDateFormats:
                    try:
                        expireDate = datetime.strptime(expireDate, possibleExpireDate).strftime('%Y-%m-%d')
                        print(expireDate)
                        self.job.setExpireDate(expireDate)
                    except Exception as e:
                        exception_message = str(title) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector(".detailList table div").get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False