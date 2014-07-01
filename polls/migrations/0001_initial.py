# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Poll'
        db.create_table(u'polls_poll', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'polls', ['Poll'])

        # Adding model 'Voter'
        db.create_table(u'polls_voter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voterID', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'polls', ['Voter'])

        # Adding model 'Choice'
        db.create_table(u'polls_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Poll'])),
            ('choice_text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'polls', ['Choice'])

        # Adding M2M table for field voters on 'Choice'
        m2m_table_name = db.shorten_name(u'polls_choice_voters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('choice', models.ForeignKey(orm[u'polls.choice'], null=False)),
            ('voter', models.ForeignKey(orm[u'polls.voter'], null=False))
        ))
        db.create_unique(m2m_table_name, ['choice_id', 'voter_id'])


    def backwards(self, orm):
        # Deleting model 'Poll'
        db.delete_table(u'polls_poll')

        # Deleting model 'Voter'
        db.delete_table(u'polls_voter')

        # Deleting model 'Choice'
        db.delete_table(u'polls_choice')

        # Removing M2M table for field voters on 'Choice'
        db.delete_table(db.shorten_name(u'polls_choice_voters'))


    models = {
        u'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Poll']"}),
            'voters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['polls.Voter']", 'symmetrical': 'False', 'blank': 'True'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'polls.poll': {
            'Meta': {'object_name': 'Poll'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'polls.voter': {
            'Meta': {'object_name': 'Voter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'voterID': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['polls']