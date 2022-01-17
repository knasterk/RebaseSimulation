import requests
import os
import pandas as pd
from datetime import datetime, timedelta
from time import sleep


def get_historical_prices(fname='data/btrfly-usd-max.csv'):
    """
    Downloads and saves price data from CoinGecko.
    If fname exists and holds price data then new data
    (after the last date in fname) is appended. Otherwise all data is dowloaded
    and a new file created.

    """
    url = 'https://api.coingecko.com/api/v3/coins/butterflydao/history'
    t0 = '2021-12-19'  # First day of BTRFLY trading
    t1 = datetime.now().strftime('%Y-%m-%d')

    if not fname:
        fname = 'data/btrfly-usd-max.csv'
        print(f'Trying to save data to {fname}.')
        if not os.path.isdir('data'):
            os.path.mkdir('data')

    # Get last date stored in the file FNAME
    if os.path.isfile(fname):
        data = pd.read_csv(fname)
        t = data['snapped_at'].iloc[-1]
        dt = datetime.strptime(t, '%Y-%m-%d %H:%M:%S UTC') + timedelta(days=1)
        t = dt.strftime('%Y-%m-%d')
    else:
        t = t0
        data = pd.DataFrame(columns=['snapped_at',
                                     'price',
                                     'market_cap',
                                     'total_volume'])

    for date in pd.date_range(start=t, end=t1, freq='D'):
        params = {'date': date.strftime('%d-%m-%Y')}
        resp = requests.get(url, params)
        if resp.status_code == 200:

            market_data = resp.json()['market_data']
            new = {'snapped_at': date.strftime('%Y-%m-%d %H:%M:%S UTC'),
                   'price': market_data['current_price']['usd'],
                   'market_cap': market_data['market_cap']['usd'],
                   'total_volume': market_data['total_volume']['usd']}
            data = data.append(pd.DataFrame(new,
                                            columns=new.keys(),
                                            index=[len(data)]))

        sleep(2)  # CoinGecko's free API is rate-limited to 50 calls/min.

    print(f'Writing data to {fname}.')
    data.to_csv(fname)


def get_bond_price(bonds_outstanding, ohm_supply, BCV):
    """
    Arguments
    ---------
    bonds_outstanding: The total OHM promised to bonders.
                       E.g. the TIME I'm promised when I bond.

    ohm_supply: The total supply of existing OHM,
                not including bonds_outstanding. Bonded OHMs are gradually
                added to ohm_supply during the vesting period.
    BCV: Bond Control Variable. The scaling factor at which bond prices change.
                                A higher BCV means a lower discount for bonders
                                and HIGHER INFLATION
                                (WHY? BECAUSE LESS BONDING ->
                                LESS ASSETS ADDED TO TREASURY?). A lower BCV
                                means a higher discount for bonders and lonwer
                                inflation by the protocol.

    Returns
    -------
    bond_price: The price of the bond in USD.
    premium: The bond_price above 1 USD.
    debt_ratio: The total OHM promised to bonders divided by ohm_supply.
               Higher debt_ratio
               -> higher debt (more promised OHM relative to supply)
               -> higher premium
               -> higher bond_price
               -> lower bond discount


    """

    debt_ratio = bonds_outstanding / ohm_supply
    premium = debt_ratio * BCV
    bond_price = 1 + premium

    return bond_price, premium, debt_ratio


def get_bond_payout(bond_price, market_value_asset):
    """
    Arguments
    ---------
    ohm_price: The price of the bond in USD.
    market_value_asset: The market value in USD of the assets used to pay for
                        the bond.

    Returns
    -------
    bond_payout: The number of OHMs sold to a bonder (vesting over 5 days).
                 bond_payout is ohm_bonders.
    """

    bond_payout = market_value_asset / bond_price

    return bond_payout


