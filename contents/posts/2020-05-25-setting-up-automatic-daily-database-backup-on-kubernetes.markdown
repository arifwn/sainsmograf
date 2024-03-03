---
author: Arif Widi Nugroho
comments: true
cover:
  image: '/media/uploads/container.jpg'
  image_credit: 'Guillaume Bolduc'
  image_credit_url: 'https://unsplash.com/@guibolduc?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'
  image_type: parallax
date: 2020-05-25 10:19:29.430441
layout: post
published: true
tags:
- kubernetes
- container
- infrastructure
thumbnail:
  image: '/media/uploads/container.jpg'
title: Setting Up Automatic Daily Database Backup on Kubernetes
excerpt: ... and upload them to Backblaze B2 and RSync.net (Updated on 2024-03-03)

---

# Setting Up Automatic Daily Database Backup on Kubernetes (Updated: 2024-03-03)

Kubernetes has been supporting [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) for a while now, so it's a no brainer to deploy a database app in a Kubernetes cluster. Statefulset allows your pods to maintain sticky, persistent IDs, as well as persistent storage, making it ideal for database apps. Still, even with persistent storage, you should always configure automatic offsite backup when deploying a database app on a Kubernetes cluster. This would ensure your data survives any disaster that might befall your new shiny cluster.

Automatic offsite backups can be a hassle, but it doesn't have to be. In this post, I'm going to setup an automatic daily backup on a MySQL pod into a Backblaze B2 bucket.

## Step 1: Automatically Dump All Databases into a Persistent Volume

I want to dump all databases inside a MySQL pod into a persistent volume. Each database will be dumped into a separate file (so I can load them individually as needed later) on a persistent volume which will be uploaded into a Backblaze B2 bucket later. I'll use Kubernetes' new [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) workload to schedule a daily database dump job.

