#!/usr/bin/env python3
"""
Generate one address of each type (Legacy P2PKH, Bech32 P2WPKH, Bech32m P2TR)
from a single BIP39 mnemonic using bip-utils (BIP44,BIP84,BIP86).
"""

from bip_utils import (
    Bip39MnemonicGenerator, Bip39SeedGenerator,
    Bip44, Bip44Coins, Bip44Changes,
    Bip84, Bip84Coins,
    Bip86, Bip86Coins
)

# --------- 1) Create or set a mnemonic ---------
mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

print("Mnemonic:")
print(mnemonic)
print()

# --------- 2) Generate seed from mnemonic (BIP39) ---------
seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

# --------- 3) Derive Legacy (P2PKH) using BIP44 ----------------
bip44_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
# m/44'/0'/0'/0/0  -> Account 0, external chain(0), address index 0
bip44_addr_ctx = bip44_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
legacy_address = bip44_addr_ctx.PublicKey().ToAddress()

# --------- 4) Derive Bech32 (P2WPKH) using BIP84 ----------------
bip84_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
bip84_addr_ctx = bip84_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
bech32_address = bip84_addr_ctx.PublicKey().ToAddress()

# --------- 5) Derive Bech32m (Taproot P2TR) using BIP86 ----------
bip86_ctx = Bip86.FromSeed(seed_bytes, Bip86Coins.BITCOIN)
bip86_addr_ctx = bip86_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
bech32m_address = bip86_addr_ctx.PublicKey().ToAddress()

# --------- 6) Output results ---------
print("Derived addresses (account 0 / external / index 0):")
print(f"Legacy (P2PKH, BIP44 m/44'/0'/0'/0/0): {legacy_address}")
print(f"Bech32 (P2WPKH, BIP84 m/84'/0'/0'/0/0): {bech32_address}")
print(f"Bech32m (P2TR,  BIP86 m/86'/0'/0'/0/0): {bech32m_address}")

