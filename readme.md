# s3ToKibana

This repository contains configurations and scripts to ingest AWS CloudTrail logs from an S3 bucket into Elasticsearch and visualize the data in Kibana.

## Overview

The s3ToKibana project automates the process of collecting AWS CloudTrail logs from an S3 bucket, processing them using Logstash, storing them in Elasticsearch, and creating visualizations in Kibana for easier analysis.

## Prerequisites

Before using this project, make sure you have the following prerequisites installed:

- [Logstash](https://www.elastic.co/logstash/)
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [Kibana](https://www.elastic.co/kibana/)
- [AWS CLI](https://aws.amazon.com/cli/)
- [Java](https://www.java.com/)

