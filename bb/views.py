# coding: utf-8
from __future__ import unicode_literals
from django.shortcuts import render
# from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.admin.utils import NestedObjects
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from accounts.models import ForumProfile
from .models import Forum, Topic, Post, Category, Appendix
from .forms import ImageUploadForm
import json
import operator


def site_error(request, msg, back=None):
    ctx = {
        'title': 'notice',
        'msg': msg,
        'back': back
    }
    return render(request, 'common/error.html', ctx)


def preview(request):
    if request.method == 'POST' and request.is_ajax():
        content = request.POST.get('content', '')
        md = {}
        md['marked'] = content
        return HttpResponse(json.dumps(md))


def index(request):
    categories = Category.objects.all()
    forums = Forum.objects.all()
    users_count = ForumProfile.objects.count()
    topics_count = Topic.objects.count()
    posts_count = Post.objects.count()

    last_topics_list = Topic.objects.all().filter(deleted=False).order_by('-last_replied_time')[0:30]
    post_list_name = 'last topics'
    ctx = {'last_replied_topics': last_topics_list, 'post_name': post_list_name, 'Forums': forums,
           'users_count': users_count, 'topics_count': topics_count,
           'categories': categories, 'posts_count': posts_count,
           }
    return render(request, 'common/index.html', ctx)


def upload_pic(request, pk):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Forum.objects.get(pk=pk)
            m.avatar = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')


def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'widget/categories.html', {'category_single': category})


def category_all(request):
    categories = Category.objects.all()
    forums = Forum.objects.all()
    c_forum = [c for c in categories]
    ctx = {'categories': categories, 'forums': forums, 'cf': c_forum}
    return render(request, 'bbs/category_all.html', ctx)


def forum_view(request, forum_id):
    try:
        page = request.GET['page']
    except ValueError:
        page = None
    if page == '1':
        page = None
    forum = Forum.objects.get(id=forum_id)
    topics = Topic.objects.filter(forum=forum, deleted=False)
    ctx = {
        'topics': topics,
        'Forum': Forum,
        'Forum_view': True,
        'page': page
    }
    return render(request, 'bbs/forum_view.html', ctx)


def forum_list(request):
    forums = Forum.objects.all()            # 所有存在的分区都列出
    return render(request, 'bbs/forum_all.html', {'forums': forums})


def forum_topics(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    topics = Forum.topic_set.all()           # 列出当前单个分区下属的帖子，而不是所有分区的全部帖子
    ctx = {'Forum': forum,
           'topics': topics
           }
    return render(request, 'widget/forum_topic_list.html', ctx)


def forums_topics(request):
    f_topics = Forum.objects.all()          # 所有分区的所有帖子
    return render(request, 'bbs/forums_topic_all.html', {'f_topics': f_topics})


def topic_view(request, topic_id):
    """ view single topic """
    topic = Topic.objects.get(id=topic_id)
    topic.view_count += 1
    topic.save()
    t_forum = topic.forum
    posts = topic.post_set.filter(deleted=False)
    try:
        page = request.GET['page']
    except ValueError:
        page = None
    if page == '1':
        page = None
    ctx = {'topic': topic,
           't_Forum': t_forum,
           'page': page,
           'posts': posts
           }
    return render(request, 'bbs/topic.html', ctx)


def create_topic_reply(request, topic_id):
    msg = []
    if request.method == 'POST':
        topic = Topic.objects.get(id=topic_id)
        reply = Post()
        # 回帖所属的那个帖子
        reply.topic = topic
        if request.POST['content']:
            reply.content = request.POST['content']
        else:
            msg.append('content cannot be empty')
            return render(request, 'bbs/topic.html', {'msg': msg})
        reply.user = request.user
        reply.save()
        return HttpResponseRedirect(reverse('topic_view_count', kwargs={'topic_id': topic_id}))
    elif request.method == 'GET':
        msg.append('did not get stuff')
        return render(request, 'bbs/topic.html', {'msg': msg})


@staff_member_required
def delete_topic_reply(request, post_id):
    post = Post.objects.get(id=post_id)
    # 被回帖的那个主题的id
    t_id = post.topic.id
    post.deleted = True
    post.save()
    post.topic.save()
    return HttpResponseRedirect(reverse('bbs:topic_view', kwargs={'topic_id': t_id}))


def pre_create_topic(request):
    cf_list = []
    categories = Category.objects.all()
    for c in categories:
        for ca in c.forum_set.all():
            cf_list.append(str(ca))
    ctx = {
        'categories': categories,
        'cf_list': cf_list,
    }
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:sign_in',))
    return render(request, 'bbs/pre_topic.html', ctx)


def create_topic(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    msg = []
    if request.method == 'GET':
        ctx = {'Forum': forum,'title': 'create_new_topic'}
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('sign_in'))
        return render(request, 'bbs/create_topic.html', ctx)
    elif request.method == 'POST':
        topic = Topic()
        topic.content = request.POST.get('content')
        topic.forum = forum
        topic.title = request.POST['title']
        if not topic.title:
            msg.append('title cannot be empty')
            return render(request, 'bbs/create_topic.html', {'msg': msg})
        if not request.user.is_authenticated():
            return site_error(request, 'please login', reverse('sign_in'))
        return HttpResponseRedirect(reverse('bbs:list_topics', kwargs={'Forum_id': forum_id}))


def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.user != topic.author and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('bbs:topic_view', kwargs={'topic_id': topic.id}))
    t_forum_id = topic.forum.id
    topic.deleted = True
    topic.save()
    return HttpResponseRedirect(reverse('bbs:Forum_view', kwargs={'Forum_id': t_forum_id}))


def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.user != topic.author and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('bbs:topic_view', kwargs={'topic_id': topic.id}))
    if request.method == 'GET':
        return render(request, 'bbs/edit_topic.html', {'topic': topic})
    elif request.method == 'POST':
        topic.title = request.POST['title']
        topic.content = request.POST['content']
        if not topic.title:
            return render(request, 'bbs/edit_topic.html', {'error': 'title cannot be empty'}, )
        topic.save()
        return HttpResponseRedirect(reverse('bbs:topic_view', kwargs={'topic_id': topic.id}))


def add_appendix(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    t_n = Topic.Forum
    if request.user != topic.user:
        return render(request, 'bbs/appendix.html', {'error': 'you cannot add appendix to others'})
    if request.method == 'GET':
        return render(request, 'bbs/appendix.html', {'Forum': t_n, 'topic': topic})
    elif request.method == 'POST':
        appendix = Appendix()
        appendix.content = request.POST['content']
        if not appendix.content:
            return render(request, 'bbs/appendix.html', {'error': 'content cannot be empty'})
        appendix.topic = topic
        appendix.save()
        return HttpResponseRedirect(reverse('bbs:topic_view', kwargs={'topic_id': topic.id}))


def search(request, kw):
    k = kw.split(' ')
    condition = reduce(operator.and_, [Q(title__contains=x) for x in k])
    topics = Topic.objects.filter(condition)
    try:
        page = request.GET['page']
    except ValueError:
        page = None
    if page == '1':
        page = None
    ctx = {
        'title': '%s-search result' % k,
        'page': page,
        'topics': topics,
        'post_list_title': 'search %s' % k
    }
    return render(request, 'bbs/index.html', ctx)


def recent(request):
    try:
        page = request.GET['page']
    except ValueError:
        page = None
    if page == '1':
        page = None
    topics = Topic.objects.all().filter(deleted=False)
    ctx = {
        'topics': topics,
        'pager': page,
    }
    return render(request, 'bbs/index.html', ctx)