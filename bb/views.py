# coding: utf-8
from __future__ import unicode_literals
import json
import operator
import datetime

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden

from accounts.models import ForumProfile
from .models import Forum, Topic, Post, Category
from .forms import ImageUploadForm, TopicUEditorForm, PostReplyForm


today = datetime.date.today()
today_tc = Topic.objects.filter(created__day=today.day).count()
yesterday_tc = Topic.objects.filter(created__day=today.day - 1).count()
categories = Category.objects.all()
forums = Forum.objects.all()
forum = Forum()
users_count = ForumProfile.objects.count()
posts_count = Post.objects.count()


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
    last_topics_list = Topic.objects.all().filter(deleted=False).order_by('-last_replied_time')[0:30]
    post_list_name = 'last topics'
    ctx = {'last_replied_topics': last_topics_list, 'post_name': post_list_name, 'Forums': forums,
           'users_count': users_count, 'today_topics_count': today_tc, 'yesterday_topics_count': yesterday_tc,
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


def category_details(request, category_id):
    category = Category.objects.get(id=category_id)
    ctx = {
        'category_single': category, 'today_topics_count': today_tc, 'yesterday_topics_count': yesterday_tc,
    }
    return render(request, 'widget/categories.html',ctx)


def category_all(request):
    c_forum = [c for c in categories]
    ctx = {
        'categories': categories, 'forums': forums, 'cf': c_forum,
    }
    return render(request, 'bb/category_all.html', ctx)


def forum_view(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    topics = Topic.objects.filter(forum=forum, deleted=False)
    ctx = {
        'topics': topics,
        'forum': forum,
    }
    return render(request, 'bb/forum_view.html', ctx)


def forum_list(request):
    forums = Forum.objects.all()            # 所有存在的分区都列出
    return render(request, 'bb/forum_all.html', {'forums': forums})


def forum_topics(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    topics = forum.topic_set.all()           # 列出当前单个分区下属的帖子，而不是所有分区的全部帖子
    ctx = {'forum': forum,
           'topics': topics
           }
    return render(request, 'widget/forum_topic_list.html', ctx)


def forums_topics(request):
    forums = Forum.objects.all()          # 所有分区的所有帖子
    return render(request, 'bb/forums_topic_all.html', {'forums': forums})


def topic_view(request, topic_id):
    """ view single topic """
    form = PostReplyForm()
    topic = Topic.objects.get(id=topic_id)
    topic.view_count += 1
    topic.save()
    t_forum = topic.forum
    posts = topic.post_set.filter(deleted=False)
    ctx = {'topic': topic,
           't_forum': t_forum,
           'form': form,
           'posts': posts
           }
    return render(request, 'bb/topic.html', ctx)


def create_topic_reply(request, topic_id):
    if request.method == 'POST':
        topic = Topic.objects.get(id=topic_id)
        reply = Post()
        # 回帖所属的那个帖子
        reply.topic = topic
        reply.content = request.POST['Content']
        reply.user = request.user
        reply.save()
        # 帖自被回复的时间就等于reply的创建时间
        topic.last_replied_time = reply.time_created
        topic.save()
        # 当前论坛的回帖总数
        forum.post_count += 1
        forum.save()
        return HttpResponseRedirect(reverse('bb:topic_view', kwargs={'topic_id': topic_id}))
    elif request.method == 'GET':
        return render(request, 'bb/topic.html')


@staff_member_required
def delete_topic_reply(request, post_id):
    post = Post.objects.get(id=post_id)
    # 被回帖的那个主题的id
    t_id = post.topic.id
    post.deleted = True
    post.save()
    post.topic.save()
    return HttpResponseRedirect(reverse('bb:topic_view', kwargs={'topic_id': t_id}))


def pre_create_topic(request):
    cf_list = []
    categories = Category.objects.all()
    form = TopicUEditorForm()
    for c in categories:
        for ca in c.forum_set.all():
            cf_list.append(str(ca))
    ctx = {
        'categories': categories,
        'cf_list': cf_list,
        'form': form
    }

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:sign_in',))
    return render(request, 'bb/pre_topic.html', ctx)


def create_topic(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    msg = []
    if request.method == 'GET':
        form = TopicUEditorForm(initial={'content': u'测试'})
        ctx = {'forum': forum, 'title': 'create_new_topic', 'form': form}
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('bb:sign_in'))
        return render(request, 'bb/create_topic.html', ctx)
    elif request.method == 'POST':
        topic = Topic()
        form = TopicUEditorForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['Content']
            print content
            name = form.cleaned_data['Name']
            user = request.user
            topic.content = content
            topic.title = name
            topic.forum = forum
            topic.author = user
            topic.save()
            forum.topic_count += 1
            forum.save()
        if not topic.title:
            msg.append('title cannot be empty')
            return render(request, 'bb/create_topic.html', {'msg': msg})
        if not request.user.is_authenticated():
            return site_error(request, 'please login', reverse('sign_in'))
        return HttpResponseRedirect(reverse('bb:forum_topic_all', kwargs={'forum_id': forum_id}))


def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.user != topic.author and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('bb:topic_view', kwargs={'topic_id': topic.id}))
    t_forum_id = topic.forum.id
    topic.deleted = True
    topic.save()
    return HttpResponseRedirect(reverse('bb:Forum_view', kwargs={'Forum_id': t_forum_id}))


def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.user != topic.author and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('bb:topic_view', kwargs={'topic_id': topic.id}))
    if request.method == 'GET':
        return render(request, 'bb/edit_topic.html', {'topic': topic})
    elif request.method == 'POST':
        topic.title = request.POST['title']
        topic.content = request.POST['content']
        if not topic.title:
            return render(request, 'bb/edit_topic.html', {'error': 'title cannot be empty'}, )
        topic.save()
        return HttpResponseRedirect(reverse('bb:topic_view', kwargs={'topic_id': topic.id}))


def add_appendix(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    t_n = Topic.Forum
    if request.user != topic.user:
        return render(request, 'bb/appendix.html', {'error': 'you cannot add appendix to others'})
    if request.method == 'GET':
        return render(request, 'bb/appendix.html', {'Forum': t_n, 'topic': topic})
    elif request.method == 'POST':
        appendix = Appendix()
        appendix.content = request.POST['content']
        if not appendix.content:
            return render(request, 'bb/appendix.html', {'error': 'content cannot be empty'})
        appendix.topic = topic
        appendix.save()
        return HttpResponseRedirect(reverse('bb:topic_view', kwargs={'topic_id': topic.id}))


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
    return render(request, 'bb/index.html', ctx)


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
    return render(request, 'bb/index.html', ctx)