from brownie import CustodialWalletMain, accounts, config, Contract, network

owner_account = accounts.add(config["wallets"]["from_key_presenter_1"])
spender_account = accounts.add(config["wallets"]["from_key_presenter_2"])
beneficiary_account = accounts.add(config["wallets"]["from_key_presenter_3"])


def deploy_main_wallet():
    print(f"Deploying Main Wallet on {network.show_active()}")
    wallet = CustodialWalletMain.deploy(
        beneficiary_account.address, {"from": owner_account}, publish_source=False
    )
    print(wallet.address)


def deploy_child_wallet():
    print(f"Creating Child Wallet on {network.show_active()}")
    main_wallet = Contract.from_abi(
        CustodialWalletMain._name,
        CustodialWalletMain[-1].address,
        CustodialWalletMain.abi,
    )
    child_wallet = main_wallet.createWallet({"from": owner_account})
    child_wallet.wait(1)
    child_wallets = main_wallet.getWallets({"from": owner_account})
    print(child_wallets)


def main():
    deploy_main_wallet()
    deploy_child_wallet()
