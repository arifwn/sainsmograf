---
layout: page
title: T9 Predictive Text Input Emulator
url: /labs/t9-emulator/
---

This is a [T9 Predictive Text Input Emulator](http://en.wikipedia.org/wiki/T9_(predictive_text)), implemented using [Trie](http://en.wikipedia.org/wiki/Trie).

Hint: use cycle button to cycle through all matching words.

<iframe style="
    width: 340px;
    height: 500px;
    padding: 20px 5px 5px 5px;
    background: white;
    border: none;
    box-shadow: inset 0 0 7px rgba(0,0,0,0.7);
" src="https://www.sainsmograf.com/t9-emulator/embed.html"></iframe>

<p><a href="https://www.sainsmograf.com/t9-emulator/" target="_BLANK">Open in New Window</a></p>

##Limitation

- It's not context-aware or grammar-aware. No smart result ordering.

##Sample words

- testing: 8378464
- super: 78737
- mario: 62746
- legend: 534363
- and many more (over 2MB of english words)&hellip;

## Links

- [Github Project](https://github.com/arifwn/t9-emulator)
- [Javascript Trie Prediction](https://github.com/jrolfs/javascript-trie-predict/blob/master/predict.js)