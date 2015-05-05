# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.template import RequestContext
from bb.models import Category, Forum, Topic
from django.shortcuts import render_to_response, render
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
import json
from django.db.models import Q


@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('user:sign_in'))
def index(request):
    return render_to_response('bar/index.html', {'title': _('home')})


# @user_passes_test(lambda u: u.is_superuser, )
def user_manage(request):
    ctx = {'title': _('user management')}
    return render(request, 'bar/user_manager.html', ctx)


# @user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('sign_in'))
def user_data(request):
    data = dict()
    data.update({'init_data': []})
    for u in User.objects.all():
        info_list = [u.username, u.email]
        data['init_data'].append(info_list)
        return HttpResponse(json.dumps(data), content_type='application/javascript')


# @user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('sign_in'))
def user_data_serialize(request):
    fields = ['id', 'username', 'email']
    order_dir = request.GET.get('sSortDir_0')
    order_field = int(request.GET.get('iSortCol_0'))
    if order_dir == 'asc':
        order_by = '%s' % fields[order_field]
    else:
        order_by = '-%s' % fields[order_field]
    length = int(request.GET.get('iDisplayLength', 10))
    key = request.GET.get('sSearch')
    start = int(request.GET.get('iDisplayStart', 0))
    if key:
        if key.isdigit():
            condition = Q(email__contains=key) | Q(username__contains=key) | Q(id=key)
        else:
            condition = Q(email__contains=key) | Q(username__contains=key)
        users = User.objects.filter(condition).order_by(order_by)
    else:
        users = User.objects.all().order_by(order_by)
    data = dict()
    data['aaData'] = []
    data['iTotalDisplayRecords'] = len(users)
    users = users[start:start + length]
    data['iTotalRecords'] = User.objects.count()
    for u in users:
        info_list = list()
        info_list[:] = u.id, u.username, u.email
        info_list.append('<a href="%s" class="label label-success">%s</a>' %
                         (reverse_lazy('toolbar:user_edit', kwargs={'uid': u.id}), _('edit'), ))
        data['aaData'].append(info_list)
    return HttpResponse(json.dumps(data), content_type='application/javascript')


# @user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('sign_in'))
def user_edit(request, user_id):
    u = User.objects.get(id=user_id)
    if request.method == 'GET':
        return render(request, 'bar/user_edit.html')
    elif request.method == 'POST':
        data = request.POST
        username = request.POST['username']
        email = data.get('email', False)
        password = data.get('password', False)
        active = 'active' in data
        admin = 'admin' in data
        nickname = data.get('nickname')
        location = data.get('location')
        website = data.get('website')
        avatar_img = 'avatar_img' in data
        u.username = username
        u.email = email
        if password:
            u.set_password(password)
        u.is_active = active
        u.is_superuser = admin
        u.save()
        p = u.profile
        p.nickname = nickname
        p.website = website
        p.location = location
        p.avatar_img = avatar_img
        p.save()
        return HttpResponseRedirect(reverse('panel:user_edit', args=[user_id]))


def category_manage(request):
    return render(request, 'bar/category_manage.html', )


@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('user:sign_in'))
def category_serialize(request):
    fields = ['id', 'title']
    order_dir = request.GET.get('sSortDir_0')
    order_field = int(request.GET.get('iSortCol_0'))
    if order_dir == 'asc':
        order_by = '%s' % fields[order_field]
    else:
        order_by = '-%s' % fields[order_field]
    length = int(request.GET.get('iDisplayLength', 10))
    key = request.GET.get('sSearch')
    start = int(request.GET.get('iDisplayStart', 0))
    if key:
        if key.isdigit():
            condition = Q(title__contains=key) | Q(id=key)
        else:
            condition = Q(title__contains=key)
        categories = Category.objects.filter(condition).order_by(order_by)
    else:
        categories = Category.objects.all().order_by(order_by)
    data = {}
    data['aaData'] = []
    data['iTotalDisplayRecords'] = len(categories)
    categories = categories[start:start + length]
    data['iTotalRecords'] = Category.objects.count()
    for c in categories:
        info_list = [c.id, c.title,]
        info_list.append('<a href="%s" class="label label-success">%s</a>' %
                         (
                             reverse('toolbar:category_edit', kwargs={'category_id': c.id}),
                             _('edit')
                         )
                         )
        data['aaData'].append(info_list)
    return HttpResponse(json.dumps(data), content_type='application/javascript')


def category_edit(request, category_id):
    category = Category.objects.get(id=category_id)
    forums = Forum.objects.all()
    ctx = {'category': category, 'forums': forums}
    if request.method == 'GET':
        return render(request, 'bar/category_edit.html', ctx)
    elif request.method == 'POST':
        title = request.POST.get('title', 'empty')
        description = request.POST.get('description', None)
        forum = request.POST['forum']
        category.title = title
        category.description = description
        category.forum = forum
        category.save()
        return HttpResponseRedirect(reverse('toolbar:category_edit', args=[category.id]))