def get_ohm_stakers(ohm_supply, reward_rate):
    """
    ohm_supply: The total supply of existing OHM,
                not including bonds_outstanding. Bonded OHMs are gradually
                added to ohm_supply during the vesting period.
    reward_rate: The set percentage of OHM distributed to the stakers on each
                 rebase relative to ohm_total_supply. Set by the team.
                 Use fraction of 1, not percentage.
    """
    ohm_stakers = ohm_supply * reward_rate

    return ohm_stakers


def get_ohm_dao(bond_price, market_value_asset):
    """
    OHM is minted for the DAO. This happens whenever someone purchases a bond.
    The DAO gets the same number of OHM as the bonder. This represents the
    DAO profit.

    Arguments
    ---------
    ohm_price: The price of the bond in USD.
    market_value_asset: The market value in USD of the assets used to pay for
                        the bond.

    Returns
    -------
    ohm_dao: The number of OHMs to the DAO. This is equal to the number of OHMs
             sold to a bonder. bond_payout is ohm_bonders.
    """
    ohm_dao = get_bond_payout(bond_price, market_value_asset)

    return ohm_dao


def get_p_ohm_redeem(ohm_supply, ohm_price, p_ohm_supply,
                     p_ohm_redeemed, vest_supply_frac=0.09):
    """
    OHM is minted for the team, investors, advisors, or the DAO.
    This happens whenever the aforementioned party exercises their p_ohm.
    E.g. an individual would supply 1 p_ohm along with 1 DAI to mint 1 OHM.
    The p_ohm is subsequently burned.

    Team, investor, and advisor pOHM cumulatively vest as 11.8% of OHM supply.
    This means that at 1m OHM supply, a maximum of 118k pOHM can be redeemed.
    At 10m OHM supply, it’s 1.18m pOHM. pOHM holders finish vesting anywhere
    from 2b to 5b supply, so this is a long term bet.
    There’s a lot of upside for holders, but it is dependent on actual growth
    of the protocol.

    See: https://olympusdao.medium.com/what-is-poh-16b2c38a6cd6

    Assumptions
    -----------
     * p_ohm is only redeemed for a profit.
     * The max amount of redeemable p_ohm will be redeemed for any profit.
     * Redeemers allways have sufficient USD to redeem.

    Arguments
    ---------
    ohm_supply: The total supply of existing OHM,
                not including bonds_outstanding. Bonded OHMs are gradually
                added to ohm_supply during the vesting period.
    ohm_price: The price of the bond in USD.
    p_ohm_supply: The total supply of p_ohm. Current supply, not initial.
    p_ohm_redeemed: The number of p_ohms redeemed.
    vest_supply_frac: The number of p_ohm that can be redeemed as a fraction
                      of the total OHM supply (ohm_supply).

    Returns
    -------
    p_ohm_redeem: The number of OHMs that were minted/redeemed from the p_ohm.
    p_ohm_redeemed: The number of p_ohms redeemed.
    p_ohm_supply: Updated total supply of p_ohm. Current supply, not initial.
    """

    # No redeem if it costs more than is gained.
    if ohm_price > 1:
        p_ohm_redeem = min(ohm_supply * vest_supply_frac - p_ohm_redeemed,
                           p_ohm_supply)
    else:
        p_ohm_redeem = 0.

    p_ohm_supply -= p_ohm_redeem
    p_ohm_redeemed += p_ohm_redeem

    return p_ohm_redeem, p_ohm_redeemed, p_ohm_supply


def get_supply_growth(ohm_stakers, ohm_bonders, ohm_dao, ohm_pexercise):
    """
    OHM supply does not have a hard cap. Its supply increases when:
     - OHM is minted and distributed to the stakers.
     - OHM is minted for the bonder. This happens whenever someone purchases a
       bond.
     - OHM is minted for the DAO. This happens whenever someone purchases a
       bond. The DAO gets the same number of OHM as the bonder.
     - OHM is minted for the team, investors, advisors, or the DAO.
       This happens whenever the aforementioned party exercises their pOHM.
    """

    supply_growth = ohm_stakers
    supply_growth += ohm_bonders
    supply_growth += ohm_dao
    supply_growth += ohm_pexercise

    return supply_growth


