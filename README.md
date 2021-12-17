# RebaseSimulation
Simulations of rebasing cryptocurrency tokens

## Test
```
python3 tot_supply_sim.py
```

## Goals
 * How does BCV affect ohm_supply?
 * How does BCV affect the treasury balance?


## Assumptions
 * Whether to stake or bond is governed by profitability. See `utils.bond_or_stake()`


## Parameters
 * `reward_rate`: The set percentage of OHM distributed to the stakers on each rebase relative to ohm_total_supply. Set by the team. Use fraction of 1, not percentage.
 * `BCV`: Bond Control Variable. The scaling factor at which bond prices change. A higher BCV means a lower discount for bonders and HIGHER INFLATION
                             (WHY? BECAUSE LESS BONDING -> LESS ASSETS ADDED TO TREASURY?).

## Questions

ohm_total_supply: IS THIS DIFFERENT FROM OHM_SUPPLY?
                  SHOULD IT BE THE TOTAL SUPPLY OF STAKED OHM OR THE TOTAL SUPPLY OF OHM (STAKED AND NOT STAKED)? IT SEEMS TO BE THE TOTAL SUPPLY, INDEPENDENT OF WHETHER STAKED OR NOT.
                  SEE REWARD YIELD:
                    Reward yield refers to the actual amount of OHM received by each staker on each rebase. The reward yield is a rough target from a policy point of view. It can almost never be maintained precisely due to e.g. fluctuating amounts of OHM staked.

BCV: Bond Control Variable. The scaling factor at which bond prices change. A higher BCV means a lower discount for bonders and HIGHER INFLATION
                            (WHY? BECAUSE LESS BONDING -> LESS ASSETS ADDED TO TREASURY?).

n_rebase: Are there 15 rebases in a vesing period? Does vesing payout (redeem) only occur at rebases? My impression is that the claimable rewards on Wonderland are updated more frequently.

How to model `ohm_price`?
    - For now: as a linear increase with a USD per day.

How to model `market_value_asset`?
    - For now: fixed at 33 000 USD

## TODO
 * Check code against contracts.
 * Make it possible to quickly sweep over parapeter values.
