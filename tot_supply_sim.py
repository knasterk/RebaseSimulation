import utils as u
from plot import plot_history


n_rebase = 5*3*365  # number of rebases to simulate; 3 rebases per day

# Parameters
BCV = 100
REWARD_RATE = 0.006  # reward rate per rebase, fraction of 1
VEST_SUPPLY_FRAC = 0.09

# Initial conditions
ohm_supply_init = 1  # start the simulation at 1 OHM == 1 USD
bonds_outstanding_init = 0  # start the simulation with 0 bonds
n_rebase_to_fully_vested = 15
ohm_bonders_init = 0
ohm_stakers_init = 0
p_ohm_supply_init = 25E6
ohm_price_init = 1.  # Start at 1 USD
p_ohm_redeemed = 0.

# TODO: Check this with K. Currently 99K per day.
market_value_asset = 33000

ohm_supply = ohm_supply_init
bonds_outstanding = bonds_outstanding_init
ohm_bonders = ohm_bonders_init
ohm_stakers = ohm_stakers_init
p_ohm_supply = p_ohm_supply_init
ohm_price = ohm_price_init

# Bonders bond at different discounts.
vesting_bonds = []

# Records
history = {}
history['bonds_outstanding'] = [bonds_outstanding_init]
history['bond_price'] = []
history['premium'] = []
history['debt_ratio'] = []
history['strategy'] = []
history['bond_stake_diff'] = []
history['ohm_bonders'] = []
history['ohm_dao'] = []
history['ohm_stakers'] = []
history['p_ohm_redeem'] = []
history['p_ohm_redeemed'] = []
history['ohm_supply'] = [ohm_supply_init]
history['ohm_supply_growth'] = []
history['ohm_price'] = []
history['market_value_asset'] = []
history['vesting_bonds'] = []

# OHM staked:
"""
Just assume that the entire OHM supply is staked

added from bonds outstanding
added when strategy is stake
added by ohm_stakers (i.e. when stakers are rewarded by reward_rate)

What about un-staking??
"""

for t in range(n_rebase):

    bonds_outstanding, ohm_staked, vesting_bonds = \
        u.get_bonds_outstanding(vesting_bonds)

    bond_price, premium, debt_ratio = u.get_bond_price(bonds_outstanding,
                                                       ohm_supply, BCV)
    strategy, roi_bond, roi_stake, bond_stake_diff = \
        u.bond_or_stake(bond_price=bond_price,
                        ohm_price=ohm_price,
                        reward_rate=REWARD_RATE,
                        n_rebase_to_fully_vested=n_rebase_to_fully_vested)

    if strategy == 'bond':
        ohm_bonders = u.get_bond_payout(bond_price, market_value_asset)
        ohm_dao = u.get_ohm_dao(bond_price, market_value_asset)
        ohm_stakers = 0.

        bond_reward_per_rebase = ohm_bonders / n_rebase_to_fully_vested
        vesting_bonds.append({'bond_t0': ohm_bonders,
                              'bond': ohm_bonders,
                              'reward_per_rebase': bond_reward_per_rebase,
                              'rebase_i': n_rebase_to_fully_vested})
    else:
        ohm_stakers = u.get_ohm_stakers(ohm_supply, REWARD_RATE)
        ohm_bonders = 0.
        ohm_dao = 0.

    if (t % 1) == 0:
        p_ohm_redeem, p_ohm_redeemed, p_ohm_supply = \
            u.get_p_ohm_redeem(ohm_supply,
                               ohm_price,
                               p_ohm_supply,
                               p_ohm_redeemed,
                               vest_supply_frac=VEST_SUPPLY_FRAC)

    supply_growth = u.get_supply_growth(ohm_stakers, ohm_bonders,
                                        ohm_dao, p_ohm_redeem)
    ohm_supply += supply_growth

    history['bond_price'].append(bond_price)
    history['premium'].append(debt_ratio)
    history['debt_ratio'].append(debt_ratio)
    history['strategy'].append(strategy)
    history['bond_stake_diff'].append(bond_stake_diff)
    history['ohm_bonders'].append(ohm_bonders)
    history['ohm_dao'].append(ohm_dao)
    history['ohm_stakers'].append(ohm_stakers)
    history['p_ohm_redeem'].append(p_ohm_redeem)
    history['p_ohm_redeemed'].append(p_ohm_redeemed)
    history['ohm_supply'].append(ohm_supply)
    history['ohm_supply_growth'].append(supply_growth)
    history['bonds_outstanding'].append(bonds_outstanding)
    history['vesting_bonds'].append(vesting_bonds)
    history['ohm_price'].append(ohm_price)
    history['market_value_asset'].append(market_value_asset)

    # TODO: check this with K.
    # Linear increase with 1 USD per day.
    ohm_price += (1/3)

ax = plot_history(history, title=f'BCV: {BCV}')