def get_bonds_outstanding(vesting_bonds):
    """
    Assumptions
    -----------
    * All vested bonds are immediately staked

    Arguments
    ---------
    vesting_bonds: a list of vesting bonds, each a dict containing the bonds
                   sold at a particular time.

    Returns
    -------
    bonds_outstanding: The total number of bonds outstanding,
                       i.e. still not vested.
    vesting_bonds: An updated list of vesting_bonds
    ohm_staked: The number of OHM vested and immediately staked.
    """
    bonds_outstanding = 0.
    ohm_staked = 0.
    rm_list = []

    for i, bond in enumerate(vesting_bonds):
        if bond['rebase_i'] > 0:
            bond['bond'] -= bond['reward_per_rebase']
            ohm_staked += bond['reward_per_rebase']
            bond['rebase_i'] -= 1
            bonds_outstanding += bond['bond']
        else:
            rm_list.append(i)

    # Remove fully vested bonds
    for rm_i in rm_list[::-1]:
        vesting_bonds.pop(rm_i)

    return bonds_outstanding, ohm_staked, vesting_bonds


def bond_or_stake(bond_price, ohm_price, reward_rate,
                  n_rebase_to_fully_vested=15, claim_interval=1):
    """

    Assumptions
    -----------
    * Constant APY over vesting period: reward_rate == reward_yield, i.e.
      the amount of staked OHM doesn't change over the vesting period.
    * No transaction fee

    Arguments
    ---------
    bond_price: The price of the bond in USD.
    ohm_price: The price of OHM in USD.
    reward_rate: The set percentage of OHM distributed to the stakers on each
                 rebase relative to ohm_total_supply. Set by the team.
                 Use fraction of 1, not percentage.
    n_rebase_to_fully_vested: The number of rebases in a vesting period.
    claim_interval: The number of rebases between each claim of the vested
                    bonds. Default 1, i.e claim at every rebase.
                    claim_interval = 3: claim once a day (if 3 rebases a day).
                    n_rebase_to_fully_vested has to be divisible by
                    claim_interval.

    Returns:
    strategy: The optimal strategy, boding ('bond') or staking ('stake').
    roi_bond: The return on investment if bonding (as a fraction of 1).
    roi_stake: The return on investment if staking (as a fraction of 1).
    bond_stake_diff: The difference between roi_bond and roi_stake.
    """
    n_claims = n_rebase_to_fully_vested / claim_interval
    assert n_claims.is_integer(), """n_rebase_to_fully_vested has to be evenly
    divisible by claim_interval."""
    n_claims = int(n_claims)

    bond_t0 = 100. / bond_price  # Buy for 100. usd
    stake_t0 = 100. / ohm_price  # Buy for 100. usd

    stake = stake_t0 * (1 + reward_rate)**n_rebase_to_fully_vested
    bond_reward_per_claim = bond_t0 / n_claims
    staked_bonds = 0.

    for t in range(n_claims):
        staked_bonds *= (1 + reward_rate)**claim_interval
        staked_bonds += bond_reward_per_claim

    roi_bond = (staked_bonds - stake_t0) / stake_t0
    roi_stake = (stake - stake_t0) / stake_t0

    roi_bond = staked_bonds * ohm_price
    roi_stake = stake * ohm_price

    bond_stake_diff = roi_bond - roi_stake

    if roi_bond > roi_stake:
        strategy = 'bond'
    else:
        strategy = 'stake'

    return strategy, roi_bond, roi_stake, bond_stake_diff


def roi_to_reward_rate(roi_5day, n_rebase_per_day):
    """

    APY = (1 + reward_rate)**(n_rebase_per_day * 365)
    APY**(1 / n_rebase_per_day * 365) = 1 + reward_rate
    """
    reward_rate = roi_5day**(1 / (n_rebase_per_day * 5)) - 1

    return reward_rate
