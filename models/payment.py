class Payment:
    def __init__(self, amount):
        self.amount = float(amount)

    def pay_cash(self, cash_given):
        # In this CLI, assume exact cash given == amount for simplicity.
        change = float(cash_given) - self.amount
        if change < -1e-6:
            print(f"❌ Not enough cash. Still need ${-change:.2f}")
            return False
        print(f"💵 Cash payment accepted. Change: ${max(change,0):.2f}")
        return True

    def pay_card(self):
        print("💳 Card payment approved.")
        return True

    def pay_wallet(self):
        print("📱 E-Wallet payment successful.")
        return True


