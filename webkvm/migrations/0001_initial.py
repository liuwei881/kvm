# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'kvmtag'
        db.create_table(u'webkvm_kvmtag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'webkvm', ['kvmtag'])

        # Adding model 'kvmstatus'
        db.create_table(u'webkvm_kvmstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('online', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('offline', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'webkvm', ['kvmstatus'])

        # Adding model 'kvm_list'
        db.create_table(u'webkvm_kvm_list', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('vir_disk', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webkvm.kvmtag'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webkvm.kvmstatus'])),
            ('kvm_location', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'webkvm', ['kvm_list'])


    def backwards(self, orm):
        # Deleting model 'kvmtag'
        db.delete_table(u'webkvm_kvmtag')

        # Deleting model 'kvmstatus'
        db.delete_table(u'webkvm_kvmstatus')

        # Deleting model 'kvm_list'
        db.delete_table(u'webkvm_kvm_list')


    models = {
        u'webkvm.kvm_list': {
            'Meta': {'ordering': "['-create_time']", 'object_name': 'kvm_list'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'kvm_location': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webkvm.kvmtag']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webkvm.kvmstatus']"}),
            'vir_disk': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'webkvm.kvmstatus': {
            'Meta': {'object_name': 'kvmstatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offline': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'online': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'webkvm.kvmtag': {
            'Meta': {'object_name': 'kvmtag'},
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['webkvm']