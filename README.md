# Polly Chain
Polly Chain is a simple blockchain operating fully on PoW Nakamoto-like consensus.

It's made purely out of curiosity, should be used only as an educational material e.t.c. Not exclusively safe, not too fast and still in development 🌳


## Overview
The blockchain consists of 3 main modules, modules are not dependent on each other and can be easily run and used with a couple prerequisites taken into consideration:
- **Node** is an entry point in user interaction with the blockchain. It recieves blocks and transactions, validates them, constantly exchanges data with other known nodes and miners, as well as stores its own copy of the blockchain. 

  To host a node launch the _Node.py_ file. A socket will be instantly opened using your LAN IP address and binded on the port 8330.
  The program will ping all the known nodes( predefined in the _TRUSTED_IPS_ variable ) to fetch the current state of the blockchain. 
  If none of the pinged nodes have the actual copy of the blockchain( ***non - empty with at least one valid block*** ) - an empty blockchain will be created and the Node will start waiting for the miners to submit new blocks e.t.c.

  Node recieves transactions from the Wallet interface and stores them in the '_mempool_' - a list of all the transactions, which were not included into a block. These pending transactions are later fed to the miners🔨

- **Miners** use their computing power in search of a correct nonce( _'number used only once'_ ) which, when found, will bring them **current block's rewards**, a right to include specific transactions(thus earn transaction fees) and to issue a new block.

  After finding the correct nonce miner assembles the block: 

  1. Pending transactions are queried from the nodes and included into a block based on the **highest** transaction fee.
  2. Block structure is populated
  3. Block is transmitted to all the available nodes
  4. After checking the block's validity nodes append it to the blockchain ✔️
- **Wallet** allows the end user to interact with the blockchain. After creating a wallet you can send/recieve coins from anyone anytime 💰

## How to use?

1. Download this repository ⬇️
2. To create a wallet, send/recieve juicy coins go to _src/Wallet.py_ 🪙
3. To start mining and competing for the block rewards - go to _src/Miner.py_ ⚒️
4. To host a node and become a part of the Polly Chain ecosystem go to _src/Node.py_ ✈️
