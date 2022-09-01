from brownie import USDC, accounts, config
from web3 import Web3


def deploy_token_and_transfer():
    owner_account = accounts.add(config["wallets"]["from_key_presenter_1"])
    spender_account = accounts.add(config["wallets"]["from_key_presenter_2"])
    token = USDC.deploy({"from": owner_account}, publish_source=False)
    token.transfer(spender_account, Web3.toWei(1000, "ether"), {"from": owner_account})


def main():
    deploy_token_and_transfer()
