import logging
from ..LibFrame import applicationDict
from ..Objects.Project import Project
class InformationHandler(object):
    

    def createProject(self,projectdict):
        project_result=False
        if projectdict['project_name']=="":
            return project_result
        
        if projectdict['project_site']=="":
            return project_result

        if projectdict['project_country']=="":
            return project_result

        if projectdict['project_environment']=="":
            return project_result

        if projectdict['projekt_type']=="":
            return project_result

        if projectdict['projekt_application']=="":
            return project_result

        newproject=Project(project_name = projectdict['project_name'],
                            project_site = projectdict['project_site'],
                            project_country = projectdict['project_country'],
                            project_environment = projectdict['project_environment'],
                            project_description = projectdict['project_description'],
                            projekt_type= projectdict['projekt_type'],
                            projekt_application= projectdict['projekt_application'],
                            projekt_site_id=projectdict['projekt_site_id'])
        project=applicationDict['dbconn'].addProject(newproject)

        try:
            if project.project_id>0:
                project_result=True
        except Exception as e:
            logging.error("create project failed:"+str(e)+" "+str(projectdict))
        
        return project_result

        
        