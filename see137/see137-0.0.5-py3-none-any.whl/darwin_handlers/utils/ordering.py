import copy
import crayons as cy
from loguru import logger

# logger.add(sys.stdout, format="{time} - {level} - {message}")
def symbol_split(symbol):
    if not isinstance(symbol, str):
        return None
    
    s = symbol.split("/")
    if len(s) != 2:
        return None
    
    return s



def get_target_percentage(desired, rl_pct):
    # Get a percentage of the total amount to sell/buy
    assert 0.0 <= desired <= 1.0
    assert 0.0 <= rl_pct <= 1.0 
    return desired * rl_pct


def get_divergence_of_total(current_percentage, target_percentage):
    if target_percentage >= current_percentage:
        return 0.0
    return current_percentage - target_percentage


def get_percentage_of_sale(divergence):
    return 1-divergence


def get_sale_amount(asset_amount, percentage_to_sell):
    return asset_amount * percentage_to_sell




def buy_divergence(current_pct, target_pct):
    return target_pct-current_pct


def get_buy_pct(rl_pct, desired, current_percentage):
    # How much we're buying of the total portfolio
    target = get_target_percentage(desired=desired, rl_pct=rl_pct)
    buy_div = buy_divergence(current_pct=current_percentage, target_pct=target)
    return buy_div

def get_usd_pct(buy_pct, total_portfolio_value):
    return buy_pct*total_portfolio_value



""" The complete functions """


def get_sale_pct(decision_percentage, cap_percentage, current_percentage):
    """ 
        Dynamically get a percentage of the current amount we're trying to sell. 
        It should allow us to buy.
    """
    # print(decision_percentage, cap_percentage, current_percentage)
    target_pct = get_target_percentage(rl_pct=decision_percentage, desired=cap_percentage)
    diverge = get_divergence_of_total(current_percentage=current_percentage, target_percentage=target_pct)
    percent_sale = get_percentage_of_sale(diverge)
    return percent_sale


def buy_total_cash(percentage, cap_allocation, pct_of_networth, net_worth):
    """ 
        # BUY TOTAL CASH
        ---
        Get the amount of cash we can spare on a given purchase in total cash. 
        Total cash = Percentage of
        ```py
            total_cash = buy_total_cash(decision_percentage, cap_allocation, pct_of_networth, net_worth)
            amount = ((total_cash / current_price)*0.98) # We get the amount of the given currency we want to buy
            trade = Trade()
        ```
        
        Parameters:
            - percentage: The percentage we want to act on
            - cap_allocation - This is the portfolio cap of the user for this given currency/portfolio. 
                - Portfolio cap is decided using rebalancing logic (modern portfolio theory)
                - float: between between 0-1
            - pct_net_worth - The percentage of the overall portfolio this asset is comprised of.
            - net_worth - The overall value of the portfolio. Renaming to networth
    """
    flexible_buy_percentage = get_buy_pct(percentage, cap_allocation, pct_of_networth)
    flexible_buy_percentage = abs(flexible_buy_percentage)
    total_cash = get_usd_pct(flexible_buy_percentage, net_worth)
    return total_cash


def get_buy_usd(decision_percentage, cap_allocation, pct_net_worth, net_worth):
    """ 
        # GET BUY USD
        ---
        Get the amount of cash we can spare on a given purchase
        buy_amount = buy_cash/price
        trade = self.buy(symbol, buy_amount, price, timestamp)
        Parameters:
            - decision_percentage: The percentage we want to act on
            - cap_allocation - This is the portfolio cap of the user for this given currency/portfolio. 
                - Portfolio cap is decided using rebalancing logic (modern portfolio theory)
                - float: between between 0-1
            - pct_net_worth - The percentage of the overall portfolio this asset is comprised of.
            - net_worth - The overall value of the portfolio. Renaming to networth
    """
    buy_pct = get_buy_pct(decision_percentage, cap_allocation, pct_net_worth)
    buy_usd = get_usd_pct(buy_pct, net_worth)
    return buy_usd



# class OrderInfo(object):
#     def get_buy_pct(self, rl_percentage, desired, current_percentage):

#         # How much we're buying of the total portfolio
#         target = get_target_percentage(desired=desired, rl_pct=rl_percentage)
#         buy_div = buy_divergence(current_pct=current_percentage, target_pct=target)
#         return buy_div
    
#     def get_sale_pct(self, rl_percentage, desired, current_percentage):
#         target_pct = get_target_percentage(rl_pct=rl_percentage, desired=desired)
#         diverge = get_divergence_of_total(current_percentage=current_percentage, target_percentage=target_pct)
#         percent_sale = get_percentage_of_sale(diverge)
        
#         # print(cy.magenta("Sales Percentage", bold=True))
#         # print("---")
#         # print(f"RL Percentage: {rl_percentage}")
#         # print(f"RL Desired: {desired}")
#         # print(f"Targeted Percentage: {target_pct}")
#         # print(f"Current percentage of total: {current_percentage}")
#         # print(f"The difference of percentage {diverge}" )
#         # print(f"The percentage of token we're holding that we intend to sell: {percent_sale}")
#         # print(rl_percentage, desired, target_pct, current_percentage, diverge, percent_sale)
#         # print()
#         return percent_sale
    
#     def get_buy_usd(self, rl_percentage, desired, current_percentage, total_portfolio_value):
#         # print(rl_percentage, desired, target_pct, current_percentage, diverge, percent_sale)
#         buy_pct = get_buy_pct(rl_percentage, desired, current_percentage)
#         buy_usd = get_usd_pct(buy_pct, total_portfolio_value)
        
#         # print(cy.magenta("Sales Percentage", bold=True))
#         # print("---")
#         # print(f"RL Percentage: {rl_percentage}")
#         # print(f"RL Desired: {desired}")
#         # print(f"Current percentage of total: {current_percentage}")
#         # print(f"Targeted Percentage: {buy_pct}")
#         # print(f"The difference of percentage {buy_usd}" )
#         return buy_usd