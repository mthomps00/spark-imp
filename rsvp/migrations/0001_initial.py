# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Camp'
        db.create_table('rsvp_camp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('logistics', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('hotel', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('hotel_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('hotel_code', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('hotel_deadline', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('venue', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('venue_address', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('ignite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('stipends', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('spreadsheet_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('mailchimp_list', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
        ))
        db.send_create_signal('rsvp', ['Camp'])

        # Adding model 'Invitation'
        db.create_table('rsvp_invitation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Q', max_length=1)),
            ('type', self.gf('django.db.models.fields.CharField')(default='G', max_length=1)),
            ('plus_one', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('inviter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rsvp.Invitation'], null=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('camp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rsvp.Camp'])),
            ('rand_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('dietary', self.gf('django.db.models.fields.CharField')(default='None', max_length=140, blank=True)),
            ('arrival_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('departure_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('hotel_booked', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('rsvp', ['Invitation'])

        # Adding unique constraint on 'Invitation', fields ['user', 'camp']
        db.create_unique('rsvp_invitation', ['user_id', 'camp_id'])

        # Adding model 'Stipend'
        db.create_table('rsvp_stipend', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invitation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rsvp.Invitation'], unique=True)),
            ('cost_estimate', self.gf('django.db.models.fields.IntegerField')(max_length=140, null=True, blank=True)),
            ('employer_subsidized', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
            ('employer_percentage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('invitee_percentage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('rsvp', ['Stipend'])

        # Adding model 'Ignite'
        db.create_table('rsvp_ignite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invitation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rsvp.Invitation'], unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('experience', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('rsvp', ['Ignite'])

        # Adding model 'Roommate'
        db.create_table('rsvp_roommate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invitation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rsvp.Invitation'], unique=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('roommate', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('more', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
        ))
        db.send_create_signal('rsvp', ['Roommate'])

        # Adding model 'Session'
        db.create_table('rsvp_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invitation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rsvp.Invitation'], unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('rsvp', ['Session'])

        # Adding model 'PlusOne'
        db.create_table('rsvp_plusone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invitation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rsvp.Invitation'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('employer', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('reason', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('rsvp', ['PlusOne'])

        # Adding model 'SparkProfile'
        db.create_table('rsvp_sparkprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('bio', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('employer', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('poc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('woman', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('journo', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('rsvp', ['SparkProfile'])


    def backwards(self, orm):
        # Removing unique constraint on 'Invitation', fields ['user', 'camp']
        db.delete_unique('rsvp_invitation', ['user_id', 'camp_id'])

        # Deleting model 'Camp'
        db.delete_table('rsvp_camp')

        # Deleting model 'Invitation'
        db.delete_table('rsvp_invitation')

        # Deleting model 'Stipend'
        db.delete_table('rsvp_stipend')

        # Deleting model 'Ignite'
        db.delete_table('rsvp_ignite')

        # Deleting model 'Roommate'
        db.delete_table('rsvp_roommate')

        # Deleting model 'Session'
        db.delete_table('rsvp_session')

        # Deleting model 'PlusOne'
        db.delete_table('rsvp_plusone')

        # Deleting model 'SparkProfile'
        db.delete_table('rsvp_sparkprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rsvp.camp': {
            'Meta': {'object_name': 'Camp'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hotel': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'hotel_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'hotel_deadline': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hotel_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logistics': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mailchimp_list': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'spreadsheet_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'stipends': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'venue_address': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'})
        },
        'rsvp.ignite': {
            'Meta': {'object_name': 'Ignite'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'experience': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rsvp.Invitation']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'rsvp.invitation': {
            'Meta': {'unique_together': "(('user', 'camp'),)", 'object_name': 'Invitation'},
            'arrival_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'camp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rsvp.Camp']"}),
            'departure_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dietary': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '140', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hotel_booked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rsvp.Invitation']", 'null': 'True', 'blank': 'True'}),
            'plus_one': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rand_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Q'", 'max_length': '1'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'G'", 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'rsvp.plusone': {
            'Meta': {'object_name': 'PlusOne'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'employer': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rsvp.Invitation']", 'unique': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reason': ('django.db.models.fields.TextField', [], {})
        },
        'rsvp.roommate': {
            'Meta': {'object_name': 'Roommate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rsvp.Invitation']", 'unique': 'True'}),
            'more': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'roommate': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'rsvp.session': {
            'Meta': {'object_name': 'Session'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rsvp.Invitation']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'rsvp.sparkprofile': {
            'Meta': {'object_name': 'SparkProfile'},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'employer': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'journo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'poc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'woman': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'rsvp.stipend': {
            'Meta': {'object_name': 'Stipend'},
            'cost_estimate': ('django.db.models.fields.IntegerField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'employer_percentage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'employer_subsidized': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rsvp.Invitation']", 'unique': 'True'}),
            'invitee_percentage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['rsvp']