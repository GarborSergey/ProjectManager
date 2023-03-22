import os
import shutil
import configparser
from datetime import datetime


# For TEST
BASE_DIR = 'C:\\Users\\Сергей\\PycharmProjects\\ProjectManager'
TEMPLATE_DIR = 'C:\\Users\\Сергей\\PycharmProjects\\ProjectManager\\template_files'


# custom error class
class ProjectManagerError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f'{self.message}' if self.message else ''


class Project:
    def __init__(self, name, counterparty, path, templatePath):
        self.__name = self.convert_string(name)
        self.__counterparty = self.convert_string(counterparty)
        self.__dateCreate = datetime.now()
        self.__dateModification = datetime.now()

        self.__create_project(path, templatePath)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise ProjectManagerError('Project name must be type of STRING')

        self.__name = self.convert_string(name)

    @property
    def counterparty(self):
        return self.__counterparty

    @counterparty.setter
    def counterparty(self, counterparty):
        if not isinstance(counterparty, str):
            raise ProjectManagerError('Counterparty name must be type of STRING')

        self.__counterparty = self.convert_string(counterparty)

    @staticmethod
    def convert_string(string: str):
        return string.replace(' ', '_')

    # path is a global BASE_DIR that in config app
    def __create_project(self, path, templatePath):
        pathCounterparty = path + os.sep + self.__counterparty  # path to Counterparty dir
        pathProject = pathCounterparty + os.sep + self.__name  # path to Project dir

        # if counterparty folder not exists create else None
        if not os.path.exists(pathCounterparty):
            os.mkdir(pathCounterparty)

        # if project in counterparty folder not exists create else ERROR
        if not os.path.exists(pathProject):
            os.mkdir(pathProject)
        else:
            raise ProjectManagerError(f'A project with this name "{self.__name}" already exists\n'
                                      f'path: {pathProject}')

        # create empty folder for source project raw
        os.mkdir(pathProject + os.sep + f'!исходный_проект_{self.__name}')
        # copy and rename template files
        shutil.copy2(templatePath + os.sep + 'TEMPLATE.dwg', pathProject + os.sep + f'внешний_вид_{self.__name}.dwg')

    # create INI file with all params of project
    def __create_infoINI_file(self, path):
        pass


if __name__ == '__main__':
    p = Project('Test Project Name', 'Test Counterparty Name', BASE_DIR, TEMPLATE_DIR)
