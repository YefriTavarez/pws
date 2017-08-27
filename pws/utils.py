# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

import frappe
import hashlib

def s_hash(string):
	h = hashlib.sha1(string)

	return h.hexdigest()
