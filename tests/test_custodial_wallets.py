from brownie import (
    USDC,
    CustodialWalletMain,
    accounts,
    config,
)
import pytest
from web3 import Web3


@pytest.fixture(scope="module")
def account(accounts):
    owner_account = accounts.add(config["wallets"]["from_key_presenter_1"])
    spender_account = accounts.add(config["wallets"]["from_key_presenter_2"])
    beneficiary_account = accounts.add(config["wallets"]["from_key_presenter_3"])
    return owner_account, spender_account, beneficiary_account


@pytest.fixture(scope="module")
def token(USDC, account):
    owner_account = account[0]
    token = USDC.deploy({"from": owner_account})
    return token


@pytest.fixture(scope="module")
def custodial_main_wallet(account, CustodialWalletMain):
    owner_account = account[0]
    beneficiary_account = account[2]
    wallet_main = CustodialWalletMain.deploy(
        beneficiary_account, {"from": owner_account}
    )
    return wallet_main


def test_balance_after_token_transfer(token, account):
    assert Web3.toWei(100000, "ether") == token.balanceOf(account[0])
    token.transfer(account[1], Web3.toWei(10000, "ether"), {"from": account[0]})
    assert Web3.toWei(10000, "ether") == token.balanceOf(account[1])


def test_create_child_wallet(custodial_main_wallet, account):
    custodial_main_wallet.createWallet({"from": account[0]})
    assert len(custodial_main_wallet.getWallets({"from": account[0]})) == 1


def test_deposit_tokens_and_coins_to_child_wallet(
    token, account, custodial_main_wallet
):
    owner_account = account[0]
    spender_account = account[1]
    beneficiary_account = account[2]

    # create child wallet and get wallets
    custodial_main_wallet.createWallet({"from": owner_account})
    wallet_addresses = custodial_main_wallet.getWallets({"from": owner_account})
    print(wallet_addresses)
    assert len(wallet_addresses) == 2

    # check balances
    assert token.balanceOf(owner_account) == Web3.toWei(90000, "ether")
    assert token.balanceOf(spender_account) == Web3.toWei(10000, "ether")
    assert token.balanceOf(beneficiary_account) == 0

    # transfer to first deposit address from spender account
    tx = token.transfer(
        wallet_addresses[0], Web3.toWei(300, "ether"), {"from": spender_account}
    )
    tx.wait(1)
    assert token.balanceOf(wallet_addresses[0]) == Web3.toWei(300, "ether")
    assert token.balanceOf(spender_account) == Web3.toWei(9700, "ether")
    assert token.balanceOf(beneficiary_account) == 0

    # sweep balance from first deposit address
    tx = custodial_main_wallet.sweepWallet(
        wallet_addresses[0], token.address, {"from": owner_account}
    )
    tx.wait(1)
    assert token.balanceOf(wallet_addresses[0]) == 0
    assert token.balanceOf(beneficiary_account.address) == Web3.toWei(300, "ether")

    # transfer ETH to first deposit address. gets autosweeped
    assert Web3.fromWei(accounts[0].balance(), "ether") == 100
    tx = accounts[0].transfer(wallet_addresses[0], Web3.toWei(1, "ether"))
    tx.wait(1)
    assert Web3.fromWei(accounts[0].balance(), "ether") == 99
    assert Web3.fromWei(beneficiary_account.balance(), "ether") == 1
