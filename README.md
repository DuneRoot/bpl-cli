# BPL CLI

> A simple CLI client for the Blockpool Blockchain

This is an easy-to-use Python Command Line Interface (CLI) client for interacting with a Blockpool Blockchain. This client provides the majority of the functionality provided by [BPL-desktop](https://github.com/blockpool-io/BPL-desktop)

## Features

### Account
- [x] Delegate registration
- [x] Transferring BPL
- [x] Vote for a delegate
- [x] Status of account
- [x] List of transactions (in chronological order)
- [x] Create a new address and public key from a BIP39 mnemonic

### Message
- [x] Sign a message
- [x] Verify a message

### Network
- [x] Network status
- [x] Network config new
- [x] Network config use
- [x] Showing network config
- [x] Showing network peers

### Command Entity
- [x] Constructor
- [x] Run method

### Exceptions
- [x] BPLClientNetworkException
- [x] BPLClientAccountsException

## Installation

```sh
python -m pip install bpl-client
```

## Usage

### Help

```sh
C:\>bpl-cli -help
BPL Client

Usage:
  bpl-cli network config setup
  bpl-cli network config show
  bpl-cli network status
  bpl-cli account status <address>
  bpl-cli account transactions <address>
  bpl-cli account send <amount> <recipient>
  bpl-cli account vote <username>
  bpl-cli account delegate <username>
  bpl-cli message sign <message>
  bpl-cli message verify <message> <publicKey>

Options:
  -h --help                 Show this screen.
  --version                 Show version.

Help:
  For help using this client, please see https://github.com/DuneRoot/bpl-cli
```

### Network config new

To create a new custom network config the command ``bpl-cli network config new`` must be used. It should be noted that if the network config has not been selected using `network config new` or `network config use` and a different command is used then a ``BPLClientNetworkException`` is raised.

```sh
C:\>bpl-cli network config new
Enter config identifier: testnet_01
Enter peer address and port: 35.180.64.83:9028
Enter version: 25
Enter begin epoch: 2017-03-21 13:00:00

Network Config (testnet_01)
 +--------------+------------------------------------------------------------------+
 |     Name     |                              Value                               |
 +--------------+------------------------------------------------------------------+
 | version      | 25                                                               |
 | peer address | 35.180.64.83:9028                                                |
 | begin epoch  | 2017-03-21 13:00:00                                              |
 | nethash      | f9b98b78d2012ba8fd75538e3569bbc071ce27f0f93414218bc34bc72bdeb3db |
 +--------------+------------------------------------------------------------------+

 ```

### Network config use

To use or select a default or custom network config the command ``bpl-cli network config use`` must be used. It should be noted that if an invalid config identifier is inputted then a `BPLClientNetworkException` is raised.

```sh
C:\>bpl-cli network config use

Config Identifiers
 +------------+
 |  Configs   |
 +------------+
 | testnet1   |
 | testnet    |
 | mainnet    |
 | testnet_01 |
 +------------+

Enter config identifier: mainnet

Network Config (mainnet)
 +--------------+------------------------------------------------------------------+
 |     Name     |                              Value                               |
 +--------------+------------------------------------------------------------------+
 | version      | 25                                                               |
 | peer address | 13.56.163.57:9030                                                |
 | begin epoch  | 2017-03-21 13:00:00                                              |
 | nethash      | 7bfb2815effb43592ccdd4fd0f657c082a7b318eed12f6396cc174d8578293c3 |
 +--------------+------------------------------------------------------------------+
```

### Transferring BPL

To transfer BPL the command ``bpl-cli account send <amount> <address>`` must be used. A prompt for the secret passphrase is then displayed, which masks the input.

```sh
C:\>bpl-cli account send 0.1 BFCKaUEkmG8ULYitaharStcdn7ijuDxxpK
Enter secret passphrase:
Confirm (y/n): y
Sending 0.1 BPL to BFCKaUEkmG8ULYitaharStcdn7ijuDxxpK.
Transaction sent successfully with id 295fb4d1c128f6319a2ebfe688dd762c6d15fc1e40ccde92ca531cce25d4ae74.
```

### Listing transactions

To list the transactions of an address, the command ``bpl-cli account transactions <address>`` must be used.

```sh
C:\>bpl-cli account transactions B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY

Transactions (Address: B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY)
 +------------------------------------------------------------------+---------------------+------------------------------------+------------------------------------+--------------+------------+---------------+
 |                          Transaction ID                          |      Timestamp      |               Sender               |             Recipient              |    Amount    |    Fee     | Confirmations |
 +------------------------------------------------------------------+---------------------+------------------------------------+------------------------------------+--------------+------------+---------------+
 | 295fb4d1c128f6319a2ebfe688dd762c6d15fc1e40ccde92ca531cce25d4ae74 | 2018-08-08 09:08:54 | B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY | BFCKaUEkmG8ULYitaharStcdn7ijuDxxpK | 10000000     | 10000000   | 30            |
 | bfcdc447bacb31cc7b53794bdbafb88d26e0fb03cee1363aba733cd1a2a1b4c7 | 2018-08-07 15:49:22 | B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY | BFCKaUEkmG8ULYitaharStcdn7ijuDxxpK | 10000000     | 10000000   | 4002          |
 | 73e6d46a070825bbaeb69a7a522446b5f46f563cc1da0f180dfde8ad17e96d96 | 2018-08-07 15:42:47 | B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY | BFCKaUEkmG8ULYitaharStcdn7ijuDxxpK | 1000000      | 10000000   | 4023          |
 | 4942794d20170637c5c9853bce7ce488bfc56bc2697745bb19ccba81ad224e2a | 2018-08-07 15:39:54 | B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY | B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY | 1000000      | 10000000   | 4038          |
 | a52cf29d2d2825ff5a6d7fb6bc4d7d07e0e395908a9d840207d65466b2068d3c | 2018-08-07 12:46:58 | B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY | N/A                                | 0            | 1000000000 | 4695          |
 | 5530522fc3371f6c3527d138f0eb48a8fe6cf50329440fcfe54991d05e4ebe59 | 2018-08-07 12:21:26 | B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY | B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY | 0            | 100000000  | 4801          |
 | 4fdea05eb8c17f00e6f1db0b0b0869e1b7ea428a61760c157f789f6e497c8c05 | 2018-08-07 10:05:33 | B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY | BFCKaUEkmG8ULYitaharStcdn7ijuDxxpK | 100          | 10000000   | 5301          |
 | ee3270bacf2ada607915b38154618c78174698afcf02680d5f37734bf18bc9e7 | 2018-08-07 10:04:04 | B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY | BFCKaUEkmG8ULYitaharStcdn7ijuDxxpK | 100          | 10000000   | 5301          |
 | a754cefa329ba2c1966f6346bc69300e7ae55e4c2b8c331765319b19e215e0c2 | 2018-08-06 15:19:36 | BFCKaUEkmG8ULYitaharStcdn7ijuDxxpK | B8a5sk4SBzWTxURX3sw5iMy7py26QgA4NY | 500000000000 | 10000000   | 9641          |
 +------------------------------------------------------------------+---------------------+------------------------------------+------------------------------------+--------------+------------+---------------+
```

## Security or Errors

If you discover a security vulnerability or error within this package, please email [me](mailto:alistair.o'brien@ellesmere.com) or message me on the [BPL discord](https://discordapp.com/invite/67HxSKq).


## Credits

- [Alistair O'Brien](https://github.com/johnyob)
