---
title: MTG Tools - Card Render Bot
subtitle: Beautiful renders of your favorite cards
date: 02/01/2023
author: Ludovic Heyberger
tags: [ guide, tools ]
banner: assets/banner_card_render_bot.jpg
---

I've always found ugly how Twitter displayed Magic the Gathering™ card pictures.

This is why I went on an [expedition][expedition] to fix that and created a dedicated card rendering chatbot available through [Messenger][Messenger] and [Telegram][Telegram].


# Usage

ℹ️ This bot is **publicly available and free to use**.


## Facebook Messenger

1. Open Facebook Messenger
2. Start a new discussion by navigating to [https://m.me/108575720841085](https://m.me/108575720841085)
3. Press the `Get Started` button


## Telegram

1. Open Telegram
2. Start a new discussion by navigating to [https://t.me/cardrenderbot](https://t.me/cardrenderbot)
3. Press the `Start` button


# Simple examples


## 1. Single card

You can render a single card by typing it's full name:

**💡 Example :**
```
arcane signet
```

**Result :**
![Arcane Signet](assets/arcane_signet.jpg)

You can also type only part of the full name if there's no ambiguity:

**💡 Example :**
```
wrath god
```

**Result :**
![Wrath of God](assets/wrath_of_god.jpg)


## 2. Single card from a specific set

If you want to render a card from a specific set, you can prefix the name with the set code.

The following example will render [Mana Crypt][Mana Crypt] from the [Kaladesh Inventions][Kaladesh Inventions] set:

**💡 Example :**
```
mps mana crypt
```

**Result :**
![Mana Crypt](assets/mana_crypt.jpg)


## 3. Specific card from a specific set

Some sets contain cards with different illustrations.
If you want a specific card, you can specify the set code and the collector number.

The following example will render the [basic Plains][basic Plains] from the [Dominaria United][Dominaria United] set:

**💡 Example :**
```
dmu plains
```

**Result :**
![Basic Plains](assets/dmu_262.jpg)


The following example will render the [full art Plains][full art Plains] from the [Dominaria United][Dominaria United] set:

**💡 Example :**
```
dmu 277
```

**Result :**
![Full Art Plains](assets/dmu_277.jpg)


# Advanced examples


## 1. Two cards, side by side

If you want to render two cards, side by side, just type two queries on two lines:

**💡 Example :**
```
Thrasios, Triton Hero
Tymna the Weaver
```

**Result :**
![Thrasios / Tymna](assets/thrasios_tymna.jpg)


## 2. Two-cards combo

If you want to render a two-cards combo, you can seperate the two queries by the `+` sign:

**💡 Example :**
```
Demonic Consultation + Thassa Oracle
```

**Result :**
![Demonic Consultation + Thassa's Oracle](assets/demonic_consultation_thassa_oracle.jpg)


## 3. Two-cards battles

If you want to render a battle between two cards, you can seperate the two queries by the `vs` sign:

**💡 Example :**
```
Esper Sentinel vs Rhystic Study
```

**Result :**
![Esper Sentinel vs Rhystic Study](assets/esper_sentinel_rhystic_study.jpg)


## 4. Three, four and five cards hands

If you want to render up to five cards, just type the queries on seperate lines:

**💡 Example :**
```
bro 278
bro 280
bro 282
bro 285
bro 286
```

**Result :**
![The Brother's War Lands](assets/bro_lands.jpg)


# Support me ❤️

If you want to support me or be kept up to date:

- Follow [me](https://bsky.app/profile/lheyberger.bsky.social) on Bluesky
- Follow [me](https://twitter.com/lheybergermtg) on Twitter
- Subscribe to the [Atom feed](./feed.atom)


[Messenger]:https://m.me/108575720841085
[Telegram]:https://t.me/cardrenderbot
[Dominaria United]:https://scryfall.com/sets/dmu
[Kaladesh Inventions]:https://scryfall.com/sets/mps
[Mana Crypt]:https://scryfall.com/card/mps/16/mana-crypt
[basic Plains]:https://scryfall.com/card/dmu/262/plains
[full art Plains]:https://scryfall.com/card/dmu/277/plains
[expedition]:https://scryfall.com/search?q=!expedition-map
