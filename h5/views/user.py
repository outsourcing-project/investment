# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.template import loader
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from web.models import (
    Advertising,
    Profile,
    Infrastructure,
    HousingResources,
    Infrastructure,
    HousingCertificatePicture,
    HousingPicture,
    HousingResourcesOrder,
    Setting,
    Bedroom,
)

from pingPay.pay import create_ping_order
from imagestore.qiniu_manager import(
    get_extension,
    handle_uploaded_file,
    upload,
    url
)

from utils import(
    send_v_code, check_v_code, md5_create,
    jwt_token_gen, jwt_token_decode, website_check_login,
    generate_order_num
)

from settings import (
    DB_PREFIX,
    DOMAIN,
    QINIU_DOMAIN,
    UPLOAD_DIR,
)

import os
import datetime
import time
import random
import string
import redis
import logging


@csrf_exempt
@website_check_login
def index(request):
	c_user = request.session.get('c_user', None)
	profile = Profile.objects.filter(is_del=False, pk=c_user['id']).first()
	infrastructures = Infrastructure.objects.filter(
		is_del=False,
		is_valid=True
	).order_by('-order_no')

	if request.method == 'POST':
		c_user_id = request.POST.get('c_user_id', '')
		user_name = request.POST.get('user_name', '')
		gender = request.POST.get('gender', '')
		birbath = request.POST.get('birbath', '')
		mobile = request.POST.get('mobile', '')
		# bank_acount = request.POST.get('bank_acount', '')
		id_card = request.POST.get('id_card', '')
		promo_code = request.POST.get('promo_code', '')
		employe = request.POST.get('employe', '')

		# try:
		profile.user_name = user_name
		if gender:
			profile.gender = gender
		birbath = datetime.datetime.strptime(birbath, "%Y-%m-%d")
		profile.birbath = birbath
		profile.mobile = mobile
		# profile.bank_acount = bank_acount
		profile.promo_code = promo_code
		profile.employe = employe
		profile.id_card = id_card

		if request.FILES:
			if request.FILES.get('test-image-file', None):
				# 上传图片
				id_card_picture = request.FILES['test-image-file']
				ts = int(time.time())
				ext = get_extension(id_card_picture.name)
				key = 'id_card_picture_{}.{}'.format(ts, ext)
				handle_uploaded_file(id_card_picture, key)
				upload(key, os.path.join(UPLOAD_DIR, key))
				profile.id_card_picture = key

		profile.save()

	context = {
		'module': 'index',
		'sub_module': 'user_index',
		'client': profile,
		'infrastructures': infrastructures,
		'qiniu_domain': QINIU_DOMAIN,
	}

	return render(request, 'frontend/user/05-4-member01.html', context)


@csrf_exempt
@website_check_login
def housing_resource_create(request):
	c_user = request.session.get('c_user', None)
	profile = Profile.objects.filter(is_del=False, pk=c_user['id']).first()
	infrastructures = Infrastructure.objects.filter(
		is_del=False,
		is_valid=True
	).order_by('-order_no')

	if request.method == 'POST':
		content = request.POST.get('content', '')
		lease = request.POST.get('lease', 0)
		category = request.POST.get('category', '')
		province = request.POST.get('province', '')
		city = request.POST.get('city', '')
		area = request.POST.get('area', '')
		bet = request.POST.get('bet', 0)
		month_rent = request.POST.get('month_rent', 0)
		pay = request.POST.get('pay', 0)
		direction = request.POST.get('direction', 0)
		layer = request.POST.get('layer', 0)
		total_layer = request.POST.get('total_layer', 0)
		community = request.POST.get('community', '')
		address = request.POST.get('address', '')
		infrastructures = request.POST.getlist('infrastructures', '')
		bus = request.POST.get('bus', '')
		subway = request.POST.get('subway', '')
		buy = request.POST.get('buy', '')
		sitting_room = request.POST.get('sitting_room', '')
		sitting_room_area = request.POST.get('sitting_room_area', '')
		sitting_room_complete = request.POST.getlist('sitting_room_complete', '')
		imgs1 = request.POST.getlist('imgs1', '')
		imgs2 = request.POST.getlist('imgs2', '')
		bedroom_count = request.POST.get('bedroom_count', 0)

		# try:
		# 保存房源信息
		with transaction.atomic():
			housing_resources = HousingResources()
			housing_resources.user = profile.get_user()
			housing_resources.content = content
			housing_resources.lease = lease
			housing_resources.category = category
			housing_resources.province = province
			housing_resources.bet = bet
			housing_resources.pay = pay
			housing_resources.direction = direction
			housing_resources.layer = layer
			housing_resources.total_layer = total_layer
			housing_resources.community = community
			housing_resources.address = address
			housing_resources.bus = bus
			housing_resources.subway = subway
			housing_resources.buy = buy
			housing_resources.audit_status = 0
			housing_resources.sitting_room_area = float(sitting_room_area) if sitting_room_area else 0
			housing_resources.save()
			# 获取基础设施
			infrastructure_list = Infrastructure.objects.filter(pk__in=infrastructures).all()
			housing_resources.infrastructure = infrastructure_list

			if not sitting_room:
				housing_resources.sitting_room = 1

			if type(sitting_room_complete) == list:
				housing_resources.sitting_room_complete = ','.join(sitting_room_complete)

			housing_resources.save()

			if type(imgs1) == list:
				for i in imgs1:
					HousingCertificatePicture.objects.create(
						housing_resources=housing_resources,
						picture=i,
					)

			if type(imgs2) == list:
				for i in imgs2:
					HousingPicture.objects.create(
						housing_resources=housing_resources,
						picture=i,
					)

			# 存储卧室信息
			for i in range(1,int(bedroom_count)):
				areai = request.POST.get('area' + str(i) , 0)
				detailsi = request.POST.getlist('details' + str(i), 0)
				Bedroom.objects.create(
					housing_resources=housing_resources,
					area=areai,
					complete=','.join(detailsi),
				)

				# 获取支付的金额
				# setting = Setting.objects.filter(
				# 	is_del=False,
				# 	is_valid=True,
				# 	code='housing_resources_pay'
				# ).first()
				# # 创建订单
				# hro = HousingResourcesOrder.objects.create(
				# 	user=profile.get_user(),
				# 	order_num=generate_order_num(),
				# 	total_fee=setting.value,
				# 	real_fee=setting.value,
				# 	status=1
				# )

				# subject = u'房源发布'
				# channel = 'alipay_pc_direct'
				# if not hro.pay_way:
				# 	channel = 'alipay_pc_direct'

				# client_ip = '127.0.0.1'
				# success_url = DOMAIN + '/hrs'
				# charge_id = create_ping_order(hro.order_num, subject, subject, hro.real_fee, channel, client_ip, success_url=success_url)


		# except Exception as e:
		# 	return JsonResponse({'error_code': 1, 'error_msg': '提交审核失败'})

		return JsonResponse({'error_code': 0, 'error_msg': '提交审核成功'})

	context = {
		'module': 'index',
		'sub_module': 'housing_resource_create',
		'client': profile,
		'infrastructures': infrastructures,
		'qiniu_domain': QINIU_DOMAIN,
	}

	return render(request, 'frontend/user/05-4-member02.html', context)


