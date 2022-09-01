# ERC20 Custodial Wallets Demo
Disclaimer: Do not use in production. <br />
Creates deposit addresses for users.
## Installation
Project is made with Brownie.
```
pip install eth-brownie
```
Rename `.env-example` to `.env`.
```
mv .env-example .env
```
Edit the `.env` file and add your keys.

## Usage
To deploy the token, please use `00_deploy_token.py`
```
brownie run scripts/00_deploy_token.py --network <insert network>
```
To deploy the main wallet, please use `01_deploy_wallets.py`
```
brownie run scripts/01_deploy_wallets.py --network <insert network>
```
Please edit deployment scripts to your need.

## TODO
- Refactor deployment and interaction scripts
- Do more tests