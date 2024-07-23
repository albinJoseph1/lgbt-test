# Required Packages
from datetime import datetime
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
        self.companyName = "NHS Liverpool University Hospitals"
        self.ownerUsername = "nhsliverpooluniversityhospitals"
        self.currencyType = "Euro"
        self.location = "Liverpool"
        self.scrapPageURL = "https://www.liverpoolft.nhs.uk/working-with-us/current-opportunities/"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        hasCookie = bool(self.chrome.find_elements_by_id("cookieBannerButton"))
        if hasCookie:
            cookieAccept = WebDriverWait(self.chrome, 100).until(
                EC.presence_of_element_located((By.ID, "cookieBannerButton"))
            )
            cookieAccept.click()

    def loadJobs(self):
        self.loadScrapPage()
        categoryLinks = []
        listingAllLinks = []
        try:
            categories = WebDriverWait(self.chrome, 100).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#hj-select-sector .clearfix li"))
            )

            for category in categories:
                linkElement = WebDriverWait(category, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li > a:first-child"))
                )
                categoryLink = linkElement.get_attribute('href')
                categoryLinks.append(categoryLink)

            for categoryLink in categoryLinks:
                self.chrome.getComplete(categoryLink)
                jobLinks = WebDriverWait(self.chrome, 100).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#hj-job-list > ol > li.hj-job"))
                )


                for jobLink in jobLinks:

                  noRestictionsApply = not bool(jobLink.find_elements_by_css_selector(
                          'a .hj-job-details .hj-eligibility-note.hj-warning'))
                  if noRestictionsApply:
                        applyLinkElement = WebDriverWait(jobLink, 100).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "li.hj-job > a:first-child"))
                        )
                        applyLink = applyLinkElement.get_attribute('href')
                        applyLink = applyLink.split('?')
                        newApplyLink = applyLink[0]
                        listingAllLinks.append(newApplyLink)
                        self.job.setLink(newApplyLink)

                        hasSalary = bool(jobLink.find_elements_by_css_selector('.hj-salary.hj-job-detail'))
                        if hasSalary:
                            salary = jobLink.find_element_by_css_selector('.hj-salary.hj-job-detail').get_attribute('title')
                            salary = salary.replace("Salary:", "")
                            self.job.setSalary(salary)

                        location = self.location
                        self.job.setLocation(location)
                        self.job.setSalaryCurrency(self.currencyType)
                        salaryHour = None
                        self.job.setSalaryPerHour(salaryHour)
                        postedDate = None
                        self.job.setPostedDate(postedDate)
                        self.job.setCompanyName(self.companyName)
                        self.job.setOwnnerUsername(self.ownerUsername)

                        self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                self.chrome.pageWait()

                elementsToRemove = []
                elementsTobeRemoved = ['.hj-employer-icons', '#hj-vacancy-docs',
                                       '.hj-apply-online.hj-button.hj-primary', '#hj-enquiry-html']
                for element in elementsTobeRemoved:
                    hasElementPresent = bool(self.chrome.find_elements_by_css_selector(element))
                    if hasElementPresent:
                        elementsToRemove.append(self.chrome.find_element_by_css_selector(element))
                self.sanitizeElementsForDescription(elementsToRemove)

                hasExpireDate = bool(self.chrome.find_elements_by_css_selector(
                    '.card-body > .row > div:last-child > dl.front-end-job-summary  dd.field-value:last-child'))
                if hasExpireDate:
                    expire = self.chrome.find_element_by_css_selector(
                        '.card-body > .row > div:last-child > dl.front-end-job-summary  dd.field-value:last-child').text
                    try:
                        expire = datetime.strptime(expire, '%d/%m/%Y %H:%M')
                        expire = expire.strftime('%Y-%m-%d')
                        self.jobs[currentJobIndex].setExpireDate(expire)
                    except Exception as e:
                        exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                description = self.chrome.find_element_by_xpath('//*[@id="hj-job"]/div[2]').get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

                title = self.chrome.find_element_by_xpath('//*[@id="hj-job"]/div[1]/h2').text
                self.jobs[currentJobIndex].setTitle(title)

                contract = self.chrome.find_element_by_xpath('//*[@id="hj-job-summary"]/div/div/div/div[1]/dl/dd[3]').text
                self.jobs[currentJobIndex].setContract(contract)


            return True

        except:
            self.exceptionLogging()
            return False

