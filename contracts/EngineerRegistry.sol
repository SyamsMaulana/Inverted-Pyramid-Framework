// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract EngineerRegistry {
    enum State { AVAILABLE, LOCKED, SUSPENDED, BLACKLISTED }
    mapping(bytes32 => State) public statuses;
}
