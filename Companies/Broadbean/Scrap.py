# Required Packages
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from Companies.StandardAgent import ScrapAgent
from Objects import Job
from datetime import datetime


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = {}
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Broadbean"
        self.ownerUsername = "broadbean"
        self.scrapPageURL = "https://batchaws.adcourier.com/services/?q=U2FsdGVkX1_9iO663cW-l5pDDvbxWpXe1ek2ReM3VRzva_F4iw3mtM9oEBTy0Hr1"
        self.feedType = self.feedTypeXML
        self.hasSubAgents = True
        self.mixedAgentsJobs = True
        self.hasCompanyNameConversion = True
        self.scrapType = self.feedType
        self.userEmails = {}
        self.endpointUrl = self.scrapPageURL
        self.ignoredCompanies = ["DHL Supply Chain"]
        #     Company Details End

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

                if job.find('application_url').text is None:
                    self.exceptionLogging('warning', "Skipping job: " + job.find('job_title').text.strip())
                    continue
                else:
                    link = job.find('application_url').text.strip()

                    companyName = job.find("company_name").text.strip()

                    if companyName in self.ignoredCompanies:
                        continue

                    self.job.setCompanyName(companyName)

                    userName = job.find("user_name").text.strip()
                    self.job.setOwnnerUsername(userName)

                    userEmail = job.find("user_email").text
                    if userEmail is not None:
                        userEmail = userEmail.strip()
                        self.userEmails[userName] = userEmail

                    title = job.find('job_title').text.strip()
                    self.job.setTitle(title)

                    location = job.find('job_location').text.strip()

                    description = job.find('job_description').text.strip()

                    contract = job.find('job_contract').text.strip()

                    expireDate = job.find("job_expiry_date").text.strip()
                    possibleExpiryDateFormats = [
                        "%d-%m-%Y",
                        "%y-%m-%d"
                    ]
                    for possibleExpireDate in possibleExpiryDateFormats:
                        try:
                            expireDate = datetime.strptime(expireDate, possibleExpireDate).strftime('%Y-%m-%d')
                            self.job.setExpireDate(expireDate)
                        except Exception as e:
                            exception_message = str(title) + ' : ' + str(e) + "\n"
                            self.exceptionLogging('warning', exception_message)

                    salary = job.find("salary").text.strip()

                    self.job.setTitle(title)

                    self.job.setLink(link)

                    self.job.setLocation(location)

                    self.job.setContract(contract)

                    self.job.setDescription(description)

                    self.job.setSalary(salary)

                    try:
                        self.jobs[companyName].append(self.job)
                    except:
                        self.jobs[companyName] = []
                        self.jobs[companyName].append(self.job)

                    self.job = Job()

            return True
        except:
            self.exceptionLogging()
            return False