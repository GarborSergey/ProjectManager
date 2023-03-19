from datetime import datetime


class Project:
    def __init__(self, name: str, counterparty: str):
        self.name = name
        self.counterparty = counterparty
        self.dateCreate = datetime.now()

    def rename_project(self, new_name: str):
        self.name = new_name

    def rename_counterparty(self, new_name: str):
        self.counterparty = new_name


if __name__ == '__main__':
    pass
