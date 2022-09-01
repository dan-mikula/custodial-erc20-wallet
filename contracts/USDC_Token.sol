// SPDX-License-Identifier: MIT

pragma solidity ^0.8.16;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract USDC is ERC20, ERC20Burnable, Ownable {
    constructor() public ERC20("US Dollar Coin - Mock", "USDC") {
        _mint(msg.sender, 100000 * 10**18);
    }

    function createSupply(uint256 _amount) public onlyOwner {
        require(_amount > 0, "Please provide an amount that is bigger than 0");
        _mint(msg.sender, _amount);
    }
}
