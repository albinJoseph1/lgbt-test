# Required Packages
from datetime import datetime
from Resource import htmlmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import pathlib

from Managers import environmentManager
from Companies.StandardAgent import ScrapAgent

class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()


        self.chrome = chrome
        self.storage = storage
        self.jobs = {}
        self.sourceJobCount = 0
        self.agents = []
        self.subAgentsLoaded = 0

        #     Company Details Start
        self.companyName = "Sega"
        self.ownerUsername = ""
        self.scrapPageURL = ""
        self.subAgents = []

        self.feedType = self.feedTypeWebScrap
        self.subCompaniesModulePath = str( pathlib.Path(__file__).parent.absolute() )+"/SubAgents"
        self.subCompaniesModulePath = environmentManager.formatPath(self.subCompaniesModulePath)
        self.hasSubAgents = True
        #     Company Details End

    def getCompanyName(self):
        return self.companyName

    def getFeedType(self):
        return self.feedType

    def getFeedUrl(self):
        return self.scrapPageURL

    def getSourceJobCount(self):
        return 0

    def getScrapedJobCount(self):
        return len(self.jobs)

    def getOwnerUsername(self):
        return self.ownerUsername

    def loadScrapPage(self):
        pass

    def loadSubAgents(self):

        #code to init all sub agents in subAgent module
        agentModulePaths = [name for name in os.listdir(self.subCompaniesModulePath) if os.path.isdir(os.path.join(self.subCompaniesModulePath, name))]
        for agentModuleName in agentModulePaths:
            initedAgent = None
            try:
                agentClassName = agentModuleName+"Agent"
                exec("from Companies.Sega.SubAgents."+agentModuleName+".Scrap import Agent as "+agentClassName)
                initedAgent = eval(agentClassName+"(self.chrome)")

                self.subAgents.append(initedAgent)
            except ModuleNotFoundError:
                pass

        self.subAgentsLoaded = self.subAgents.__len__()

    def loadJobs(self):
        self.loadSubAgents()
        try:
            for subAgent in self.subAgents:
                subAgent.loadJobs()
                self.addSubAgentJobs(subAgent)
            return True

        except:
            self.exceptionLogging()
            return False

    def addSubAgentJobs(self, subAgent):
        self.jobs[subAgent.getCompanyName()] = subAgent.jobs