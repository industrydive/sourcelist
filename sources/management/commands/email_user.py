from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from sources.models import Person
from sourcelist.settings import PROJECT_NAME, EMAIL_SENDER, SITE_URL


def email_user(email_address, status):
    person = Person.objects.get(email_address=email_address)
    person_id = person.id
    person_url = SITE_URL + '/admin/sources/person/{}/change/'.format(person_id) ## use url reverse instead?
    person_info = 'this is where the info will go' ## UPDATE

    confirm_url = 'confirm url here' ## UPDATE

    status = person.status
    status_type = status.split('_')[0]
    
    if status_type == 'added':
        subject_title = 'You have been added as a source by '
        if status == 'added_by_self':
            subject_title += 'yourself'
        elif status == 'added_by_other':
            subject_title += 'someone else'
        elif status == 'added_by_admin':
            subject_title += 'an admin'

        subject = '[{}] {}'.format(PROJECT_NAME, subject_title)
        message = ''
        html_message = 'To confirm you would like be included in the {project_name} database and to confirm the following information is correct, please click here: <br><br> {confirm_url} <br><br> \
            {person_info} <br><br> \
            If the information if incorrect, please edit your entry: <br><br> {person_url} <br><br>View the database:<br><br> {site_url}\
            '.format(
                project_name=PROJECT_NAME,
                confirm_url=confirm_url,
                person_info=person_info,
                person_url=person_url,
                site_url=SITE_URL
            )
    sender = EMAIL_SENDER
    recipients = [email_address]
    # reply_email = sender

    send_mail(
        subject,
        message,
        sender,
        recipients,
        # reply_to=[reply_email],
        html_message=html_message,
        fail_silently=False,
    )


class Command(BaseCommand):
    help = 'Email new user when added.'

    def add_arguments(self, parser):
        ## required
        parser.add_argument('email', 
            help='Specify the user email.'
        )

        parser.add_argument('status',
            help='Specify the status.'
        )

        ## optional
        # parser.add_argument('-t' '--test',
        #     action='store_true',
        #     # type=str,
        #     dest='test',
        #     default=False,
        #     help="Specific whether it's a test or not"
        # )

    def handle(self, *args, **options):
        ## unpack args
        email_address = options['email']
        status = options['status']

        ## call the function
        email_user(email_address, status)
