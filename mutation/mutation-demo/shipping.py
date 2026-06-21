"""
Módulo de cálculo de total de pedido.

Regras de negócio:
- Desconto por quantidade:
    * 3 a 4 itens   -> 5%
    * 5 a 9 itens   -> 10%
    * 10+ itens     -> 15%
- Desconto por cupom:
    * "PROMO10" -> +10%
    * "PROMO20" -> +20%
- O desconto total é limitado a no máximo 30% (cap).
- Frete fixo de R$ 15,00, GRATUITO se o total (após desconto) for >= R$ 200,00.
"""


def calculate_order_total(subtotal: float, quantity: int, coupon_code: str = None) -> float:
    if subtotal < 0 or quantity < 0:
        raise ValueError("subtotal e quantity não podem ser negativos")

    discount = 0.0

    # Desconto por quantidade
    if quantity >= 10:
        discount += 0.15
    elif quantity >= 5:
        discount += 0.10
    elif quantity >= 3:
        discount += 0.05

    # Desconto por cupom
    if coupon_code == "PROMO10":
        discount += 0.10
    elif coupon_code == "PROMO20":
        discount += 0.20

    # Cap máximo de desconto
    if discount > 0.30:
        discount = 0.30

    total = subtotal * (1 - discount)

    # Frete grátis a partir de R$ 200 (após desconto)
    shipping = 0.0 if total >= 200 else 15.0

    return round(total + shipping, 2)
