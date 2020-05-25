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
excerpt: ... and upload them to Backblaze B2

---

# Setting Up Automatic Daily Database Backup on Kubernetes

Kubernetes has been supporting [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) for a while now, so it's a no brainer to deploy a database app in a Kubernetes cluster. Statefulset allows your pods to maintain sticky, persistent IDs, as well as persistent storage, making it ideal for database apps. Still, even with persistent storage, you should always configure automatic offsite backup when deploying a database app on a Kubernetes cluster. This would ensure your data survives any disaster that might befall your new shiny cluster.

Automatic offsite backups can be a hassle, but it doesn't have to be. In this post, I'm going to setup an automatic daily backup on a MySQL pod into a Backblaze B2 bucket.

## Step 1: Automatically Dump All Databases into a Persistent Volume

I want to dump all databases inside a MySQL pod into a persistent volume. Each database will be dumped into a separate file (so I can load them individually as needed later) on a persistent volume which will be uploaded into a Backblaze B2 bucket later. I'll use Kubernetes' new [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) workload to schedule a daily database dump job.

It's quite annoying to set this up over and over again, so I packed a small MySQL backup script into a container (`arifwn/container-backup:mysql`) suitable for use inside a Kubernetes' CronJob workload. This docker image can be used to backup a specific database or all databases. The source code is availabe on my github repo here: [https://github.com/arifwn/container-backup](https://github.com/arifwn/container-backup).

	#!yaml
    apiVersion: batch/v1beta1
    kind: CronJob
    metadata:
        name: backup-all-mysql80-db
        namespace: backups
    spec:
        concurrencyPolicy: Allow
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
                            image: arifwn/container-backup:mysql
                            imagePullPolicy: Always
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

This will create a new CronJob workload entry on the Kubernetes cluster that run every 2:00 AM everyday. I also mounted a persistent volume (created beforehand) that will be used to store the resulting .sql dumps. We'll mount this volume in another CronJob entry to upload the content to Backblaze B2 later.

## Step 2: Upload to a Backblaze B2 Bucket

Next is uploading the .sql files generated from the last step into a Backblaze B2 bucket. [Backblaze B2](https://www.backblaze.com/b2/cloud-storage.html) is a (very) cheap cloud storage service (about $0.005/GB/Mo) from Backblaze with free ingress bandwidth cost, perfect for storing large backup data offsite. Egress is also cheap (about $0.01/GB) and very fast, unlike some other cheap cloud backup solution (e.g. AWS Glacier).

I also packed my trusty B2 backup script into a docker image (`arifwn/container-backup:b2`). This image will compress each top-level folder in the mounted volume into a .tar.gz archive and upload it into the specified B2 bucket. The image will also perform daily cleanup on the target bucket so only the last 7 daily backups, the last 8 weekly backups, and the last 12 monthly backups retained. The source code is availabe on my github repo here: [https://github.com/arifwn/container-backup](https://github.com/arifwn/container-backup).

    #!yaml
    apiVersion: batch/v1beta1
    kind: CronJob
    metadata:
        name: backblaze-backup
        namespace: backups
    spec:
        concurrencyPolicy: Allow
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
                            imagePullPolicy: Always
                            name: backblaze-backup
                            resources:
                                limits:
                                    cpu: "1" # don't use too much cpu to avoid starving the node
                            volumeMounts:
                            - mountPath: /source
                                name: source-data-volume
                        dnsPolicy: ClusterFirst
                        volumes:
                        - name: source-data-volume
                            persistentVolumeClaim:
                                claimName: backup-storage-pv-claim
        schedule: 30 2 * * *
        successfulJobsHistoryLimit: 3

This will create a new CronJob workload entry on the Kubernetes cluster that run every 2:30 AM everyday (plenty of time for the database dump cron to complete). The cron will compress all data found inside the mounted volume (each top-level folder will be compressed into a separate .tar.gz archive), upload them into a B2 bucket, and remove any old backup archives except the last 7 daily backups, the last 8 weekly backups, and the last 12 monthly backups.

And that's it! The database is now backed up automatically every night to a B2 bucket. It only take minutes to setup and you can sleep soundly at night knowing your data is safe from random cluster failure. Don't forget to setup CronJob failure alert so you'll get notified when uploads failed (the B2 backup image will return with non-zero exit code on failure).
