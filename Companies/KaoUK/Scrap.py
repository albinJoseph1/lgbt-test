
import os

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
        self.companyName = "Kao UK"
        self.ownerUsername = ""
        self.scrapPageURL = ""
        self.subAgents = []

        self.feedType = self.feedTypeWebScrap

        self.subCompaniesModulePath = str(os.path.dirname(__file__))+"/SubAgents"
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
                exec("from Companies.KaoUK.SubAgents."+agentModuleName+".Scrap import Agent as "+agentClassName)
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