def category_create(request):
    if request.method == 'GET':
        ctx = {'title': _('create category')}
        return render(request, 'bar/category_create.html', ctx)
    elif request.method == 'POST':
        category = Category()
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        category.title = title
        category.description = description
        category.save()
        return HttpResponseRedirect(reverse('toolbar:category_create'))


# @user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('user:sign_in'))
def forum_manage(request):
    return render_to_response('bar/forum_manage.html', {'title': _('forum management')})


@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('user:sign_in'))
def forum_serialize(request):
    fields = ['id', 'title']
    order_dir = request.GET.get('sSortDir_0')
    order_field = int(request.GET.get('iSortCol_0'))
    if order_dir == 'asc':
        order_by = '%s' % fields[order_field]
    else:
        order_by = '-%s' % fields[order_field]
    length = int(request.GET.get('iDisplayLength', 10))
    key = request.GET.get('sSearch')
    start = int(request.GET.get('iDisplayStart', 0))
    if key:
        if key.isdigit():
            condition = Q(title__contains=key) | Q(id=key)
        else:
            condition = Q(title__contains=key)
        forums = Forum.objects.filter(condition).order_by(order_by)
    else:
        forums = Forum.objects.all().order_by(order_by)
    data = {}
    data['aaData'] = []
    data['iTotalDisplayRecords'] = len(forums)
    forums = forums[start:start + length]
    data['iTotalRecords'] = Forum.objects.count()
    for f in forums:
        info_list = [f.id, f.title]
        info_list.append('<a href="%s" class="label label-success">%s</a>' %
                         (
                             reverse('toolbar:forum_edit', kwargs={'forum_id': f.id}),
                             _('edit')
                         )
                         )
        data['aaData'].append(info_list)
    return HttpResponse(json.dumps(data), content_type='application/javascript')


@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('user:sign_in'))
def forum_edit(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    if request.method == 'GET':
        ctx = {
            'title': _('edit forum'), 'forum': forum,
        }
        return render(request, 'bar/forum_edit.html', ctx)
    elif request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        forum.title = title
        forum.description = description
        forum.save()
        return HttpResponseRedirect(reverse('toolbar:forum_edit', args=[forum.id]))


@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('user:sign_in'))
def forum_create(request):
    categories = Category.objects.all()
    if request.method == 'GET':
        ctx = {'title': _('create node'),
               'categories': categories,
               }
        return render(request, 'bar/forum_create.html', ctx)
    elif request.method == 'POST':
        form = Forum()
        title = request.POST['title']
        description = request.POST['description']
        form_category = request.POST['category']
        forum_category = Category.objects.get(title=form_category)
        form.title = title
        form.description = description
        form.category = forum_category
        form.save()
        return HttpResponseRedirect(reverse_lazy('toolbar:forum_manage'))


@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('sign_in'))
def topic_manage(request):
    ctx = {'title', _('topic management')}
    return render(request, 'bar/topic_manage.html', ctx)


@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('sign_in'))
def topic_edit(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    ctx = {'title': _('edit topic')}
    if request.method == 'GET':
        return render(request, 'bar/topic_edit.html', ctx)
    elif request.method == 'POST':
        title = request.POST['title']
        node_title = request.POST['node']
        content = request.POST['content']
        order = request.POST['order']
        node = Forum.objects.get(title=node_title)
        topic.title = title
        topic.node = node
        topic.content = content
        topic.order = order
        topic.save()
        return HttpResponseRedirect(reverse('toolbar:topic_edit', args=[topic.id]))


# @user_passes_test(lambda u: u.is_superuser, login_url=reverse('sign_in'))
def topic_table_ss(request):
    fields = ['id', 'title', 'user__username', 'node__title']
    order_dir = request.GET.get('sSortDir_0')
    order_field = int(request.GET.get('iSortCol_0'))
    if order_dir == 'asc':
        order_by = '%s' % fields[order_field]
    else:
        order_by = '-%s' % fields[order_field]
    length = int(request.GET.get('iDisplayLength', 10))
    key = request.GET.get('sSearch')
    start = int(request.GET.get('iDisplayStart', 0))
    if key:
        if key.isdigit():
            condition = Q(title__contains=key) | Q(node__title__contains=key) | Q(user__username__contains=key) | Q(id=key)
        else:
            condition = Q(title__contains=key) | Q(node__title__contains=key) | Q(user__username__contains=key)
        topics = Topic.objects.filter(condition, deleted=False).order_by(order_by)
    else:
        topics = Topic.objects.filter(deleted=False).order_by(order_by)
    data = dict()
    data['aaData'] = []
    data['iTotalDisplayRecords'] = len(topics)
    topics = topics[start:start + length]
    data['iTotalRecords'] = Topic.objects.count()
    for t in topics:
        info_list = list()
        info_list[:] = t.id, t.title, t.user.username, t.node.title
        info_list.append('<a href="%s" class="label label-success">%s</a>' %
                         (reverse('panel:topic_edit', kwargs={'topic_id': t.id}),
                          _('edit')))
        data['aaData'].append(info_list)
    return HttpResponse(json.dumps(data))