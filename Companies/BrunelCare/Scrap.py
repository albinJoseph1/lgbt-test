# Required Packages
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from datetime import datetime

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Brunel Care"
        self.ownerUsername = "brunelcare"
        self.scrapPageURL = "https://brunelcare.current-vacancies.com/RSSFeeds/Vacancies/BRUNELCARE?feedID=DB81F04E6FA54C83A71ADA3C8DE9BF7F"
        self.feedType = self.feedTypeXML
        #     Company Details End

    def loadScrapPage(self):
        pass

    def loadXML(self):
        with urlopen(self.scrapPageURL) as xml:
            tree = ET.parse(xml)
            self.jobsContainer = tree.getroot().find('channel')

    # Scraper Function
    def loadJobs(self):
        self.loadXML()
        try:
            for job in self.jobsContainer.findall('item'):
                title = job.find('title').text
                self.job.setTitle(title)

                apply_link = job.find('link').text
                self.job.setLink(apply_link)

                a10NameSpace = {'a10': 'http://www.w3.org/2005/Atom'}
                jobContent = job.find('a10:content', a10NameSpace)

                description = jobContent.find('Vacancy/vAdvertText').text
                if description is not None:
                    self.job.setDescription(description)

                location = jobContent.find('Vacancy/vLocation').text
                self.job.setLocation(location)

                expire = jobContent.find('Vacancy/vExpiryDate').text
                expire = expire.split()[0]
                expire = datetime.strptime(expire, '%d/%m/%Y').strftime('%Y-%m-%d')
                self.job.setExpireDate(expire)

                salary = jobContent.find('Vacancy/vSalary').text
                self.job.setSalary(salary)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False
