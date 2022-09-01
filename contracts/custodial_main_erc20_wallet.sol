// SPDX-License-Identifier: MIT

pragma solidity ^0.8.16;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./erc20_wallet_child.sol";

contract CustodialWalletMain is Ownable {
    CustodialERC20WalletChild[] public wallets;
    CustodialERC20WalletChild public wallet;
    event WalletEvent(
        CustodialERC20WalletChild indexed _addr,
        string _action,
        uint256 _timestamp
    );
    address private beneficiaryAddress;

    constructor(address _beneficiaryAddress) {
        beneficiaryAddress = _beneficiaryAddress;
    }

    function createWallet()
        public
        onlyOwner
        returns (CustodialERC20WalletChild)
    {
        wallet = new CustodialERC20WalletChild(beneficiaryAddress);
        wallets.push(wallet);
        emit WalletEvent(wallet, "creation", block.timestamp);
        return wallet;
    }

    function getWallets()
        public
        view
        onlyOwner
        returns (CustodialERC20WalletChild[] memory)
    {
        return wallets;
    }

    function sweepWallet(
        address _contractAddress,
        address _tokenContractAddress
    ) public onlyOwner returns (bool) {
        IERC20Wallet walletContract = IERC20Wallet(_contractAddress);
        walletContract.sweep(_tokenContractAddress);
        return true;
    }
}

interface IERC20Wallet {
    function sweep(address _tokenContractAddress) external;
}
