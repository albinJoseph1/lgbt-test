# Required Packages
from urllib.request import urlopen

import xml.etree.ElementTree as ET



from Companies.StandardAgent import ScrapAgent

class Agent(ScrapAgent):
    def __init__(self, storage = None):
        super().__init__()
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0
        self.XML = None

        #Company Details Start
        self.companyName = "Volkswagen Group United Kingdom Ltd"
        self.ownerUsername = "volkswagen"
        self.scrapPageURL = "https://uk.idibu.com/clients/board_scripts/lgbtjobs/lgbtjobs.xml"
        self.feedType = self.feedTypeXML
        self.maxScrapPageLimit = 20
          # Company Details End



    def loadScrapPage(self):
        pass

    def loadXML(self):
        with urlopen(self.scrapPageURL) as xml:
            tree = ET.parse(xml)
            self.jobsContainer = tree.getroot()


    # Scraper Function
    def loadJobs(self):
        self.loadXML()
        try:
            for job in self.jobsContainer.findall('job'):
                company = job.find('contact/company').text
                if('Volkswagen' in company):

                    apply_link = job.find('application_url').text
                    self.job.setLink(apply_link)

                    title = job.find('title').text
                    self.job.setTitle(title)

                    description = job.find('description').text
                    self.job.setDescription(description)

                    location = job.find('location').text
                    self.job.setLocation(location)

                    min_salary = str(job.find('salary/min').text)
                    max_salary = str(job.find('salary/max').text)
                    salary = min_salary + "-" + max_salary
                    self.job.setSalary(salary)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False
