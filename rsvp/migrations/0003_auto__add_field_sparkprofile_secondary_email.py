# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SparkProfile.secondary_email'
        db.add_column('rsvp_sparkprofile', 'secondary_email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SparkProfile.secondary_email'
        db.delete_column('rsvp_sparkprofile', 'secondary_email')


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
            'Meta': {'ordering': "('_order',)", 'unique_together': "(('user', 'camp'),)", 'object_name': 'Invitation'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'secondary_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
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