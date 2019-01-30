#!/usr/bin/python

# This file was created by pchen2145 
# Below are functions that demonstrate scripting using Python and AWS boto3
# The corresponding yaml file is included in this repository

# Import AWS boto3 library and yaml library
import boto3
import yaml

# Create S3 object resource and S3 client
s3 = boto3.resource('s3')
client = boto3.client('s3')

def delete_bucket(bucketname):
	response = client.delete_bucket(Bucket=bucketname)

# Object parameter is a list of objects to upload
def upload_object(bucketname, objects):
	for obj in objects:

		# Replace pathname with the absolute path of your folder containing files to upload
		s3.Object(bucketname, obj).upload_file('/Users/user/projects/python/%s' % obj)

def create_bucket(bucketname):
	bucket = s3.create_bucket(Bucket=bucketname)
	return bucket

# Returns a list of all buckets you own in S3
def list_buckets():
	buckets = [bucket.name for bucket in s3.buckets.all()]
	return buckets

# Returns a list of all objects in an S3 bucket
def list_objects(bucketname):
	bucket = s3.Bucket(bucketname)
	obj_list = [obj.key for obj in bucket.objects.all()]
	return obj_list

# Returns a list of all objects in all S3 buckets
def list_all_objects():
	obj_list_total = []
	for n in list_buckets():
		obj_list_total.append(list_objects(n))
	return sum(obj_list_total, [])

# Uploads objects to appropriate buckets based on yaml config file
def upload_objects_from_file(yamlconfig):

	# Read from yaml file and parse into json
	json_buckets_objects = yaml.load(open(yamlconfig))

	# Create list of bucketnames from json
	buckets = json_buckets_objects['buckets']

	# Iterate through bucketnames list and upload objects
	for bucket in buckets:
		upload_object(bucket['name'], bucket['files'])

# Creates buckets in S3 based on yaml config file
def bucket_compare_create(yamlconfig):

	# Read from yaml file and parse into json
	json_buckets_objects = yaml.load(open(yamlconfig))

	# Get list of all buckets currently in S3
	awsbuckets = list_buckets()

	# Create list of bucketnames from json
	bucket = json_buckets_objects['buckets']
	bucketnames = [a['name'] for a in bucket]

	# Loop through bucketnames in list and compare them to buckets on S3
	for n in bucketnames:
		if n in awsbuckets:
			print("Bucket " + n + " already exists and will not be created")
		else:
			create_bucket(n)

	return list_buckets()

bucket_compare_create('s3config.yml')
upload_objects_from_file('s3config.yml')
