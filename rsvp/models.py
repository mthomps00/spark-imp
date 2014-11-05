from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import random

class Camp(models.Model):
    theme = models.CharField(max_length=60)
    display_name = models.CharField(max_length=60, blank=True, null=True)
    short_name = models.CharField(max_length=20, blank=True, null=True)
    welcome = models.TextField(blank=True, default='')
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    logistics = models.TextField(blank=True)
    banner_image = models.ImageField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    ticket_cost = models.PositiveIntegerField(blank=True, null=True)

    # Hotel information
    hotel = models.CharField(max_length=60, blank=True)
    hotel_link = models.URLField(blank=True)
    hotel_code = models.CharField(max_length=60, blank=True, verbose_name='Hotel promotion code')
    hotel_deadline = models.DateField(blank=True, null=True)
    
    # Venue information
    venue = models.CharField(max_length=60, blank=True)
    venue_address = models.CharField(max_length=140, blank=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    
    # Event components
    ignite = models.BooleanField(blank=True, default=False)
    stipends = models.BooleanField(blank=True, default=False)
    talk = models.BooleanField(blank=True, default=False)
    paid = models.BooleanField(blank=True, default=False)

    # Google Spreadsheet with invitee information
    spreadsheet_url = models.URLField(blank=True)
    faq_url = models.URLField(blank=True, null=True)
    
    # MailChimp list name
    mailchimp_list = models.CharField(max_length=140, blank=True)
    
    def __unicode__(self):
        return u'Spark Camp %s' % self.theme

class Invitation(models.Model):
    # Field choices
    STATUS_CHOICES = (
        ('Q', 'Invitation not yet sent'),
        ('P', 'Awaiting a response'),
        ('Y', 'Attendance confirmed'),
        ('I', 'Registration incomplete'),
        ('N', 'Can\'t make it'),
        ('C', 'Had to cancel'),
        ('X', 'No response'),
        ('Z', 'No show'),
        ('W', 'On the waitlist'),
        ('M', 'Maybe'),
    )
    ATTENDEE_TYPE = (
        ('G', 'Guest'),
        ('S', 'Sponsor'),
        ('H', 'Host'),
        ('A', 'Administrative Support / Staff'),
    )
    
    # Invitation metadata
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='Q')
    type = models.CharField(max_length=1, choices=ATTENDEE_TYPE, default='G')
    plus_one = models.BooleanField(default=False)
    inviter = models.ForeignKey('self', blank=True, null=True)
    expires = models.DateField(blank=True, null=True)
    custom_message = models.TextField(blank=True, null=True)
    has_paid = models.BooleanField(default=False)
    special_cost = models.IntegerField(blank=True, null=True)
    nominated_by = models.CharField(max_length=60, blank=True, null=True)
    
    # User-specific metadata
    user = models.ForeignKey(User)
    camp = models.ForeignKey(Camp)
    rand_id = models.CharField(max_length=8, unique=True, editable=False)
    
    # Logistical information
    arrival_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Tell us the time you\'ll be arriving at Spark Camp (format: 2006-10-25 14:30).'
    )
    departure_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Tell us the time you\'ll be leaving Spark Camp (format: 2006-10-25 14:30).'
    )
    hotel_booked = models.BooleanField(
        blank=True,
        default=False,
        help_text='Check here if you\'ve taken care of your hotel room.'
    )
    
    def __unicode__(self):
        return u'%s Invite: %s %s (%s)' % (self.camp, self.user.first_name, self.user.last_name, self.user.username)
        
    def is_waitlisted(self):
        "Calculates whether the invitation has been waitlisted."
        import datetime
        today = datetime.date.today()
        if self.expires < today and self.status == 'P':
            return True
        else:
            return False
    
    def price(self):
        if self.special_cost:
            return self.special_cost
        else:
            return self.camp.ticket_cost
    
    @models.permalink
    def get_absolute_url(self):
        return ('invitation', [str(self.rand_id)])
            
    class Meta:
        unique_together = ('user', 'camp')
        order_with_respect_to = 'user'
        
    def save(self, *args, **kwargs):
        if self.id is None:
            self.rand_id = random_number = random.randrange(10000000,99999999) #Generate a random ID so we can retrieve and edit this anonymously
        if self.expires is None:
            self.expires = self.camp.start_date
        super(Invitation, self).save(*args, **kwargs) # Call the "real" save() method.

