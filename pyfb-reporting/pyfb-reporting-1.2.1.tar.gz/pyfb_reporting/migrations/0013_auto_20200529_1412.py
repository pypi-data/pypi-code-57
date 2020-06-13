# Generated by Django 2.1.8 on 2020-05-29 14:12

import datetime

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pyfb_reporting', '0012_auto_20200529_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cdr',
            name='aleg_uuid',
            field=models.CharField(default='', max_length=100, verbose_name='a leg call-ID'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='call_class',
            field=models.CharField(default='', help_text='Class of calls.', max_length=10, verbose_name='Class of call'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='callee_number',
            field=models.CharField(default='', max_length=100, verbose_name='Dest. number'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='caller_number',
            field=models.CharField(default='', max_length=100, verbose_name='caller ID num'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='cost_rate',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=11, verbose_name='buy rate'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_related', to='pyfb_company.Customer', verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='customer_ip',
            field=models.CharField(default='', help_text='Customer IP address.', max_length=100, verbose_name='customer IP address'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='direction',
            field=models.CharField(default='', help_text='Type of calls.', max_length=10, verbose_name='Type of call'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='duration',
            field=models.DecimalField(decimal_places=3, default=0, help_text='effective call duration in s.', max_digits=13, verbose_name='call duration'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime.now(), verbose_name='hangup time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cdr',
            name='hangup_disposition',
            field=models.CharField(default='', max_length=100, verbose_name='hangup disposition'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carrier_related', to='pyfb_company.Provider', verbose_name='provider'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='rate',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=11, verbose_name='sell rate'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='read_codec',
            field=models.CharField(default='', max_length=20, verbose_name='read codec'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='sip_charge_info',
            field=models.CharField(default='', help_text='Contents of the P-Charge-Info header for billing purpose.', max_length=100, verbose_name='charge info'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='sip_code',
            field=models.CharField(db_index=True, default='', max_length=3, verbose_name='hangup SIP code'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='sip_reason',
            field=models.TextField(default='', max_length=255, verbose_name='hangup SIP reason'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='sip_rtp_rxstat',
            field=models.CharField(default='', max_length=30, verbose_name='sip rtp rx stat'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='sip_rtp_txstat',
            field=models.CharField(default='', max_length=30, verbose_name='sip rtp tx stat'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='sip_user_agent',
            field=models.CharField(default='', max_length=100, verbose_name='sip user agent'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='start_time',
            field=models.DateTimeField(db_index=True, default=datetime.datetime.now(), verbose_name='start time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cdr',
            name='total_cost',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=11, verbose_name='total cost'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='total_sell',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=11, verbose_name='total sell'),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='write_codec',
            field=models.CharField(default='', max_length=20, verbose_name='write codec'),
        ),
    ]
