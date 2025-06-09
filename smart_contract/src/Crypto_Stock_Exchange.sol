// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {ERC721Enumerable} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {MessageHashUtils} from "@openzeppelin/contracts/utils/cryptography/MessageHashUtils.sol";
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

error Crypto_Stock_Exchange__InvalidInterval();
error Crypto_Stock_Exchange__ZeroAmount();
error Crypto_Stock_Exchange__TransferFailed();
error Crypto_Stock_Exchange__NotAuthorized();
error Crypto_Stock_Exchange__NotEnoughAllowance();
error Crypto_Stock_Exchange__InvalidSignature();
error Crypto_Stock_Exchange__Token_Ownership_Does_Not_Match_Buyer();

contract Crypto_Stock_Exchange is ReentrancyGuard {
    IERC20 public immutable USDT;
    BetNFT public immutable NFT;
    address public immutable backendSigner;

    constructor(address tusdAddress, address _backendSigner) {
        USDT = IERC20(tusdAddress);
        NFT = new BetNFT(address(this));
        backendSigner = _backendSigner;
    }

    function placeBet(
        string calldata symbol,
        uint256 lower,
        uint256 upper,
        uint256 amount,
        uint256 deadline,
        address owner,
        uint256 ownerfee,
        bytes memory signature
    ) external nonReentrant {
        if (lower > upper) revert Crypto_Stock_Exchange__InvalidInterval();
        if (amount == 0) revert Crypto_Stock_Exchange__ZeroAmount();

        uint256 allowed = USDT.allowance(msg.sender, address(this));
        if (allowed < amount + ownerfee) revert Crypto_Stock_Exchange__NotEnoughAllowance();

        if (!_verifyBuyNFT(msg.sender, owner, ownerfee, deadline, signature)) {
            revert Crypto_Stock_Exchange__InvalidSignature();
        }

        if (!USDT.transferFrom(msg.sender, address(this), amount + ownerfee)) {
            revert Crypto_Stock_Exchange__TransferFailed();
        }

        if (!USDT.transfer(owner, ownerfee)) revert Crypto_Stock_Exchange__TransferFailed();

        uint256 datenow = block.timestamp;

        NFT.mint(msg.sender, symbol, lower, upper, amount, deadline, datenow, ownerfee);
    }

    function _verifyBuyNFT(address sender, address owner, uint256 ownerfee, uint256 deadline, bytes memory signature)
        internal
        view
        returns (bool)
    {
        bytes32 messageHash = keccak256(abi.encodePacked(sender, owner, ownerfee, deadline));
        bytes32 ethSignedMessageHash = MessageHashUtils.toEthSignedMessageHash(messageHash);

        address recovered = ECDSA.recover(ethSignedMessageHash, signature);

        return recovered == backendSigner;
    }

    function _verifySellNFT(
        uint256 tokenId,
        address buyer,
        uint256 price,
        address owner,
        uint256 ownerfee,
        bytes memory signature
    ) internal view returns (bool) {
        if (NFT.ownerOf(tokenId) != buyer) {
            revert Crypto_Stock_Exchange__Token_Ownership_Does_Not_Match_Buyer();
        }

        bytes32 messageHash = keccak256(abi.encodePacked(tokenId, buyer, price, owner, ownerfee));
        bytes32 ethSignedMessageHash = MessageHashUtils.toEthSignedMessageHash(messageHash);

        address recovered = ECDSA.recover(ethSignedMessageHash, signature);
        return recovered == backendSigner;
    }

    function sellNFT(
        uint256 tokenId,
        address buyer,
        uint256 price,
        address owner,
        uint256 ownerfee,
        bytes calldata signature
    ) external nonReentrant {
        if (!_verifySellNFT(tokenId, buyer, price, owner, ownerfee, signature)) {
            revert Crypto_Stock_Exchange__InvalidSignature();
        }

        if (!USDT.transfer(buyer, price)) revert Crypto_Stock_Exchange__TransferFailed();
        if (!USDT.transfer(owner, ownerfee)) revert Crypto_Stock_Exchange__TransferFailed();

        NFT.burn(tokenId);
    }
}

contract BetNFT is ERC721Enumerable {
    uint256 public nextId;
    address public immutable exchange;

    constructor(address _exchange) ERC721("Stock Bet NFT", "SBET") {
        exchange = _exchange;
    }

    modifier onlyExchange() {
        if (msg.sender != exchange) revert Crypto_Stock_Exchange__NotAuthorized();
        _;
    }

    function mint(
        address to,
        string calldata symbol,
        uint256 lower,
        uint256 upper,
        uint256 amount,
        uint256 deadline,
        uint256 datenow,
        uint256 ownerfee
    ) external onlyExchange {
        _safeMint(to, nextId);
        emit BetCreated(to, nextId, symbol, lower, upper, amount, deadline, datenow, ownerfee);
        nextId++;
    }

    function burn(uint256 tokenId) external onlyExchange {
        _burn(tokenId);
        emit BetBurn(tokenId);
    }

    event BetBurn(uint256 indexed id);

    event BetCreated(
        address indexed user,
        uint256 indexed id,
        string symbol,
        uint256 lower,
        uint256 upper,
        uint256 amount,
        uint256 deadline,
        uint256 datenow,
        uint256 ownerfee
    );
}
