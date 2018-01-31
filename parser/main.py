import json

import requests
from bs4 import BeautifulSoup

LIST_OF_TYPES = [
    "zku",
    "phone",
    "internet",
    "tv",
    "games",
    "online",
    "fin",
    "chat",
    "charity",
    "soft",
    "travel"
]

link_for_all_payments_in_category = "https://money.yandex.ru/catalogue/{}/all"


class Payment(object):

    def __init__(self, name, link):
        self.name = name
        self.link = link
        try:
            self.rules = self.get_rules_new()
            print("downloaded: {}".format(self.name))
        except:
            try:
                self.rules = self.get_rules_old()
                print("downloaded: {}".format(self.name))
            except:
                print("Nothing found for {}".format(self.name))
                self.rules = []

    def __str__(self):
        return str(self.dict)

    def __repr__(self):
        return str(self.dict)

    @property
    def dict(self):
        return self.__dict__

    def get_rules_new(self):
        payment_parameter_string = requests.get(self.link).text
        payment_soup = BeautifulSoup(payment_parameter_string, "lxml")
        find = payment_soup.find("div", {"class": "island"})
        find_rules = find.find_all("div", {"class": "data-unit"})
        all_rules = []
        for rule in find_rules:
            rule_label = rule.label.text
            rule_instructions = rule.find("div", {"class": "showcase__field-hint"})
            if rule_instructions is not None:
                rule_instructions = rule_instructions.text
            all_rules.append(Rule(rule_label, rule_instructions))
        return all_rules

    def get_rules_old(self):
        payment_parameter_string = requests.get(self.link).text
        payment_soup = BeautifulSoup(payment_parameter_string, "lxml")
        find = payment_soup.find("table", {"class": "xforms"})
        find_rules = find.find_all("tr")
        all_rules = []
        for rule in find_rules:
            rule_label = rule.label
            if rule.label is not None:
                rule_label = rule.label.text
            rule_instructions = rule.find("span", {"class": "xf_hint"})
            if rule_instructions is not None:
                rule_instructions = rule_instructions.text
            all_rules.append(Rule(rule_label, rule_instructions))
        return all_rules


class Rule(object):

    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

    def __str__(self):
        return str(self.dict)

    def __repr__(self):
        return str(self.dict)

    @property
    def dict(self):
        return self.__dict__


class PaymentsGetter(object):

    def __init__(self, link):
        self.link = link

    def get_payments_from_yandex(self, payment_type):
        yandex_string = requests.get(self.link.format(LIST_OF_TYPES[payment_type]))
        soup = BeautifulSoup(yandex_string.text, "lxml")
        find_all = soup.find_all('div', {"class": "shop-list-item"})
        payments = []
        print(len(find_all))
        for i in find_all:
            payment = Payment(i.find('div', {"class": "shop-list-item__name"}).text, i.a.get("href"))
            payments.append(payment)
        return payments

    @staticmethod
    def save_payments_to_file(filename, data):
        with open(filename, "a") as save_file:
            save_file.write(json.dumps(data, indent=4))


def download_all_and_save():
    getter = PaymentsGetter(link_for_all_payments_in_category)
    all_data = []
    for num in range(0, len(LIST_OF_TYPES)):
        all_data.append(getter.get_payments_from_yandex(num))
    getter.save_payments_to_file("yandex_dump.txt", all_data)


if __name__ == '__main__':
    download_all_and_save()
