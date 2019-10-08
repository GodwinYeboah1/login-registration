from __future__ import unicode_literals
import re

import bcrypt
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-._]+@[a-zA-Z0-9+-._]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
	def register(self,first_name,last_name,email,password,conf_password):
		response={
			'valid':True,
			'errors':[],
			'user':None
		}

		#for first name
		if len(first_name)<1:
			response['errors'].append('First name is required')
		elif len(first_name)<2:
			response['errors'].append(' First Name must be greater than 2 characters or more')
			#for last name
		if len(last_name)<1:
			response['errors'].append('Last name is required')
		elif len(last_name)<2:
			response['errors'].append(' Last Name must be greater than 2 characters or more')
			#for email
		if len(email)<1:
			response['errors'].append('Email is required')
		elif not EMAIL_REGEX.match(email):
			response['errors'].append('Invalid Email')
		else:
			email_list=User.objects.filter(email=email.lower())
			if len (email_list)>0:
				response['errors'].append('Email already exist')
		
			#for password
		if len(password)<1:
			response['errors'].append('Password is required')
		elif len(password)<8:
			response['errors'].append(' Password must be greater than 8 characters or more')

			#for conf password
		if len(conf_password)<1:
			response['errors'].append('Please confirm the password')
		if conf_password != password:
			response['errors'].append('Confirm password must match password')

		if len(response['errors'])>0:
			response['valid']=False

		else:
			user=User.objects.create(
				first_name=first_name,
				last_name=last_name,
				email=email.lower(),
				password=bcrypt.hashpw(password.encode(),bcrypt.gensalt())

			)
			response['user']=user

		return response


	def login(self,email,password):

		response={
			'valid':True,
			'errors':[],
			'user':None
		}

		#for email
		if len(email)<1:
			response['errors'].append('Email is required')
		elif not EMAIL_REGEX.match(email):
			response['errors'].append('Email is required')
		else:
			email_list=User.objects.filter(email=email.lower())
			if len (email_list)==0:
				response['errors'].append('Email does not exist')
		#for password
		if len(password)<1:
			response['errors'].append('Password is required')
		elif len(password)<8:
			response['errors'].append(' Password must be greater than 8 characters or more')

		if len(response['errors'])==0:
			hashed_pw = email_list[0].password
			if bcrypt.checkpw(password.encode(),hashed_pw.encode()):
				response['user']=email_list[0]
			else:
				response['errors'].append('Incorrect Password')

		if len(response['errors'])>0:
			response['valid']=False

		return response


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


    def __repr__(self):
        return "User object: {} {} {} {}".format(self.first_name, self.last_name,self.email,self.password)

