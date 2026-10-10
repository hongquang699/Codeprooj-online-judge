"""Small, allowlisted terminal for site content and direct messages."""

import shlex
from pathlib import Path

from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from backend.community.models import Conversation, Message, Post
from backend.community.services.notification_service import NotificationService
from backend.judge.models import Profile


HELP = """Commands:
  status                         Show content and chat counts
  posts                          List recent posts
  show-post ID                   Show a post
  edit-post ID title|content FILE  Replace a post field with UTF-8 file contents
  chats                          List your conversations
  read ID                        Read a conversation
  send USERNAME TEXT             Send a direct message
  help                           Show this help
  quit                           Exit interactive mode"""


class Command(BaseCommand):
    help = 'Admin terminal for editing community posts and chatting with users.'

    def add_arguments(self, parser):
        parser.add_argument('--user', required=True, help='Active staff username used for chat')
        parser.add_argument('action', nargs='?', help='Command to run once; omit for interactive mode')
        parser.add_argument('arguments', nargs='*', help='Arguments for the command')

    def handle(self, *args, **options):
        user = get_user_model().objects.filter(username=options['user'], is_active=True, is_staff=True).first()
        if user is None:
            raise CommandError('An active staff user is required.')
        self.profile, _ = Profile.objects.get_or_create(user=user)
        self.user = user
        if options['action']:
            self.run_command([options['action'], *options['arguments']])
            return
        self.stdout.write('Site terminal. Type help for commands.')
        while True:
            try:
                line = input('site> ')
            except (EOFError, KeyboardInterrupt):
                self.stdout.write('')
                break
            try:
                parts = shlex.split(line)
                if parts and parts[0] in ('quit', 'exit'):
                    break
                self.run_command(parts)
            except (CommandError, ValueError) as exc:
                self.stderr.write(str(exc))

    def run_command(self, parts):
        if not parts:
            return
        action, *arguments = parts
        if action == 'help':
            self.stdout.write(HELP)
        elif action == 'status' and not arguments:
            self.stdout.write(f'Posts: {Post.objects.count()} | Chats: {Conversation.objects.count()} | Messages: {Message.objects.count()}')
        elif action == 'posts' and not arguments:
            for post in Post.objects.select_related('author__user').order_by('-created_at')[:20]:
                self.stdout.write(f'{post.pk}\t{post.title}\t{post.author.user.username}')
        elif action == 'show-post' and len(arguments) == 1:
            post = self.get_post(arguments[0])
            self.stdout.write(f'{post.pk}: {post.title}\n{post.content}')
        elif action == 'edit-post' and len(arguments) == 3:
            self.edit_post(*arguments)
        elif action == 'chats' and not arguments:
            chats = Conversation.objects.filter(participant_1=self.profile) | Conversation.objects.filter(participant_2=self.profile)
            for chat in chats.select_related('participant_1__user', 'participant_2__user').order_by('-updated_at')[:20]:
                other = chat.participant_2 if chat.participant_1_id == self.profile.pk else chat.participant_1
                self.stdout.write(f'{chat.pk}\t{other.user.username}\t{chat.updated_at:%Y-%m-%d %H:%M}')
        elif action == 'read' and len(arguments) == 1:
            chat = self.get_chat(arguments[0])
            for message in chat.messages.select_related('sender__user').order_by('-created_at')[:100]:
                self.stdout.write(f'{message.created_at:%Y-%m-%d %H:%M} {message.sender.user.username}: {message.content}')
        elif action == 'send' and len(arguments) >= 2:
            self.send(arguments[0], ' '.join(arguments[1:]))
        else:
            raise CommandError('Invalid command or arguments. Type help for usage.')

    @staticmethod
    def parse_id(value):
        if not value.isdecimal() or int(value) < 1:
            raise CommandError('ID must be a positive integer.')
        return int(value)

    def get_post(self, value):
        post = Post.objects.filter(pk=self.parse_id(value)).first()
        if post is None:
            raise CommandError('Post not found.')
        return post

    def get_chat(self, value):
        chat = Conversation.objects.filter(pk=self.parse_id(value)).first()
        if chat is None or self.profile.pk not in (chat.participant_1_id, chat.participant_2_id):
            raise CommandError('Conversation not found for this user.')
        return chat

    def edit_post(self, value, field, filename):
        if field not in ('title', 'content'):
            raise CommandError('Editable fields: title, content.')
        path = Path(filename)
        try:
            if path.stat().st_size > 1_000_000:
                raise CommandError('File exceeds 1 MB.')
            content = path.read_text(encoding='utf-8').strip()
        except (OSError, UnicodeError) as exc:
            raise CommandError(f'Cannot read UTF-8 file: {exc}') from exc
        if not content or (field == 'title' and len(content) > 255):
            raise CommandError('Field is empty or title exceeds 255 characters.')
        with transaction.atomic():
            post = self.get_post(value)
            setattr(post, field, content)
            post.save(update_fields=[field, 'updated_at'])
            LogEntry.objects.create(
                user=self.user,
                content_type=ContentType.objects.get_for_model(Post),
                object_id=str(post.pk),
                object_repr=str(post)[:200],
                action_flag=CHANGE,
                change_message=f'Site terminal changed {field}',
            )
        self.stdout.write(f'Updated post {post.pk} ({field}).')

    def send(self, username, content):
        content = content.strip()
        if not content or len(content) > 5000:
            raise CommandError('Message must contain 1 to 5000 characters.')
        target = Profile.objects.select_related('user').filter(user__username=username, user__is_active=True).first()
        if target is None or target.pk == self.profile.pk:
            raise CommandError('Recipient not found or is the current user.')
        p1, p2 = sorted((self.profile, target), key=lambda p: p.pk)
        with transaction.atomic():
            chat, _ = Conversation.objects.get_or_create(participant_1=p1, participant_2=p2)
            message = Message.objects.create(conversation=chat, sender=self.profile, content=content)
            chat.updated_at = timezone.now()
            chat.save(update_fields=['updated_at'])
            NotificationService.notify(
                recipient=target, sender=self.profile, ntype='message', title='Tin nhắn mới',
                message=f'{self.profile.user.username}: {content[:60]}',
                link=f'/community/messages/conversation.html?id={chat.pk}',
            )
        self.stdout.write(f'Sent message {message.pk} in conversation {chat.pk}.')
