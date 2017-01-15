---
author: Arif Widi Nugroho
comments: true
cover:
  image: ''
  image_credit: ''
  image_credit_url: ''
  image_type: parallax
date: 2016-12-10 16:39:06.412485
layout: post
published: false
tags:
- sysadmin
- linux
thumbnail:
  image: ''
title: Let's Backup Our Servers!
excerpt: Backup is something that we all wish we had when faced with a catastrophic loss of data. There are 1001 ways to backup your data, but this is the setup I used to create daily redundant off-site backup for production servers using Tarsnap, ZBackup, and Rsync.
---

# Let's Backup Our Servers!

Backup is something that we all wish we had when faced with a catastrophic loss of data. There are 1001 ways to backup your data, but we're often just too lazy (or simply forgot) to setup one:

> There is no way my server would get corrupted! I hosted it on AWS!

Except [EBS has expected to have an annual failure rate between 0.1% - 0.2%](https://aws.amazon.com/ebs/details/#AvailabilityandDurability). That means, at the very least, 1 out of 1000 EBS volumes on AWS will encounter an EBS failure within a given year. If you're (un)lucky, that one EBS volume could be in your server!

> My host would take care of such basic thing.

Except they most certainly don't. Most VPS providers expect their customer to backup their own data, or purchase an additional plan for backup purpose (snapshotting, off-site NFS mounts, etc). Even if you're on a shared hosting provider, they are likely to have inadequate backup plan for cost saving reason (especially now with a lot of competitors driving down price). When a hosting company forced to cut down cost, the first thing to do is tuning down their costly backup policy.

> My data is worthless. If it were gone I won't lose anything valuable.

Sure, now it might be just a silly side project. Why bother backing it up at all? Except when you suddenly gain overnight success and forgot you have no back up in place. [Don't be that bitcoin exchange site](http://siliconangle.com/blog/2011/08/01/third-largest-bitcoin-exchange-bitomat-lost-their-wallet-over-17000-bitcoins-missing/) that lost all of their data when updating their server configuration just because the forgot to set up an off-site backup for their *silly* side project and ended up losing their customers' money.


# How much will it cost to backup all my production data?

- Storage cost scale linearly. The more backup archives you retain the more you pay.
- However, how much space you use depends on your backup strategy:
  - Fast access: lightly compressed (or not at all). All data is essentially duplicated on each archive.
  - High efficiency: Heavy compression and deduplication. Huge storage saving, at the cost of data access speed.
  - Combine both strategy: Fast access for recent backup archives (say, the last 7 days of data) and high efficiency for everything else


- tarsnap vs zbackup

- offsite rsync

- backblaze b2: free upload!

- backup rotation

