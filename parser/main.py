import requests
from bs4 import BeautifulSoup

LIST_OF_TYPES = [
    "zku",
    "phone",
    "internet",
    "tv",
    "games",
    "goods",
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
        except AttributeError as e:
            print("Nothing found for {}".format(self.name))
            self.rules = []

    def __str__(self):
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
        # TODO научиться парсить старые платежи
        pass


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


if __name__ == '__main__':
    paymentss = PaymentsGetter(link_for_all_payments_in_category).get_payments_from_yandex(1)
    for pay in paymentss:
        print(pay)