@website_check_login
def housing_resource_edit(request, housing_resources_id):
	c_user = request.session.get('c_user', None)
	profile = Profile.objects.filter(is_del=False, pk=c_user['id']).first()
	infrastructures = Infrastructure.objects.filter(
		is_del=False,
		is_valid=True
	).order_by('-order_no')
	housing_resources = HousingResources.objects.get(pk=housing_resources_id)
	if request.method == 'POST':
		content = request.POST.get('content', '')
		lease = request.POST.get('lease', 0)
		category = request.POST.get('category', '')
		province = request.POST.get('province', '')
		city = request.POST.get('city', '')
		area = request.POST.get('area', '')
		bet = request.POST.get('bet', 0)
		month_rent = request.POST.get('month_rent', 0)
		pay = request.POST.get('pay', 0)
		direction = request.POST.get('direction', 0)
		layer = request.POST.get('layer', 0)
		total_layer = request.POST.get('total_layer', 0)
		community = request.POST.get('community', '')
		address = request.POST.get('address', '')
		infrastructures = request.POST.getlist('infrastructures', '')
		bus = request.POST.get('bus', '')
		subway = request.POST.get('subway', '')
		buy = request.POST.get('buy', '')
		sitting_room = request.POST.get('sitting_room', '')
		sitting_room_area = request.POST.get('sitting_room_area', '')
		sitting_room_complete = request.POST.getlist('sitting_room_complete', '')
		imgs1 = request.POST.getlist('imgs1', '')
		imgs2 = request.POST.getlist('imgs2', '')
		bedroom_count = request.POST.get('bedroom_count', 0)

		# try:
		# 保存房源信息
		with transaction.atomic():
			housing_resources.user = profile.get_user()
			housing_resources.content = content
			housing_resources.lease = lease
			housing_resources.category = category
			housing_resources.province = province
			housing_resources.bet = bet
			housing_resources.pay = pay
			housing_resources.direction = direction
			housing_resources.layer = layer
			housing_resources.total_layer = total_layer
			housing_resources.community = community
			housing_resources.address = address
			housing_resources.bus = bus
			housing_resources.subway = subway
			housing_resources.buy = buy
			housing_resources.audit_status = 0
			housing_resources.sitting_room_area = float(sitting_room_area) if sitting_room_area else 0
			housing_resources.save()
			# 获取基础设施
			infrastructure_list = Infrastructure.objects.filter(pk__in=infrastructures).all()
			housing_resources.infrastructure = infrastructure_list

			if not sitting_room:
				housing_resources.sitting_room = 1

			if type(sitting_room_complete) == list:
				housing_resources.sitting_room_complete = ','.join(sitting_room_complete)

			housing_resources.save()

			if type(imgs1) == list:
				for i in imgs1:
					HousingCertificatePicture.objects.create(
						housing_resources=housing_resources,
						picture=i,
					)

			if type(imgs2) == list:
				for i in imgs2:
					HousingPicture.objects.create(
						housing_resources=housing_resources,
						picture=i,
					)

			# 存储卧室信息
			for i in range(1,int(bedroom_count)):
				areai = request.POST.get('area' + str(i) , 0)
				detailsi = request.POST.getlist('details' + str(i), 0)
				Bedroom.objects.create(
					housing_resources=housing_resources,
					area=areai,
					complete=','.join(detailsi),
				)

				# 获取支付的金额
				# setting = Setting.objects.filter(
				# 	is_del=False,
				# 	is_valid=True,
				# 	code='housing_resources_pay'
				# ).first()
				# # 创建订单
				# hro = HousingResourcesOrder.objects.create(
				# 	user=profile.get_user(),
				# 	order_num=generate_order_num(),
				# 	total_fee=setting.value,
				# 	real_fee=setting.value,
				# 	status=1
				# )

				# subject = u'房源发布'
				# channel = 'alipay_pc_direct'
				# if not hro.pay_way:
				# 	channel = 'alipay_pc_direct'

				# client_ip = '127.0.0.1'
				# success_url = DOMAIN + '/hrs'
				# charge_id = create_ping_order(hro.order_num, subject, subject, hro.real_fee, channel, client_ip, success_url=success_url)

		return HttpResponseRedirect(reverse('website:housing_resources'))

	context = {
		'module': 'index',
		'sub_module': 'housing_resource_create',
		'client': profile,
		'infrastructures': infrastructures,
		'housing_resources': housing_resources,
		'qiniu_domain': QINIU_DOMAIN,
	}

	return render(request, 'frontend/user/05-4-member02.html', context)



