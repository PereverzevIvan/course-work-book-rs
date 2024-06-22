from django.core.management.base import BaseCommand, CommandError
from ...models import Comment


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("comment_id", nargs="+", type=int)

    def handle(self, *args, **options):
        for comment_id in options["comment_id"]:
            try:
                comment = Comment.objects.get(pk=comment_id)
            except Comment.DoesNotExist:
                raise CommandError('Comment "%s" does not exist' % comment_id)

            comment.is_hide = True
            comment.save()

            self.stdout.write(
                self.style.SUCCESS('Successfully hide comment "%s"' % comment_id)
            )


Book.objects.setect_reload
