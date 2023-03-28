import os
import shutil
import configparser
from datetime import datetime


# For TEST
BASE_DIR = 'C:\\Users\\Сергей\\PycharmProjects\\ProjectManager'
TEMPLATE_DIR = 'C:\\Users\\Сергей\\PycharmProjects\\ProjectManager\\template_files'


def logger():
    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            print(f'\nSTART a function {func.__name__} time - {str(datetime.now())}')
            try:
                func(*args, **kwargs)
            except ProjectManagerError as e:
                print(f'EXCEPTION {func.__name__} - {e} time - {str(datetime.now())}')
            except FileExistsError as e:
                print(f'EXCEPTION {func.__name__} - {e} - {str(datetime.now())}')
            else:
                print(f'Successful END a function {func.__name__} time - {str(datetime.now())}')
        return wrapper
    return actual_decorator


# custom error class
class ProjectManagerError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f'{self.message}' if self.message else ''


class Project:
    def __init__(self, name, counterparty, comment=None):
        self.__name = self.convert_string(name)
        self.__counterparty = self.convert_string(counterparty)
        self.__dateCreate = datetime.now()
        self.__dateModification = datetime.now()
        self.__comment = comment

    @staticmethod
    def convert_string(string: str):
        return string.replace(' ', '_')

    # path is a global BASE_DIR that in config app
    @logger()
    def create_project(self, path, templatePath):
        """
        Create empty folders fo projects and copy AutoCad dwg file
        :param path: base dir for projects
        :param templatePath: dir with files of templates
        :return: None
        """
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

        self.__create_message_for_log(f'run create_project with path - {path}, templatePath - {templatePath}', path)

        # create empty folder for source project raw
        os.mkdir(pathProject + os.sep + f'!исходный_проект_{self.__name}')
        os.mkdir(pathProject + os.sep + f'дополненеия_{self.__name}')
        os.mkdir(pathProject + os.sep + f'печать_{self.__name}')
        # copy and rename template file for AutoCad
        shutil.copy2(templatePath + os.sep + 'TEMPLATE.dwg', pathProject + os.sep + f'внешний_вид_{self.__name}.dwg')

        self.__create_config_file(pathProject)
        self.__create_comment_file(pathProject)

    # create INI file with all params of project
    @logger()
    def __create_config_file(self, path):
        """
        Create a config file
        :param path: path to create config file
        :return: None
        """
        pathCounterparty = path + os.sep + self.__counterparty  # path to Counterparty dir
        pathProject = pathCounterparty + os.sep + self.__name  # path to Project dir

        config = configparser.ConfigParser()
        config.add_section('ProjectSettings')
        config.set('ProjectSettings', 'name', self.__name)
        config.set('ProjectSettings', 'counterparty', self.__counterparty)
        config.set('ProjectSettings', 'dateCreate', str(self.__dateCreate))
        config.set('ProjectSettings', 'dateModification', str(self.__dateModification))
        config.set('ProjectSettings', 'pathProject', pathProject)

        with open(path + os.sep + f'{self.__name}_config.ini', 'w') as configFile:
            config.write(configFile)

    @logger()
    def __create_comment_file(self, path):
        """
        Create comment .txt file
        :param path: path to create comment file
        :return: None
        """
        with open(path + os.sep + f'comment_{self.__name}.txt', 'w') as commentFile:
            commentFile.write(f'Project - {self.__name}\nCounterparty - {self.__counterparty}\n')
            if self.__comment:
                commentFile.write(self.__comment)

    @logger()
    def put_the_project_into_work(self, path, templatePath):
        """
        Create files in project dir for work
        :param path: base dir for projects
        :param templatePath: dir with files of templates
        :return: None
        """
        pathCounterparty = path + os.sep + self.__counterparty  # path to Counterparty dir
        pathProject = pathCounterparty + os.sep + self.__name  # path to Project dir

        self.__dateModification = datetime.now()

        self.__create_config_file(pathProject)

        # create empty folder for making files
        os.mkdir(pathProject + os.sep + f'маркировка_{self.__name}')

        # create empty folder for specification of boxes
        os.mkdir(pathProject + os.sep + f'наборки_{self.__name}')

        # create empty folder for passports
        os.mkdir(pathProject + os.sep + f'паспорта_{self.__name}')

        # copy all files from template_files/marking
        for root, dirs, files in os.walk(templatePath + os.sep + 'marking'):
            for fileName in files:
                shutil.copy(templatePath + os.sep + 'marking' + os.sep + fileName, pathProject + os.sep + f'маркировка_{self.__name}')

        # copy AutoCad file dwg for electrical diagrams
        shutil.copy2(templatePath + os.sep + 'TEMPLATE.dwg', pathProject + os.sep + f'схемы_{self.__name}.dwg')

    @logger()
    def __create_message_for_log(self, message, path):
        """
        Create and write message to file log.txt for curr project
        :param message: text message to log
        :param path: path to BASE_DIR
        :return: None
        """

        pathCounterparty = path + os.sep + self.__counterparty  # path to Counterparty dir
        pathProject = pathCounterparty + os.sep + self.__name  # path to Project dir

        if not os.path.exists(pathProject + os.sep + 'log.txt'):
            with open(pathProject + os.sep + 'log.txt', 'w') as logFile:
                logFile.write(f'logs create at {str(datetime.now())}\nProject - {self.__name}\nCounterparty - {self.__counterparty}\n')

        with open(pathProject + os.sep + 'log.txt', 'a') as logFile:
            logFile.write(f'{message} time - {str(datetime.now())}')


if __name__ == '__main__':
    p = Project('Test Project Name', 'Test Counterparty Name', 'Test comment test comment')
    p.create_project(BASE_DIR, TEMPLATE_DIR)
    p.put_the_project_into_work(BASE_DIR, TEMPLATE_DIR)
