# Required Packages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from Companies.StandardAgent import ScrapAgent

import requests
from urllib3 import poolmanager
from Resource import htmlmin
import ssl
import xml.dom.minidom


class Agent(ScrapAgent):
    def __init__(self, chrome, storage=None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "QBE Insurance Group Limited"
        self.ownerUsername = "qbeinsurancegroup"
        self.scrapPageURL = "https://qbe.wd3.myworkdayjobs.com/QBE-Careers/siteMap.xml"
        self.feedType = self.feedTypeWebScrap
        self.jobLinks = []
        self.locationFilters = ['United Kingdom','GBR']
        self.location = 'United Kingdom'
        #     Company Details End

    def loadScrapPage(self):
        pass

    def loadXML(self):
        url = self.scrapPageURL
        class TLSAdapter(requests.adapters.HTTPAdapter):

            def init_poolmanager(self, connections, maxsize, block=False):
                # Create and initialize the urllib3 PoolManager.
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
        self.loadXML()

        try:
            xmlparse = xml.dom.minidom.parseString(self.XML)

            jobContainers = xmlparse.getElementsByTagName('url')
            for jobContainer in jobContainers:
                link = jobContainer.getElementsByTagName('loc')[0].firstChild.nodeValue
                self.jobLinks.append(link)

            for link in self.jobLinks:
                self.chrome.getComplete(link)
                self.job.setLink(link)

                location = None
                hasLocation = bool(self.chrome.find_elements_by_css_selector("[data-automation-id='locations']"))

                hasLocationFilter = False
                locationOuters = self.chrome.find_elements_by_css_selector("[data-automation-id='locations'] dd")

                for locationOuter in locationOuters:
                    location = locationOuter.text
                    # print(location)

                    for locationFilter in self.locationFilters:
                        if locationFilter in location:
                            hasLocationFilter = True
                            # location = location.split('locations')[1]
                            break

                if hasLocation and hasLocationFilter:

                    self.job.setLocation(self.location)

                    title = self.chrome.find_element_by_css_selector("[data-automation-id='jobPostingHeader']").text
                    self.job.setTitle(title)

                    self.sanitizeElementsForDescription()

                    description = self.chrome.find_element_by_css_selector(
                        "[data-automation-id='jobPostingDescription']").get_attribute("innerHTML")
                    self.job.setDescription(description)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()


            return True

        except:
            self.exceptionLogging()
            return False