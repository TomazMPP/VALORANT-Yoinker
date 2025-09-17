# 🚫 Blacklist System — VALORANT Rank Yoinker

## How to Use

### 1. Blacklist File

* Edit the `blacklist.txt` file in the project root
* Add one player name per line in the format: `PlayerName#TAG`
* Lines that start with `#` are comments and will be ignored

### 2. Usage Example

```
# VALORANT Player Blacklist
ToxicPlayer#BR1
Cheater#NA1
AnotherBadPlayer#EU1
```

### 3. Features

* ✅ **Automatic Detection**: The system automatically checks all players in:

  * **Agent Select** (PREGAME)
  * **During the Match** (INGAME)
  * **Menu/Party** (MENUS)

* ✅ **Color Alerts**: When blacklisted players are detected, you’ll see red warnings in the terminal

* ✅ **Real-Time Updates**: You can edit the `blacklist.txt` file while vRY is running — changes are applied automatically

* ✅ **Case-insensitive**: It doesn’t matter if you use uppercase or lowercase

### 4. How to Add Players

1. Copy the player’s full name (with #TAG) from the game or from vRY
2. Paste it into the `blacklist.txt` file
3. Save the file
4. The blacklist will be refreshed automatically on the next check

### 5. Warning Example

When a blacklisted player is detected, you’ll see something like:

```
⚠️  BLACKLISTED PLAYERS DETECTED ⚠️
Found 1 blacklisted player(s) in Agent Select:
  • ToxicPlayer#BR1
```

## ⚠️ Important

* This feature was added in a **non-invasive** way — it doesn’t modify any existing vRY functionality
* The system only **warns** about blacklisted players; it takes no automatic action
* Use responsibly and in accordance with VALORANT’s Terms of Service
