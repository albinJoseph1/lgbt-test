# Required Packages
from datetime import datetime
from Resource import htmlmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
from urllib3 import poolmanager
from Resource import htmlmin
import ssl
import xml.dom.minidom
from Managers import lgbtManager
from Objects import Job

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = {}
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Admiral"
        self.ownerUsername = "admiral"
        self.siteSpecificJobs = True
        self.ScrapPageURL = {
            lgbtManager.site.LGBT : "https://apply.admiraljobs.co.uk/xmlfeeds/lgbt.xml",
            lgbtManager.site.BME : "https://apply.admiraljobs.co.uk/xmlfeeds/bme.xml",
            lgbtManager.site.DISABILITY : "https://apply.admiraljobs.co.uk/xmlfeeds/disability.xml"
        }
        self.feedType = self.feedTypeXML
        #     Company Details End

    def loadScrapPage(self):
        pass

    def loadXML(self,scrapPageURL):

        url = scrapPageURL
        class TLSAdapter(requests.adapters.HTTPAdapter):

            def init_poolmanager(self, connections, maxsize, block=False):
                """Create and initialize the urllib3 PoolManager."""
                ctx = ssl.create_default_context()
                ctx.set_ciphers('DEFAULT@SECLEVEL=1')
                self.poolmanager = poolmanager.PoolManager(
                    num_pools=connections,
                    maxsize=maxsize,
                    block=block,
                    ssl_version=ssl.PROTOCOL_TLS,
                    ssl_context=ctx)
        tls = TLSAdapter()
        session = requests.session()
        session.mount('https://', TLSAdapter())
        responce = session.get(url)
        self.XML = responce.text

    def loadJobs(self):
        try:
            for sitePageUrl in self.ScrapPageURL.keys():
                jobsForSite = []
                self.loadXML(self.ScrapPageURL[sitePageUrl])
                xmlparse = xml.dom.minidom.parseString(self.XML)
                jobContainers = xmlparse.getElementsByTagName('job')

                for jobContainer in jobContainers:
                    link = jobContainer.getElementsByTagName('url')[0].firstChild.nodeValue
                    self.job.setLink(link)

                    title = jobContainer.getElementsByTagName('title')[0].firstChild.nodeValue
                    self.job.setTitle(title)

                    location = None
                    hasLocation = bool(jobContainer.getElementsByTagName('location')[0].firstChild)
                    if hasLocation:
                        location = jobContainer.getElementsByTagName('location')[0].firstChild.nodeValue
                    self.job.setLocation(location)

                    salary = None
                    hasSalary = bool(jobContainer.getElementsByTagName('salary')[0].firstChild)
                    if hasSalary:
                        salary_node = jobContainer.getElementsByTagName('salary')[0].firstChild
                        if salary_node is not None:
                            salary = salary_node.nodeValue

                    self.job.setSalary(str(salary))

                    hasExpireDate = bool(jobContainer.getElementsByTagName('external_closing_date')[0].firstChild)
                    if hasExpireDate:
                        expireDate = jobContainer.getElementsByTagName('external_closing_date')[0].firstChild.nodeValue
                        try:
                            expireDate = datetime.strptime(expireDate, '%d/%m/%Y')
                            expireDate = expireDate.strftime('%Y-%m-%d')
                            self.job.setExpireDate(expireDate)
                        except Exception as e:
                            exception_message = str(self.job.getTitle()) + ' : ' + str(e) + "\n"
                            self.exceptionLogging('warning', exception_message)

                    hasAdvert = bool(jobContainer.getElementsByTagName('job_advert'))
                    hasDescription = bool(jobContainer.getElementsByTagName('job_description'))
                    if hasAdvert:
                        description = jobContainer.getElementsByTagName('job_advert')[0].firstChild.nodeValue
                    elif hasDescription:
                        description = jobContainer.getElementsByTagName('job_description')[0].firstChild.nodeValue
                    self.job.setDescription(description)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    jobsForSite.append(self.job)
                    self.job = Job()

                self.jobs[sitePageUrl] = jobsForSite

            return True
        except:
            self.exceptionLogging()
            return False
