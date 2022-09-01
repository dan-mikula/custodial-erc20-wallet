// SPDX-License-Identifier: MIT

pragma solidity ^0.8.16;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract CustodialERC20WalletChild is Ownable {
    event WalletEvent(
        address indexed _addr,
        string _action,
        uint256 _amount,
        uint256 _timestamp
    );

    address private beneficiaryAddress;

    constructor(address _beneficiaryAddress) public {
        beneficiaryAddress = _beneficiaryAddress;
    }

    function sweep(address _tokenContractAddress) public onlyOwner {
        uint256 amount = IERC20(_tokenContractAddress).balanceOf(address(this));
        IERC20(_tokenContractAddress).transfer(beneficiaryAddress, amount);
        emit WalletEvent(msg.sender, "sweep", amount, block.timestamp);
    }

    receive() external payable {
        emit WalletEvent(msg.sender, "deposit", msg.value, block.timestamp);
        payable(beneficiaryAddress).transfer(address(this).balance);
    }
}
