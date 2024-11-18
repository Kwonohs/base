import unittest
from seaborn import load_dataset
from banking import Bank, NormalMember,PremiumMember, LoyalMember

class Test1(unittest.TestCase):
    def setUp(self):
        self.normalbank = Bank(NormalMember())  # 기본적으로 할인이 없음
        self.premiumbank = Bank(PremiumMember())  # 기본적으로 할인이 없음
        self.loyalbank = Bank(LoyalMember())  # 기본적으로 할인이 없음
    
    def test_normalmember(self):
        self.normalbank.add_item(10000)
        self.assertEqual(int(self.normalbank.calculate_total()), 10220)

    def test_premiummember(self):
        self.premiumbank.add_item(10000)
        self.assertEqual(int(self.premiumbank.calculate_total()), 10240)

    def test_normalmember(self):
        self.loyalbank.add_item(10000)
        self.assertEqual(int(self.loyalbank.calculate_total()), 10260)

    def test_upper(self):
        self.assertEqual('A', 'a'.upper())

    def test_split(self):
        string = 'hello world'
        self.assertEqual(string.split(), ['hello', 'world'])

if __name__ == '__main__':
    unittest.main()