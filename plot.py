import matplotlib.pyplot as plt
plt.ion()


def plot_history(history, title=''):
    """
    - history['bonds_outstanding']
    - history['bond_price']
    - history['strategy']
    - history['bond_stake_diff']

    - history['ohm_bonders']
    - history['ohm_dao']
    - history['ohm_stakers']
    - history['p_ohm_redeem']

    - history['ohm_supply']
    - history['ohm_supply_growth']

    - history['ohm_price']
    - history['market_value_asset']
    """

    fig = plt.figure(figsize=(16, 10))
    fig.suptitle(title)

    ax = fig.add_axes((0.06, 0.67, 0.4, 0.25))
    ax.plot(history['ohm_price'])
    ax.set_ylabel('OHM price (USD)')
    ax.set_xticklabels('')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title('OHM price')

    ax = fig.add_axes((0.57, 0.67, 0.4, 0.25))
    ax.plot(history['market_value_asset'])
    ax.set_ylabel('market_value_asset (USD)')
    ax.set_xticklabels('')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title('Market value of asset to buy bonds')

    ax = fig.add_axes((0.06, 0.36, 0.4, 0.25))
    ax.plot(history['bond_price'])
    ax.set_ylabel('bond_price (USD)')
    ax.set_xticklabels('')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title('Price of bonds')

    ax = fig.add_axes((0.57, 0.36, 0.4, 0.25))
    ax.plot(history['debt_ratio'])
    ax.set_ylabel('Debt ratio')
    ax.set_xticklabels('')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title('Debt ratio')

    ax = fig.add_axes((0.06, 0.05, 0.4, 0.25))
    ax.plot(history['strategy'], '.r')
    ax.set_ylabel('bonding-staking strategy')
    ax.set_title('Wheter bonded or staked')
    ax.set_xlabel('Rebase number')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax = ax.twinx()
    ax.plot(history['bond_stake_diff'], 'k')
    ax.set_ylabel('bond-stake ratio')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax = fig.add_axes((0.57, 0.05, 0.4, 0.25))
    ax.plot(history['bonds_outstanding'])
    ax.set_ylabel('bonds_outstanding')
    ax.set_title('Outstanding bonds')
    ax.set_xlabel('Rebase number')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    fig = plt.figure(figsize=(8, 6))
    fig.suptitle(title)

    ax = fig.add_subplot(111)
    ax.plot(history['ohm_bonders'], label='OHM to bonders')
    ax.plot(history['ohm_dao'], label='OHM to DAO')
    ax.plot(history['ohm_stakers'], label='OHM to stakers')
    ax.plot(history['ohm_supply_growth'], label='OHM supply growth')
    ax.plot(history['p_ohm_redeem'], label='pOHM redeem')
    ax.set_ylabel('OHM supply growth (OHM)')
    ax.set_xlabel('Rebase number')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title('OHM supply and supply growth')
    ax.legend(loc=2)

    ax = ax.twinx()
    ax.plot(history['ohm_supply'], '--k', label='OHM supply')
    ax.plot(history['p_ohm_redeemed'], ':k', label='pOHM redeemed')
    ax.set_ylabel('OHM supply (OHM)')
    # ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(loc=(0.01, 0.6))

    return ax
