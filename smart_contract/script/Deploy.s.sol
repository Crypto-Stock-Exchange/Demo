// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../src/TUSDTestToken.sol";
import "../src/Crypto_Stock_Exchange.sol";

contract Deploy is Script {
    function run() external {
        vm.startBroadcast();

        // 1. Deploy TUSDTestToken
        TUSDTestToken tusd = new TUSDTestToken();
        console.log("TUSDTestToken deployed at:", address(tusd));

        Crypto_Stock_Exchange exchange =
            new Crypto_Stock_Exchange(address(tusd), 0xF716eC77197C3EE20B990E81736e83666584f468);
        console.log("Crypto_Stock_Exchange deployed at:", address(exchange));

        vm.stopBroadcast();
    }
}
