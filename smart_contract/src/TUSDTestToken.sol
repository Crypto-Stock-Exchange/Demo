// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TUSDTestToken is ERC20 {
    error TUSDTestToken__Send();

    address public owner;
    uint256 public immutable RATE;

    constructor() ERC20("Test USD", "USDT") {
        owner = msg.sender;
        RATE = 100000 * (10 ** decimals());
    }

    receive() external payable {
        if (msg.value <= 0) {
            revert TUSDTestToken__Send();
        }

        uint256 amountToMint = (msg.value * RATE) / 1 ether;
        _mint(msg.sender, amountToMint);
    }

    function withdraw() external {
        require(msg.sender == owner, "Only owner can withdraw");
        payable(owner).transfer(address(this).balance);
    }
}