It's quite annoying to set this up over and over again, so I packed a small MySQL backup script into a container (`arifwn/container-backup:mysql`) suitable for use inside a Kubernetes' CronJob workload. This docker image can be used to backup a specific database or all databases. The source code is availabe on my github repo here: [https://github.com/arifwn/container-backup](https://github.com/arifwn/container-backup).

	#!yaml
    apiVersion: batch/v1
    kind: CronJob
    metadata:
      name: backup-all-mysql80-db
      namespace: backups
    spec:
      concurrencyPolicy: Forbid
      failedJobsHistoryLimit: 1
      jobTemplate:
        spec:
          backoffLimit: 3
          completions: 1
          template:
            spec:
              containers:
              - env:
                - name: DBNAME
                  value: ALL # specify a specific database name here, or ALL to backup all databases
                - name: HOST
                  value: mysql80.mysql.svc.cluster.local # your MySQL host
                - name: USER
                  value: root
                - name: PASSWORD
                  value: absolutelysecret
                - name: PORT
                  value: "3306"
                image: arifwn/container-backup:mysql80
                imagePullPolicy: IfNotPresent
                name: backup-all-mysql80-db
                volumeMounts:
                - mountPath: /dump
                  name: mysql80-backup-volume-all
                  subPath: mysql80
              volumes:
              - name: mysql80-backup-volume-all
                persistentVolumeClaim:
                  claimName: backup-storage-pv-claim
      schedule: 0 2 * * *
      successfulJobsHistoryLimit: 3

This will create a new `CronJob` workload entry on the Kubernetes cluster that run every 2:00 AM everyday. I also mounted a persistent volume (created beforehand) that will be used to store the resulting `.sql` dumps. We'll mount this volume in another `CronJob` entry to upload the content to Backblaze B2 later.

Using PostgreSQL? No problem!


	#!yaml
    apiVersion: batch/v1
    kind: CronJob
    metadata:
      name: backup-all-postgres16-db
      namespace: backups
    spec:
      concurrencyPolicy: Forbid
      failedJobsHistoryLimit: 1
      jobTemplate:
        spec:
          backoffLimit: 3
          completions: 1
          template:
            spec:
              containers:
              - env:
                - name: DBNAME
                  value: ALL
                - name: HOST
                  value: postgres16.database.svc.cluster.local
                - name: PASSWORD
                  value: absolutelysecret
                - name: PORT
                  value: "5432"
                - name: USER
                  value: postgres
                image: arifwn/container-backup:postgresql-16
                imagePullPolicy: IfNotPresent
                name: backup-all-postgres16-db
                volumeMounts:
                - mountPath: /dump
                  name: postgres16-backup-volume-all
                  subPath: postgres16
              volumes:
              - name: postgres16-backup-volume-all
                persistentVolumeClaim:
                  claimName: backup-storage-pv-claim
      schedule: 0 2 * * *
      successfulJobsHistoryLimit: 3


## Step 2: Upload to a Backblaze B2 Bucket

Next is uploading the `.sql` files generated from the last step into a Backblaze B2 bucket. [Backblaze B2](https://www.backblaze.com/b2/cloud-storage.html) is a (very) cheap cloud storage service ($0.006/GB/Mo) from Backblaze with free ingress bandwidth cost, perfect for storing large backup data offsite. Egress is also cheap (free up to 3x monthly storage, then $0.01/GB) and very fast, unlike some other cheap cloud backup solution (e.g. AWS Glacier).

I also packed my trusty B2 backup script into a docker image (`arifwn/container-backup:b2`). This image will compress each top-level folder in the mounted volume into a `.tar.gz` archive and upload it into the specified B2 bucket. The image will also perform daily cleanup on the target bucket so only the last 7 daily backups, the last 8 weekly backups, and the last 12 monthly backups retained. The source code is availabe on my github repo here: [https://github.com/arifwn/container-backup](https://github.com/arifwn/container-backup).

    #!yaml
    apiVersion: batch/v1
    kind: CronJob
    metadata:
      name: backblaze-backup
      namespace: backups
    spec:
      concurrencyPolicy: Forbid
      failedJobsHistoryLimit: 1
      jobTemplate:
        spec:
          backoffLimit: 3
          completions: 1
          template:
            spec:
              containers:
              - env:
                - name: B2_ACCOUNT_ID
                  value: accountid # replace with your B2 account id
                - name: B2_API_KEY
                  value: secretkey # replace with your B2 API Key
                - name: BUCKET_NAME
                  value: mysql-backup
                - name: SOURCE_DIR
                  value: /source/
                - name: SYSTEM_NAME
                  value: My Cluster
                image: arifwn/container-backup:b2
                imagePullPolicy: IfNotPresent
                name: backblaze-backup
                resources:
                  limits:
                    cpu: "100m" # don't use too much cpu to avoid starving the node
                volumeMounts:
                - mountPath: /source
                  name: source-data-volume
              volumes:
              - name: source-data-volume
                persistentVolumeClaim:
                  claimName: backup-storage-pv-claim
      schedule: 30 2 * * *
      successfulJobsHistoryLimit: 3

This will create a new `CronJob` workload entry on the Kubernetes cluster that run every 2:30 AM everyday (plenty of time for the database dump cron to complete). The cron will compress all data found inside the mounted volume (each top-level folder will be compressed into a separate `.tar.gz` archive), upload them into a B2 bucket, and remove any old backup archives except the last 7 daily backups, the last 8 weekly backups, and the last 12 monthly backups.

And that's it! The database is now backed up automatically every night to a B2 bucket. It only take minutes to setup and you can sleep soundly at night knowing your data is safe from random cluster failure. Don't forget to setup `CronJob` failure alert so you'll get notified when uploads failed (the B2 backup image will return with non-zero exit code on failure).

## Step 3 (Optional): Upload to an Offsite Server with RSync

You can't have enough backup these days. While having copies of your data on B2 is great for your peace of mind, having yet another copy safely stored in another backup provider is great for redundancy. [RSync.net](https://rsync.net/) is a great backup provider and supports automatic daily snapshots so you can go back in time to retrieve previous version of your file. All you need to do is generating a new ssh key and [upload them to your rsync.net server](https://www.rsync.net/resources/howto/ssh_keys.html), then use those keys on the config below.

    #!yaml
    apiVersion: batch/v1
    kind: CronJob
    metadata:
      name: rsync-backup
      namespace: backups
    spec:
      concurrencyPolicy: Forbid
      failedJobsHistoryLimit: 1
      jobTemplate:
        spec:
          backoffLimit: 3
          completions: 1
          template:
            spec:
              containers:
              - env:
                - name: TARGET
                  value: youraccount@yourhost.rsync.net:your-target-path # replace with your rsync.net account name
                envFrom:
                - configMapRef:
                  name: rsync-backup-base-env-config
                image: arifwn/container-backup:rsync
                imagePullPolicy: "IfNotPresent"
                name: rsync-backup
                resources:
                  limits:
                    cpu: "100m" # don't use too much cpu to avoid starving the node
                volumeMounts:
                - mountPath: /source
                  name: source-data-volume
              volumes:
              - name: source-data-volume
                persistentVolumeClaim:
                  claimName: backup-storage-pv-claim
      schedule: 30 2 * * *
      successfulJobsHistoryLimit: 3
    ---
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: rsync-backup-base-env-config
      labels:
        app: rsync-backup
    data:
      PRIVATE_KEY: |
        -----BEGIN RSA PRIVATE KEY-----
        Your SSH Private Key
        -----END RSA PRIVATE KEY-----
      PUBLIC_KEY: |
        Your SSH Public Key

Note that you don't have to use RSync.net, any host with ssh access will do.