# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'kvmstatus'
        db.delete_table(u'webkvm_kvmstatus')


        # Renaming column for 'kvm_list.status' to match new field type.
        db.rename_column(u'webkvm_kvm_list', 'status_id', 'status')
        # Changing field 'kvm_list.status'
        db.alter_column(u'webkvm_kvm_list', 'status', self.gf('django.db.models.fields.CharField')(max_length=20))
        # Removing index on 'kvm_list', fields ['status']
        db.delete_index(u'webkvm_kvm_list', ['status_id'])


        # Changing field 'kvm_list.kvm_location'
        db.alter_column(u'webkvm_kvm_list', 'kvm_location', self.gf('django.db.models.fields.CharField')(max_length=40))

    def backwards(self, orm):
        # Adding index on 'kvm_list', fields ['status']
        db.create_index(u'webkvm_kvm_list', ['status_id'])

        # Adding model 'kvmstatus'
        db.create_table(u'webkvm_kvmstatus', (
            ('offline', self.gf('django.db.models.fields.CharField')(max_length=20)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('online', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'webkvm', ['kvmstatus'])


        # Renaming column for 'kvm_list.status' to match new field type.
        db.rename_column(u'webkvm_kvm_list', 'status', 'status_id')
        # Changing field 'kvm_list.status'
        db.alter_column(u'webkvm_kvm_list', 'status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webkvm.kvmstatus']))

        # Changing field 'kvm_list.kvm_location'
        db.alter_column(u'webkvm_kvm_list', 'kvm_location', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'webkvm.kvm_list': {
            'Meta': {'ordering': "['-create_time']", 'object_name': 'kvm_list'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'kvm_location': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webkvm.kvmtag']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'vir_disk': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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