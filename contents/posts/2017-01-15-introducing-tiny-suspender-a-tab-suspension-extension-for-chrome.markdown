---
author: Arif Widi Nugroho
comments: true
cover:
  image: ''
  image_credit: ''
  image_credit_url: ''
  image_type: parallax
date: 2017-01-15 18:39:27.232323
excerpt: ''
layout: post
published: true
tags:
- Chrome
- Extension
thumbnail:
  image: https://lh3.googleusercontent.com/5_tHqceVvFxKysiylR_6b793XF9DSJQyORnjh0phH9SbYkS9g8ClBB_61PyPqXNEG1BrJG3KsLVKulqUhkJewvbLaujjeZ0W46npgkyp_1Vk18-bnVuIpVU4Ew-KFQznEMoYUsM6NX1vrar7cNXLQ__cUvJkn6N6gMRs_CLT5t0TzNiVwg8EDHDxRuNBCGCatnkh0WVnRXaoBPbhF3txvmWm5i1BMjsEBCbUuDcf87Dvat2HMJ-IMJjGe0-4NHHiU1hVVlE1vebX835ToZ7Kuk4yVyMJG673X1upugDS9hTKs0FKrRiYAuE2lNLPxJ91p6nxmvpvJ1dUueVA158RLzmpv_exdXcejcMEQm3WCvrzoBEGv9NtF_rHeXjSRs9UQbwFVHz9mUXTBwjiX0Wxxjkem-LsnbxTZpCgl7Md30O7BhnXKFSjam9Rt3rDV2q_8qcHdXM8wBBdpIfh-6TE7qTss8bSmCBl3Oz-q7OWmB4ra-mCnpnNUlHjJnKA1gadno7sBeZwb73tcUHpQLTXf8igWLWM0w3D_x4q--E6DY4v68q1snmRaWs0IugJImqrkipKaY6dthV4ddXdaOxrPJSmBzs6Kedq8fj3Awga42nbF4SxvK9Y=w512-h300-no
cover:
  image: https://lh3.googleusercontent.com/5_tHqceVvFxKysiylR_6b793XF9DSJQyORnjh0phH9SbYkS9g8ClBB_61PyPqXNEG1BrJG3KsLVKulqUhkJewvbLaujjeZ0W46npgkyp_1Vk18-bnVuIpVU4Ew-KFQznEMoYUsM6NX1vrar7cNXLQ__cUvJkn6N6gMRs_CLT5t0TzNiVwg8EDHDxRuNBCGCatnkh0WVnRXaoBPbhF3txvmWm5i1BMjsEBCbUuDcf87Dvat2HMJ-IMJjGe0-4NHHiU1hVVlE1vebX835ToZ7Kuk4yVyMJG673X1upugDS9hTKs0FKrRiYAuE2lNLPxJ91p6nxmvpvJ1dUueVA158RLzmpv_exdXcejcMEQm3WCvrzoBEGv9NtF_rHeXjSRs9UQbwFVHz9mUXTBwjiX0Wxxjkem-LsnbxTZpCgl7Md30O7BhnXKFSjam9Rt3rDV2q_8qcHdXM8wBBdpIfh-6TE7qTss8bSmCBl3Oz-q7OWmB4ra-mCnpnNUlHjJnKA1gadno7sBeZwb73tcUHpQLTXf8igWLWM0w3D_x4q--E6DY4v68q1snmRaWs0IugJImqrkipKaY6dthV4ddXdaOxrPJSmBzs6Kedq8fj3Awga42nbF4SxvK9Y=w1024-h600-no
  image_type: parallax
title: 'Introducing Tiny Suspender: A Tab Suspension Extension for Chrome'
excerpt: Like The Great Suspender, but with different set of features and implementation.

---

# Introducing Tiny Suspender: A Tab Suspension Extension for Chrome

<i>TL;DR Download it here: [https://chrome.google.com/webstore/detail/tiny-suspender/bbomjaikkcabgmfaomdichgcodnaeecf](https://chrome.google.com/webstore/detail/tiny-suspender/bbomjaikkcabgmfaomdichgcodnaeecf) </i>

If you use Chrome as your primary browser, you'll probably aware of its memory and resource hogging nature. Every time you open a new tab, a new process get spawned that dedicated only for that tab. It's great from reliability and security stand point, but not so great when you try to cut down resource consumption which can be critical if you're on battery power.

The Chrome dev team has performed various optimization with great results. Chrome hogs less resources now, which is great for casual users. But for users who open dozens and dozens of tabs at the same time (even hundreds!), this improvement is not enough. That's why we rely on tab suspender extensions such as The Great Suspender to reduce Chrome's CPU and memory usage when it has so many background tabs.

I've been using The Great Suspender for a while, and it actually works great. One day, I decided I want to build a suspender extension on my own, and the result is [Tiny Suspender](https://chrome.google.com/webstore/detail/tiny-suspender/bbomjaikkcabgmfaomdichgcodnaeecf). It actually has been released in Chrome Web Store for a while now. It even gather ~250 users so far. Thanks to feedbacks from those brave users (they're essentially alpha-testing the extension on their own!), Tiny Suspender finally has all features I ever want. In fact, without those users I probably would leave Tiny Suspender in barely usable state (since it was good enough for my own use). Thanks a lot guys!


### So what's so special about Tiny Suspender?

Usual features you would expect from a suspender plugin:

- Automatic and manual tab suspension: Automatically suspend background tabs, or manually suspend the tabs yourself

- Form Detection: Tiny Suspender will also try to detect active form to avoid automatically suspending page with unsubmitted form

- Audio Detection (optional): prevent autosuspending tab that plays music in the background.

- Snooze: Temporarily prevent autosuspension on a specific tab

- Whitelist: Excludes specifics domains, pages, tabs or pinned tabs.

- Keyboard Shortcuts: Suspend tabs without moving your hand away from your keyboard.


Tiny Suspender also includes an experimental feature: suspending background tabs using [Chrome Tab Discard API](https://developers.google.com/web/updates/2015/09/tab-discarding). This experimental feature must be enabled from Tiny Suspender settings and can only works on background tabs, but it's very promising. It can restore the state of suspended page quite reliably, including form state and scroll position. But it does has its share of annoyance (which is why I disable it by default), such as it would reloads all suspended tabs if you ever restart your browser and restore your last browsing session.

My goal for Tiny Suspender is to keep it true to its name: tiny. I won't add any dependencies if I can help it to keep the code size (and extension memory footprint) minimal. But of course I'm open to suggestions. In fact, several of current Tiny Suspender's features are there thanks to users' suggestions. Shoot me an email if you have any suggestion or bug report!

Extension page: [https://chrome.google.com/webstore/detail/tiny-suspender/bbomjaikkcabgmfaomdichgcodnaeecf](https://chrome.google.com/webstore/detail/tiny-suspender/bbomjaikkcabgmfaomdichgcodnaeecf)

Repository: [https://github.com/arifwn/TinySuspender](https://github.com/arifwn/TinySuspender)

