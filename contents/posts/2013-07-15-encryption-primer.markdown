---
layout: post
title: Cryptography Primer
date: 2013-07-15 20:37
author: Arif Widi Nugroho
comments: true
published: true
tags: security
thumbnail_image:https://lh3.googleusercontent.com/-e1-ir9ypUts/VnMeBtkOV_I/AAAAAAAAAL4/RhVNE0DVTpA/s512-Ic42/nasa-computer.jpg
cover_image: https://lh3.googleusercontent.com/-e1-ir9ypUts/VnMeBtkOV_I/AAAAAAAAALk/cvo4D4kRGoM/s0-Ic42/nasa-computer.jpg
cover_image_credit: Flickr/sdasmarchives
cover_image_credit_url: https://www.flickr.com/photos/sdasmarchives/7142833961/in/photolist-bTbTFF-otXi2j-nVQPYP-n9rcU9-bj1YYt-8DvP53-8DsGTK-7DciyW-oY1k5k-rj2dBj-cu7N3w-fqoBre-7GW3vA-bUzA79-kUBmeB-rj2Dt3-cGwSTs-fqmRFa-fqAsj7-fqmRep-cA7iYE-fqCRPQ-cu7K8f-bTbTnV-cE7acq-do6Ecy-brSvCA-8DsG3M-8DsG48-8DsGSK-8DsHCr-fq21Zf-bTbTAX-75wpJV-fpLiRX-fpNgdH-qr3Eta-otGFQz-octmDQ-bUy2Zf-fqoC5n-otYDDT-xVZqTZ-ovJjaB-dWrkiU-orX2vL-octVuQ-orWDrA-ocu4LP-octXrL
excerpt: In general, cryptography is used to transform a string of text into a convoluted gibberish that do not have any resemblance to the original text whatsoever to a person without access to its encryption key. That original string of text is called plaintext, and the resulting gibberish is called cyphertext.
---