class Stipend(models.Model):
    invitation = models.ForeignKey(Invitation, unique=True)
    SUBSIDY_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('U', 'Unsure'),
    )
    
    cost_estimate = models.IntegerField(
        max_length=140,
        null=True,
        blank=True,
        help_text='How much do you estimate air and ground transportation will cost? Don\'t include lodging and meals. (Just numbers, no dollar signs or symbols.)'
    )
    employer_subsidized = models.CharField(
        max_length=1,
        choices=SUBSIDY_CHOICES,
        default='U',
        help_text='Will your employer provide any funds towards travel?',
        verbose_name='Employer will cover some costs'
    )
    employer_percentage = models.IntegerField(
        blank=True,
        null=True,
        help_text='What percentage of the cost will your employer cover? (Just numbers, no dollar signs or symbols.)'
    )
    invitee_percentage = models.IntegerField(
        blank=True,
        null=True,
        help_text='What percentage of the cost can you cover yourself? (Just numbers, no dollar signs or symbols.)'
    )
    details = models.TextField(
        blank=True,
        help_text='Please explain any other factors that would assist us in processing this request.'
    )

class Ignite(models.Model):
    invitation = models.ForeignKey(Invitation, unique=True)
    EXPERIENCE_CHOICES = (
        ('Y', 'Yep, I\'m an Ignite pro.'),
        ('M', 'I think I\'ve done something similar.'),
        ('N', 'No, but I think I\'ll be OK.'),
    )
    
    title = models.CharField(
        max_length=140,
        help_text='What\'s the title of your proposed talk?'
    )
    experience = models.CharField(max_length=1, help_text='Have you done an Ignite or similar presentation before?', choices=EXPERIENCE_CHOICES)
    description = models.TextField(help_text='What\'s your talk about? Give us a little detail.')
    
class Roommate(models.Model):
    invitation = models.ForeignKey(Invitation, unique=True)
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other / Prefer not to say'),
    )
    ROOMMATE_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('A', 'Comfortable with anyone'),
    )
    
    sex = models.CharField(
        max_length=1,
        help_text='What\'s your sex?',
        choices=SEX_CHOICES
    )
    roommate = models.CharField(
        max_length=1,
        help_text='What sex are you comfortable rooming with?',
        choices=ROOMMATE_CHOICES
    )
    more = models.CharField(
        max_length=140,
        blank=True,
        help_text='Anything else we should know?'
    )

class Session(models.Model):
    invitation = models.ForeignKey(Invitation, unique=True)
    title = models.CharField(
        max_length=140,
        help_text='Suggest a name for this session'
    )
    description = models.TextField(
        help_text='What do you expect the session to be about?'
    )
    
class PlusOne(models.Model):
    invitation = models.ForeignKey(Invitation, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    employer = models.CharField(
        max_length=140,
        blank=True,
        help_text='Person\'s place of work'
    )
    job_title = models.CharField(
        max_length=140,
        blank=True,
        help_text='Person\'s job title'
    )
    reason = models.TextField(
        help_text='Tell us why this person would be great for Spark Camp.'
    )

class SparkProfile(models.Model):
    user = models.OneToOneField(User)
    has_headshot = models.BooleanField(
        default=False,
        verbose_name='Headshot sent',
        help_text='Check this if you\'ve sent your headshot to sparkcampphotos@gmail.com.'
    )
    bio = models.CharField(
        max_length=140,
        blank=True,
        help_text='Tell us your bio. Keep it Twitter-length.'
    )
    employer = models.CharField(
        max_length=140,
        blank=True,
        help_text='The name of your primary employer.'
    )
    twitter = models.CharField(
        max_length=20,
        blank=True,
        help_text='What\'s your Twitter username?'
    )
    url = models.URLField(
        blank=True,
        help_text='Link to your personal site or profile.'
    )
    email = models.EmailField(
        blank=True,
        help_text='Preferred email address.'
    )
    secondary_email = models.EmailField(
        blank=True,
        help_text='Alternate (or admin assistant) email address.'
    )
    job_title = models.CharField(
        max_length=140,
        blank=True,
        help_text='Your job title.'
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
        help_text='Preferred phone number for us to reach you.'
    )
    dietary = models.CharField(
        max_length=140,
        blank=True,
        default='None',
        help_text='Please note any food allergies or restrictions here.',
        verbose_name='Dietary needs'
    )
    
    # User details for admins.
    poc = models.BooleanField(
        blank=True,
        default=False,
        verbose_name='Person of color'
    )
    woman = models.BooleanField(
        blank=True,
        default=False
    )
    journo = models.BooleanField(
        blank=True,
        default=False,
        help_text='Works predominantly in the news industry?'
    )
    
    def __unicode__(self):
        return u'%s\'s SparkProfile' % (self.user.username)

# Create a SparkProfile whenever a User instance is created    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        SparkProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)
