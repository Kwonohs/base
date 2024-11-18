from abc import ABC, abstractmethod


# 은행 예금 금리를 고객 등급에 따라서 다르게 적용
# 예금 기본 금리는 2%라고 한다.
# Normalmember는 0.2%p 가산,
# PremiumMember는 0.4%p 가산,
# LoyalMember는 0.6%p 가산,
# 위의 내용을 strategy pattern으로 구현현


class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, amount):
        pass

# Concrete Strategy 1: 일반 할인 전략
class NormalMember(DiscountStrategy):
    def apply_discount(self, amount):
        discount = amount * 0.022
        amount += discount
        return amount

# Concrete Strategy 2: 10% 회원 할인 전략
class PremiumMember(DiscountStrategy):
    def apply_discount(self, amount):
        discount = amount * 0.024
        amount += discount
        return amount

# Concrete Strategy 3: 20% 시즌 할인 전략
class LoyalMember(DiscountStrategy):
    def apply_discount(self, amount):
        discount = amount * 0.026
        amount += discount
        return amount
    

class Bank:
    def __init__(self, discount_strategy: DiscountStrategy):
        self.discount_strategy = discount_strategy
        self.items = []

    def add_item(self, price):
        self.items.append(price)

    def calculate_total(self):
        total = sum(price for price in self.items)
        print(f'총 금액: {total}원')
        return self.discount_strategy.apply_discount(total)

    def set_discount_strategy(self, discount_strategy: DiscountStrategy):
        self.discount_strategy = discount_strategy
    

bank = Bank(NormalMember())  # 기본적으로 할인이 없음
bank.add_item(50000)

# 할인이 적용되지 않은 상태에서 총 금액 계산
print('== 일반맴버 ==')
total = bank.calculate_total()
print(f'이자: {total}원\n')


bank = Bank(PremiumMember())  # 기본적으로 할인이 없음
bank.add_item(50000)

# 할인이 적용되지 않은 상태에서 총 금액 계산
print('== 프리미엄맴버 ==')
total = bank.calculate_total()
print(f'이자: {total}원\n')
print(total)

bank = Bank(LoyalMember())  # 기본적으로 할인이 없음
bank.add_item(50000)

# 할인이 적용되지 않은 상태에서 총 금액 계산
print('== 로얄맴버 ==')
total = bank.calculate_total()
print(f'이자: {total}원\n')