@website_check_login
def housing_resources(request):
	c_user = request.session.get('c_user', None)
	profile = Profile.objects.filter(is_del=False, pk=c_user['id']).first()
	housing_resources = HousingResources.objects.filter(
		is_del=False,
		is_valid=True,
		user=profile.get_user()
	).order_by('-created')

	context = {
		'module': 'index',
		'sub_module': 'housing_resource',
		'client': profile,
		'clients1': housing_resources.filter(audit_status=2, status=2),
		'clients2': housing_resources.filter(audit_status=0, status=0),
		'clients3': housing_resources.filter(audit_status=2, status=0),
		'clients4': housing_resources.filter(audit_status=2, status=1),
		'qiniu_domain': QINIU_DOMAIN,
	}

	return render(request, 'frontend/user/05-4-member03.html', context)


@website_check_login
def login_out(request):
	if request.session.get('c_user', None):
		del request.session['c_user']

	return HttpResponseRedirect(reverse('website:home_index'))


@csrf_exempt
def update_avatar(request):
	c_user_id = request.POST.get('c_user_id', '')
	avatar = request.POST.get('avatar', '')

	try:
		profile = Profile.objects.filter(is_del=False, pk=c_user_id).first()
		profile.avatar = avatar

		profile.save()

	except Exception as e:
		logging.error(e)
		return JsonResponse({
			'error_code': 1,
			'error_msg': '修改失败',
		})

	return JsonResponse({
		'error_code': 0,
		'error_msg': '修改成功',
	})


@csrf_exempt
def update_profile(request):
	c_user_id = request.POST.get('c_user_id', '')
	user_name = request.POST.get('user_name', '')
	gender = request.POST.get('gender', '')
	birbath = request.POST.get('jHsDateInput', '')
	mobile = request.POST.get('mobile', '')
	# bank_acount = request.POST.get('bank_acount', '')
	id_card = request.POST.get('id_card', '')
	promo_code = request.POST.get('promo_code', '')
	employe = request.POST.get('employe', '')

	# try:
	profile = Profile.objects.filter(is_del=False, pk=c_user_id).first()
	profile.user_name = user_name
	profile.gender = gender
	birbath = datetime.datetime.strptime(birbath, "%Y-%m-%d")
	profile.birbath = birbath
	profile.mobile = mobile
	# profile.bank_acount = bank_acount
	profile.promo_code = promo_code
	profile.employe = employe
	profile.id_card = id_card

	if request.FILES:
		if request.FILES.get('test-image-file', None):
			# 上传图片
			id_card_picture = request.FILES['test-image-file']
			ts = int(time.time())
			ext = get_extension(id_card_picture.name)
			key = 'id_card_picture_{}.{}'.format(ts, ext)
			handle_uploaded_file(id_card_picture, key)
			upload(key, os.path.join(UPLOAD_DIR, key))
			profile.id_card_picture = key

	profile.save()

	# except Exception as e:
	# 	logging.error(e)
	# 	return JsonResponse({
	# 		'error_code': 1,
	# 		'error_msg': '保存失败',
	# 	})

	return JsonResponse({
		'error_code': 0,
		'error_msg': '保存成功',
	})

