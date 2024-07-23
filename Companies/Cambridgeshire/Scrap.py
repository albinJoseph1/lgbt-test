# Required Packages
from datetime import datetime
from Resource import htmlmin
import time
from urllib import parse
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
        self.companyName = "Cambridgeshire County Council"
        self.ownerUsername = "cambridgeshirecountycouncil"
        self.scrapPageURL = "https://www.publicsectorjobseast.co.uk/pages/Job_Search_Results.aspx?categoryList=&minsal=0&maxsal=200000&workingpattern=&keywords=&employee=1&postcode=&Distance=20&AdvertiseOn=2&SortBy=title&SortDir=DESC&Pagesize=1000&pageIndex=1"
        self.feedType = self.feedTypeWebScrap
        self.maxScrapPageLimit = 20
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        hasCookie = bool(self.chrome.find_elements_by_css_selector(".cc-cookies"))
        if hasCookie:
            cookieClose = self.chrome.find_element_by_css_selector(".cc-cookie-accept").click()
        time.sleep(1)
        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#searchresults"))
        )

    # Scraper Function
    def loadJobs(self):
        try:
            self.loadScrapPage()
            jobContainers = self.chrome.find_elements_by_css_selector("#newResults #new_search_results tbody tr")
            for jobContainer in jobContainers:
                title = str(jobContainer.find_element_by_css_selector("td:first-child a.jobTitleLink").text)
                title = title.strip()
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector("td:first-child a.jobTitleLink").get_attribute('href')
                link = self.sanitizeJobUrl(link)
                self.job.setLink(link)

                jobLocation = jobContainer.find_element_by_css_selector("td:last-child span").text
                self.job.setLocation(jobLocation)

                salary = jobContainer.find_element_by_css_selector("td:nth-child(3) span").text
                self.job.setSalary(salary)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                noPageError = bool(self.chrome.find_elements_by_css_selector("#mainSection"))
                if noPageError:
                    summeries = self.chrome.find_element_by_css_selector("#Vsummary")
                    jobSummeries = summeries.find_elements_by_css_selector(".table-container .flex-table-row .flex-row")
                    dateFlag = 0
                    for jobSummery in jobSummeries:
                        if dateFlag:
                            closingDate = jobSummery.find_element_by_css_selector("span").text
                            closingDate = closingDate.split(' at')
                            try:
                                expireDate = datetime.strptime(closingDate[0], '%d %B %Y').strftime('%Y-%m-%d')
                                self.jobs[currentJobIndex].setExpireDate(expireDate)
                            except Exception as e:
                                exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                                self.exceptionLogging('warning', exception_message)
                            break;
                        hasClosingDate = bool(jobSummery.find_elements_by_css_selector(".vacancy-closing-date"))
                        if hasClosingDate:
                            dateFlag = 1

                    self.sanitizeElementsForDescription()

                    descriptionElement = self.chrome.find_element_by_css_selector("#jobdesc")
                    description = descriptionElement.get_attribute('innerHTML')
                    description = description.replace("\n","")
                    self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

    def sanitizeJobUrl(self, jobLink):
        jobLinkWithoutVariables = jobLink.split('?')[0]
        urlVariables = parse.parse_qs(parse.urlsplit(jobLink).query)
        urlVariable =  parse.urlencode({'jobId': urlVariables['jobId'][0]})
        jobLink = jobLinkWithoutVariables + '?' + urlVariable
        return jobLink
