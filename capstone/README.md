# DRAFT: Building a Flexible Machine Learning Data Pipeline for CORD-19 Processing

# Statement of Purpose

The intention of this project is to provide a fertile ground for experimentation with creating machine learning data pipelines.

This project will be an opportunity to achieve the following:

- Get exposure to as many frameworks, libraries and methodologies as possible
- How to create a complete end to end and production worthy machine learning data pipeline
- How to allow built-in flexibility to changing most of the components of a machine learning data pipeline
- How to allow for a growing real-life, dynamic and live dataset
- How to build a complete ML data pipeline in the cloud (AWS), focusing mostly on the business problem and taking full advantage of as many services as possible while keeping at the minimum the creation of custom components
- Follow the well architected framework: operational excellence, security, reliability, performance and cost optimization

# The Dataset

The project uses CORD-19 The COVID-19 Open Research Dataset. CORD-19 is a growing resource of scientific papers on COVID-19 and related historical coronavirus research.

A comprehensive description of the corpus can be found at CORD-19: [The COVID-19 Open Research Dataset](https://www.aclweb.org/anthology/2020.nlpcovid19-acl.1.pdf).

AWS provides a [COVID-19 public data lake](https://aws.amazon.com/blogs/big-data/a-public-data-lake-for-analysis-of-covid-19-data/). This data lake contains CORD-19 comprehensive metadata.

AWS provides an [S3 bucket](https://registry.opendata.aws/cord-19/) containing full-text and metadata dataset of COVID-19 and coronavirus-related research articles optimized for machine readability.

## Corpus Metadata

Given the corpus size (almost 200,000 publications as of June 2021) and also the weekly increments, metadata becomes highly important for data analysis and pre-processing as it offers a deep insight into this vast array of papers without the need to commit a large set of resources.

The metadata can be easily accessible after being mounted to AWS Glue Data Catalog using a [CloudFormation template](https://covid19-lake.s3.us-east-2.amazonaws.com/cfn/CovidLakeStack.template.json) maintained by AWS. The process accessing the metadata in an AWS account is thoroughly [explained](https://aws.amazon.com/blogs/big-data/a-public-data-lake-for-analysis-of-covid-19-data/).

## Corpus Full Text

Amazon Resource Name (ARN)

arn:aws:s3:::ai2-semanticscholar-cord-19

AWS Region

us-west-2

**CLI Access (No AWS account required)**

aws s3 ls s3://ai2-semanticscholar-cord-19/ --no-sign-request