# Required Packages
from datetime import datetime
from Resource import htmlmin
import datetime

from Companies.StandardAgent import ScrapAgent

class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0
        #     Company Details Start
        self.companyName = "Milton Keynes College"
        self.ownerUsername = "sallyrollings"
        self.scrapPageURL = ['https://www.mkcollege.ac.uk/prison-services/vacancies/', 'https://www.mkcollege.ac.uk/working-for-us/vacancies/']
        self.feedType = self.feedTypeWebScrap
        self.jobKey = 'title'
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

    # Scraper Function
    def loadJobs(self):
        jobsCount = 0
        try:
            for scrapPageURL in self.scrapPageURL:
                self.chrome.getComplete(scrapPageURL)
                jobLinkElements = self.chrome.find_elements_by_css_selector(".vacancy .wp-block-button > a")
                jobLinks = []
                for jobLinkElement in jobLinkElements:

                    jobLinks.append(jobLinkElement.get_attribute('href'))

                jobsCount += len(jobLinks)

                for jobLink in jobLinks:
                    self.chrome.getComplete(jobLink)

                    title = self.chrome.find_element_by_css_selector("table.form tbody tr td > h1").text
                    self.job.setTitle(title)
                    # Exclude jobs having 'INTERNAL APPLICATIONS ONLY' in the title
                    if 'INTERNAL APPLICANTS ONLY' in title:
                        jobsCount -= 1
                        continue

                    link = jobLink
                    self.job.setLink(link)

                    expireDate = self.chrome.execute_script('''
                			expireDateString = jQuery("#dlAdvertDetails table.form tbody tr:eq(2) td:eq(1)").text();
                			return expireDateString
                	''')
                    expireDate = expireDate.strip()
                    try:
                        expireDate = datetime.datetime.strptime(expireDate, '%H:%M, %d %B %Y').strftime('%Y-%m-%d')
                        self.job.setExpireDate(expireDate)
                    except Exception as e:
                        exception_message = str(title) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                    location = self.chrome.execute_script('''
                			expireDateString = jQuery("#dlAdvertDetails table.form tbody tr:eq(3) td:eq(1)").text();
                			return expireDateString
                	''')
                    location = location.strip()
                    self.job.setLocation(location)

                    self.sanitizeElementsForDescription()

                    descriptionElement = self.chrome.find_element_by_css_selector("table.form tbody tr.description td")
                    description = descriptionElement.get_attribute('innerHTML')
                    description = description.strip()
                    self.job.setDescription(description)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False