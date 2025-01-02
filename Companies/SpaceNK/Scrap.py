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
        self.companyName = "Space NK"
        self.ownerUsername = "spacenk"
        self.scrapPageURL = "https://spacenk.teamtailor.com/jobs.rss"
        self.location = 'United Kingdom'
        self.feedType = self.feedTypeXML
        self.maxScrapPageLimit = 20
        #     Company Details End


    def loadScrapPage(self):
        pass

    def loadXML(self):
        with urlopen(self.scrapPageURL) as xml:
            tree = ET.parse(xml)
            self.jobsContainer = tree.getroot().find('channel')

    def loadJobs(self):
        self.loadXML()
        try:
            for job in self.jobsContainer.findall('item'):
                namespaces = {'tt': 'https://teamtailor.com/locations'}
                location = job.find('.//tt:location', namespaces)
                if location is not None:
                    country = location.find('tt:country', namespaces).text
                    if self.location in country:
                        streetName = location.find('tt:name', namespaces)
                        city = location.find('tt:city', namespaces)
                        compinedLocation = ''
                        if streetName.text != None:
                            compinedLocation = compinedLocation + streetName.text +','
                        if city.text != None:
                            compinedLocation = compinedLocation + city.text +','
                        if country != None:
                            compinedLocation = compinedLocation + country

                        self.job.setLocation(compinedLocation)
                        isJobExists = True
                else:
                    isJobExists = True

                if isJobExists:
                    title = job.find('title').text
                    self.job.setTitle(title)

                    apply_link = job.find('link').text
                    self.job.setLink(apply_link)

                    description = job.find('description').text
                    self.job.setDescription(description)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

            return True
        except:
            self.exceptionLogging()
            return False
        