The uproar caused by recent leak from [Edward Snowden](https://en.wikipedia.org/wiki/Edward_Snowden) still hasn't receded yet. There are various stances about privacy and government snooping floating around in the internet. Some say they have [nothing to hide](https://twitter.com/_nothingtohide). Others argue if the government can snoop you, and black-hat hackers can snoop the government, then we're royally screwed because anybody with money can pay the black-hats (or, gasp!, pay some corrupt government officials) to get data about anybody.

Politics aside, security must be taken seriously everytime we use internet. In this post I would like to talk about the basic of security in general computing today.

- [http://xkcd.com/1269/](http://xkcd.com/1269/)

Basic Cryptography
------------------

In general, cryptography is used to transform a string of text into a convoluted gibberish that do not have any resemblance to the original text whatsoever to a person without access to its encryption key. That original string of text is called plaintext, and the resulting gibberish is called [cyphertext](https://en.wikipedia.org/wiki/Ciphertext).

Based on the keys used for the encryption, there are two type of encryption: symmetric-key and asymmetric-key encryption. 

### Symmetric-Key Encryption

In symmetric-key encryption, the key that uses to encrypt the plaintext into cyphertext can be used to reverse the operation. Decrypting the resulting cyphertext using the same key will yield the same plain text. So, if two people can share an encryption key, they can communicate securely using that key. A simple example is sharing an encrypted rar file with your partner, your partner must know your encryption key (the password) in order to decrypt the rar file. So, you can go meet your partner and tell him your password.

What if it's impossible for you to meet your partner physically?  Supposedly, the secrecy of the data you want to transmit is very important and the balance of the world would be disrupted if it compromised. How can you tell him your password with a strong guarantee that nobody snoop it in between the transit? Using email? Email is generally transmitted in plain text, anybody in the network between you and your partner can read it. Using google chat? Then google can read it whenever it please. Using text message? Then the cellphone operator can read it. Also, [gsm security is considered broken](http://arstechnica.com/gadgets/2010/12/15-phone-3-minutes-all-thats-needed-to-eavesdrop-on-gsm-call/) and anyone with the right equipment can intercept your message. It's time to use an asymmetric-key encryption.

### Asymmetric-Key Encryption
In asymmetric-key encryption, you have two keys instead of one: the private keys (which you should guard with your life) and the public key (which you should share to anyone and their pets). So, why does it require two keys?

Anybody who know your public key can encrypt a plaintext that only you can decrypt (using your private key). Consider our example above (in which you need to transmit a super secret data to your partner). You can encrypt the password with your partner's public key, and send him the resulting cyphertext. Using his private key, he'll decrypt the cyphertext and get the password. Then you can send him your password protected rar archive to him.

Wait, why use rar? Why not simply encrypt the data using the public key instead?

Well, actually you can use anything that properly encrypt the data. [7-zip](http://www.7-zip.org/) support AES encryption (one of the commonly used symmetric-key encryption) too, just like rar. The reason why we didn't encrypt the whole data (presumably we have 1.3GB of it for the example) using the asymmetric-key encryption is it's really slow compared to the symmetric-key encryption. It is much more efficient (and faster) to encrypt the data using symmetric-key encryption and send the key/password through asymmetric-key encryption instead of encrypting the data wholesale using asymmetric-key encryption. Over time, the latest advances in cryptography will make the asymmetric-key encryption as fast as the symmetric-key encryption.


Can We Break The Encryption?
----------------------------

### Random Number Generator
Cryptography relies heavily on random numbers. For example, you don't want your keys to be easily guessable by anyone, you want it sufficiently random that the odds of successfully guessing your key is so low nobody even try to guess it (that's why you should favor randomly generated key over simple memorable string).

But how do we obtain a truly random number from inside a computer? A computer by itself cannot generate a truly random number. A computer is a state machine, so in theory, if you know the machine state at the time the secret random number generated, you might be able to guess that number.

A simple way to generate random numbers is the [Middle Square Method](https://en.wikipedia.org/wiki/Middle-square_method). First, pick a starting 5-digits value as a seed, for example: 12345. Next, compute the square of it: 12345 * 12345 = 152399025. Next, pick the middle five digits from the result: 23990. That's our random number. To get the next random number, just repeat the process using the previously generated number as the new seed: 23990 * 23990 = 575520100 -> 55201, and so on.

Notice that the value of generated random number depend on the previous number. If you know the original number that used as the seed, you can easily predict the random number generated using this method. This random number generator is called Pseudo-Random Number Generator (PRNG) because it doesn't actually generate truly random numbers. Note that the Middle Square method is very simple and not used in modern system anymore, but the concept is still the same: pseudo-random number generator depends on seed number and internal states to generate a number. If the seed and the internal states is known, then the anyone can easily predict the next random number. (in Middle Square method, there is only one internal state variable and it's always set to the previously generated number).

A pseudo-random number generator that can generate truly unpredictable random number is called Cryptographicaly Secure Pseudo-Random Number Generator (CSPRNG). One requirement for CSPRNG is nobody should be able to predict the next number by analyzing the previous numbers. Since we can predict the next number generated by the Middle Square method from the previous numbers, we can clearly see that the Middle Square method is not cryptographically secure and should not be used in real life applications.

Cryptographicaly Secure Pseudo-Random Number Generator must be fed with multiple sources of randomness to ensure its unpredictability. That source of randomness could be a network interface, human input, hard-drive needle position, ambient city noise, or even [cosmic rays](http://phys.org/news1147.html). The more sources of randomness available, the better.

Starting from the Ivy Bridge processors, Intel includes an on-chip random number generator along with a new instruction to make uses of it, [RDRAND](http://en.wikipedia.org/wiki/RDRAND). It can generate a random bit for each clock cycle. Modern operating systems use the instruction as additional source of randomness for their built-in random number generator.

There are [concerns regarding the use of RDRAND in linux kernel](https://news.ycombinator.com/item?id=6038473). Since RDRAND uses an on-chip random number generator, somebody at processor manufacturing plant could replace the chip with the one with faulty random number generator, which would potentially compromise security on linux system.

Should we worry that an exploit to random number generator could compromise our security? Probably not, but keep it in mind though.

Recently, [a bitcoin exchange got hacked](http://forum.ovh.com/showthread.php?t=88277) because the attacker could take advantage of its dedicated server provider's password reset link. Apparently, the password reset link was not random enough and can be guessed by attacker.

Tips: if your application is running under Linux, always use /dev/urandom to get your random numbers. Many people don't like it because it's slow, but keep in mind that /dev/urandom is cryptographically secure. If you're getting the random numbers from a built-in function on your programming language/library/framework of choice, be sure to check the documentation to see if it's cryptographically secure. Not all languages/frameworks pull the random number from /dev/urandom.

See also:

- [The Factoring Dead: Preparing for the Cryptopocalypse](http://www.slideshare.net/astamos/bh-slides)
- [Crypto experts issue a call to arms to avert the cryptopocalypse](http://arstechnica.com/security/2013/08/crytpo-experts-issue-a-call-to-arms-to-avert-the-cryptopocalypse/)
- [The code monkey's guide to cryptographic hashes for content-based addressing](http://valerieaurora.org/monkey.html)
- [A Stick Figure Guide to the Advanced Encryption Standard (AES)](http://www.moserware.com/2009/09/stick-figure-guide-to-advanced.html)
- [random.org](http://www.random.org/)
- [Random Number Bug in Debian Linux](https://www.schneier.com/blog/archives/2008/05/random_number_b.html)
- [Petition to Linus Torvalds: Remove RdRand from /dev/random](http://www.change.org/en-GB/petitions/linus-torvalds-remove-rdrand-from-dev-random-4/responses/9066), [discussion](https://news.ycombinator.com/item?id=6359892)
- [Why secure systems require random numbers](http://blog.cloudflare.com/why-randomness-matters)
- [Javascript Cryptography Considered Harmful](http://www.matasano.com/articles/javascript-cryptography/)

### Quantum Computing

[Quantum computing](http://www.mat.ucm.es/catedramdeguzman/old/01historias/haciaelfuturo/Burgos090900/quantumcomputingSciAmer/0698gershenfeld.html) has gain a lot of buzz recently, especially those [D-Wave](http://en.wikipedia.org/wiki/D-Wave_Systems) stuff. But what is quantum computing and what is the implication for our daily (internet) life?

#### Quantum Superposition

Remember Schrödinger cat? It's often used to illustrate quantum superposition. The cat is in the box, with poison and radioactive trigger that have 50/50 chance of releasing the poison to the poor cat. In the end, is the cat alive or dead? Not that simple. The poor cat is in a superposition of state and both alive and dead. The moment we take a peek to see how the poor cat's doing, the quantum superposition collapsed and the cat falls into one of the two possible state: alive or dead.

That cat analogy doesn't make any sense, right? How could the cat both alive and dead at the same time before we take a look at it? But it highlights an important feature of quantum superposition: the quantum superposition state collapse into in one of the possible states the moment we measure it.

#### Qubit

Ok, the quantum superposition is neat because it can represent multiple states simultaneously. But what's that got to do with quantum computing?

The building block of traditional computing, as we all know very well, is *bit*. A bit can represent two states: either 1 or 0. In quantum computing, the building block is *qubit* (quantum bit). Because qubit has quantum superposition property, it can be in multiple states at the same time; it can contain both 1 and 0 until the moment you try to measure it, at which point it would collapse into either 1 or 0. This is indeed truly mind blowing.

Each qubit can have both 0 and 1 simultaneously, and each state has its own probability coefficient. To describe a qubit, we would need two numbers to store probability coefficients for 0 and 1. To describe two qubits, we would need 4 numbers, and so on in n^2 relation. This illustrates the strength of quantum computer: we would need a traditional computer capable to store 2^100 numbers to represent a 100 qubits quantum computer. That means we need millions of [yottabyte](http://en.wikipedia.org/wiki/Yotta-) just to represent a mere 100 qubits quantum computer!

#### Quantum Teleportation

Another bizzare phenomenon is quantum teleportation. After a pair of particles interact with each other and separated, if one particle has its state changed, the other would have its state changed too, no matter what distance they are separated. It is as if the particles can sense what happen to its pal and react accordingly, just like in horror movies.

Again, what's that got to do with quantum computing?

In 1994, a researcher from AT&T, Peter W. Shor found a way to use quantum teleportation to find prime factors of an integer. It turns out to be much faster than any traditional computer can compute. It is now known as [Shor's Algorithm](http://en.wikipedia.org/wiki/Shor's_algorithm).

In asymmetric-key encryption, the public and private keys must be somehow related for the encryption algorithm to work. Therefore, the private keys can be recovered with some forms of factorization from the public key, except doing so is computationally hard, and even virtually impossible (takes too much time, like *billions* of years) if the key is sufficiently long.

With a sufficiently big quantum computer, factoring private key from public key is feasible using Shor's algorithm. The task that could takes billions of years now can be accomplished in a couple years, for instance. That's why [cryptography researchers now scramble to produce new cryptography algorithms and methods](http://pqcrypto.org/) in the event that quantum computer is finally big enough to pose a threat for cryptography world. 


Forward Secrecy
-------------
Later


Securing Email
--------------
There is no doubt that email plays an important role in our internet life. We can't even register for a new account on many website without email! But how does email really work actually?

### Simple Mail Transfer Protocol

The SMTP (Simple Mail Transfer Protocol) is used by email servers to exchange emails to each other. In fact, OSX and most linux distributions ship with `sendmail`, an email transport agent. If you're on a Mac or Linux, open a terminal and type the following code to send yourself an email (replace my email address with yours):

	#!bash
	# Sending an Email From Command Line Interface Using Unix Sendmail
	sendmail arif@sainsmograf.com << EOF
	Hello, just a test email from command line!
	EOF


Soon, you'll receive an email from `<username>@<hostname>` (example: arif@arifs-macbook-pro.local). If the command run successfully but you never receive any email, chance that:

- Your ISP block communication to port 25 to stop [spambots](https://en.wikipedia.org/wiki/Spambot)
- Your email provider (gmail, yahoo, etc) ban your ip range (possibly due to spambots, damn spambots!)

If you did receive the email, you might not be able to reply to it unless you have configured your hostname properly.

In the above example, my computer act as an email server and communicate directly to sainsmograf.com's mail server. Note the *email server* part. If you're using Outlook or Thunderbird to connect to smtp server, your computer act as a *user* of that server. Here, `sendmail` act as an email server delivering email from its user (me) to another email server (sainsmograf.com).

### Can Somebody Snoop My Email?

By default, `sendmail` uses unencrypted protocol. The email sent using the `sendmail` command in the previous section is not encrypted, and anybody between you and your destination server can easily read your email. The good news is, sendmail does support SSL and can encrypt your email messages during transmission. However, sendmail's SSL encryption won't protect your email if the recipient access his mailbox via unencrypted connection (for example, plain old POP3 without SSL).

You may need to encrypt your email message yourself to guarantee that nobody snoop your email, but how?


### Pretty Good Privacy (PGP)

A popular way to encrypt your email messages is using PGP. A widely used implementation of PGP is GNU Privacy Guard (GnuPG, or GPG). [If somebody asks you to use PGP/GPG](http://www.wired.com/threatlevel/2013/06/signed-bda0df3c/), don't be confused. What he means is you should use GnuPG to exchange PGP-encrypted message with him.

After getting GPG installed ([OSX](https://gpgtools.org/), [Linux](https://help.ubuntu.com/community/GnuPrivacyGuardHowto), [Windows](http://gpg4win.org/)), lets use it to encrypt our email!

#### Generate Private/Public Keys Pair

PGP uses asymmetric encryption (discussed above), so the first logical step to encrypt your email is generating your public and private keys. Run the following command from your terminal to generate your keys pair:

	#!bash
	# Generate Private/Public Keys Pair
	gpg --gen-key


You'll see the following output:

	#!text
	gpg (GnuPG) 1.4.13; Copyright (C) 2012 Free Software Foundation, Inc.
	This is free software: you are free to change and redistribute it.
	There is NO WARRANTY, to the extent permitted by law.

	Please select what kind of key you want:
	   (1) RSA and RSA (default)
	   (2) DSA and Elgamal
	   (3) DSA (sign only)
	   (4) RSA (sign only)
	Your selection?


Select the default by entering `1`. You'll be prompted another questions. Just answer them accordingly. Eventually, GPG will ask you to create a passphrase:

	#!text
	gpg (GnuPG) 1.4.13; Copyright (C) 2012 Free Software Foundation, Inc.
	This is free software: you are free to change and redistribute it.
	There is NO WARRANTY, to the extent permitted by law.

	Please select what kind of key you want:
	   (1) RSA and RSA (default)
	   (2) DSA and Elgamal
	   (3) DSA (sign only)
	   (4) RSA (sign only)
	Your selection? 1
	RSA keys may be between 1024 and 4096 bits long.
	What keysize do you want? (2048) 4096
	Requested keysize is 4096 bits
	Please specify how long the key should be valid.
	         0 = key does not expire
	      <n>  = key expires in n days
	      <n>w = key expires in n weeks
	      <n>m = key expires in n months
	      <n>y = key expires in n years
	Key is valid for? (0)
	Key does not expire at all
	Is this correct? (y/N) y

	You need a user ID to identify your key; the software constructs the user ID
	from the Real Name, Comment and Email Address in this form:
	    "Heinrich Heine (Der Dichter) <heinrichh@duesseldorf.de>"

	Real name: Arif Widi Nugroho
	Email address: arif@sainsmograf.com
	Comment:
	You selected this USER-ID:
	    "Arif Widi Nugroho <arif@sainsmograf.com>"

	Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? o
	You need a Passphrase to protect your secret key.


Now, enter a long passphrass, but don't forget it! If you forgot your passphrase, there is no way to recover it and you can never decrypt all messages that has been encrypted with your pulic key. Consider using a good password manager to store your complicated passphrase.

Now that you have your own private and public keys, you should share your public key to everyone! To print your public key, use this command (replace my email address with yours):

	#!bash
	# Print PGP Public Key
	gpg -a --export arif@sainsmograf.com


And the result:

	#!text
	-----BEGIN PGP PUBLIC KEY BLOCK-----
	Version: GnuPG v1.4.13 (Darwin)

	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
	TN4ixRhleA==
	=dEg9
	-----END PGP PUBLIC KEY BLOCK-----


There, you have my public key. Save that key into a file called `public.key` and import that public key using the following command:

	#!bash
	# Importing a Public Key
	gpg --import public.key


Now it's time to send myself a secret email! To encrypt a message, first, save the message inside a file called `plain.txt`. Encrypt the file using the following command: 

	#!bash
	# Encrypt a Message
	gpg -a -e -u sender@example.com -r recipient@example.com plain.txt


Replace `sender@example.com` with your email message and `recipient@example.com` with your recipient. Make sure to import your recipient's public key first!

The encrypted message would be stored inside `plain.txt.asc` file:

	#!text
	# Encrypted Message

	-----BEGIN PGP MESSAGE-----
	Version: GnuPG v1.4.13 (Darwin)

	hQIMA1wNV+AyV/2aAQ/8Dzd4h2MnY/ZNH2HO4aUUTGbgZfLWrWg1VJOKeldXw5GY
	5FkAuywDfCMha9/GH3UHh9vLYjmCHsjf4BeMgA5Z5Z3Hzwp/+kI0Nv+N07L5+UVG
	qIdXKjKuc/lBgB5NOrz8Q+7SSBbvQgKgywravwDxtzt/lhCI0J5SjUo9X8ehuH4q
	qDB+yZtrGYKdw1Ww4JIgRhV+Lsbjt2jhB2s62RirotyX6sKKVn0EfATcdNKBOuWW
	F6pLP7h0AqW0PCq3HGG8hnGeIu7Kef5xCIuJQCb7rgs0TP09NAP5fugMK5I74S2P
	DYrQh66mGDrelud3jFq1vKguqOOSrEw5SEnRSG3TeUbjHPxMenvVYkxwhL7p0sK0
	1il3s7PMrDuqFEu7SrTRUDUTgbJtrV0hgJKWi0x/6SFKOzodvW8ka5MzIpqKj3KC
	jf48s4xfd67uofol79cUuVr4zwWbe6RpDEmRt1JS3hxXTWa0dQN2WNCic0OFRXHt
	UQGKJoV2I1U2nEc2DjZNca4f9zuPvjyxCT8gp11E6HJ31WRbln5qixF7W3RA148x
	3SC7ThZp687bMGxUTUQimpy4FkrWtvQzYfoILAlJbmFiOUB1ww6q8fWMf3mV4e1n
	h1K2bpb4Syu2eeflgUxNdeLfjBmNJgMIGgsHMRspTAVqHo+KJzb1JanvuyVPCcPS
	XAGb2WhILc/NRNKodV8LZsqBK6nxCCQM+3mooLUl5KoccG5VVealdf5epN7sbnjg
	QlH+2rQjLwGGZH76bDBNhblC2M8tAUxU3BNUd/ax9EspN16IpHgWXNGNvUyh
	=rJyP
	-----END PGP MESSAGE-----


Now send that file via email to your recipient. Here is how to send the encrypted message using `sendmail`:

	#!bash 
	# Send The Encrypted Message Using Sendmail
	cat plain.txt.asc | sendmail arif@sainsmograf.com


![An Encrypted Email!](https://lh6.googleusercontent.com/-OX554vlxHAA/UfD3nvJBfSI/AAAAAAAAACw/nRf9kju8m8c/d/Screen+Shot+2013-07-25+at+5.01.40+PM.png "An Encrypted Email!")


To decrypt the message, save the message content into a file called `cipher.txt` and run:

	#!bash
	# Decrypting a PGP Message
	gpg -d cipher.txt


It would print out the decrypted message:

	#!text
	gpg: encrypted with 4096-bit RSA key, ID 3257FD9A, created 2013-07-25
	      "Arif Widi Nugroho <arif@sainsmograf.com>"
	This is a secret email!


You can encrypt binary data too, or use it to encrypt your off-site backup data. Check the man page (`man gpg`) or consult the following resource:

- [GPG Cheat Sheet](http://irtfweb.ifa.hawaii.edu/~lockhart/gpg/)
- [Working with PGP and Mac OS X](http://www.robertsosinski.com/2008/02/18/working-with-pgp-and-mac-os-x/)

That's just an overview of how PGP works. If you use an email client or install an email client plugin that support PGP, after creating your public/private keys pair, the process is mostly automatic. No need to go back and forth to the command line interface!

![Sending An Encrypted Email With OSX Mail App + GPGTools](https://lh4.googleusercontent.com/-50Khh48XTNY/UfU1QpkjNWI/AAAAAAAAAD4/Ej3sEP0yAsI/w652-h418-no/OSX+Mail+App+%252B+GPGTools.png "Sending An Encrypted Email With OSX Mail App + GPGTools")

### S/MIME (Secure/Multipurpose Internet Mail Extensions)

Almost the same with PGP, except you don't generate your public/private keys pair yourself. Instead, you obtain them in the form of digital certificate from a certificate authority.

When you send an email signed with S/MIME, your recipient will automatically get your public key. Also, if you obtain your certificate from trusted authority, such as VeriSign, your recipient's email client will automatically validate your message with no manual process involve. Also, unlike PGP, most email clients support S/MIME.

Simply obtain a certificate from a trusted certificate authority, install it, and ready to go! The drawback is you need to pay to get a certificate. [You can get a certificate with one year validity from VeriSign here (about $20)](http://www.symantec.com/verisign/digital-id?tid=gnps).

- [S/MIME Guide](http://arstechnica.com/apple/2011/10/secure-your-e-mail-under-mac-os-x-and-ios-5-with-smime/)
- [Free S/MIME Certificate - not trusted by many email clients](http://www.comodo.com/home/email-security/free-email-certificate.php)


Next:

Verifying Website Security
--------------------------  
Is the website you visit frequently actually secure? Are you sure the website you visit is actually the real website, not some hacker rig impersonating the real website?

- [EFF has a nice diagram about connection privacy](https://www.eff.org/pages/tor-and-https). Lets discuss it!
- Anything without HTTPS is insecure. Don't submit important information over plain http!

How SSL (HTTPS) Works
---------------------
- Initial handshake uses asymmetric encryption to exchange symmetric keys. Therefore HTTPS requires two roundtrip to server. SPDY protocol solve this (but chrome-only).
- Validation: The connection might be encrypted, but how can you be sure that the guys on the other side of the cable are not an imposter? Someone I trusted should confirm that I'm indeed not talking to a fake imposter.
- [Forward Secrecy](https://community.qualys.com/blogs/securitylabs/2013/06/25/ssl-labs-deploying-forward-secrecy)

Deep Net
--------
- We need to go [deeper](https://www.torproject.org/).

