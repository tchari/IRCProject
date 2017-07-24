# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-23 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IRC', '0006_auto_20170722_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardassessment',
            name='number',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Assessment Number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='COP_interestRate',
            field=models.DecimalField(decimal_places=4, max_digits=4, verbose_name='Annual Interest Rate'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='COP_lifeTime',
            field=models.PositiveIntegerField(verbose_name='Equipment Life Expectency'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_BIE_addProdDaysLost',
            field=models.PositiveIntegerField(verbose_name='Additional Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_BIE_annBIEValue',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Daily Business Interruption Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_BIE_directBILoss',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Direct Business Interruption Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_BIE_fullProdDaysLost',
            field=models.PositiveIntegerField(verbose_name='Full Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_BIE_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Business Interruption Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_BIE_totalBIE',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Business Interruption Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_BIE_totalDaysLost',
            field=models.PositiveIntegerField(verbose_name='Total Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_COP_amortizedCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Annual Amortized Capital Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_COP_annualCOP',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Annual Cost of Protection'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_COP_arealCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Equipment Capital Cost for this Area'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_COP_areasServiced',
            field=models.PositiveIntegerField(verbose_name='Areas Serviced by Equipment'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_COP_capExTotal',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Costs Subtotal'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_COP_opEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Operational Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_COP_otherCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Capital Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_COP_otherOpEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Operational Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_COP_residual',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Equipment Residual Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_COP_residualPV',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Equipment Residual Present Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_COP_totalCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Equipment Capital Cost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_OL_MEOHDisposal',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Disposal of MEOH Contaminated Foam'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_OL_customerShippingGoodwill',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Customer Goodwill and Shipping'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_OL_emergPersonnelRisk',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Risk to ERP'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_OL_mgmtTime',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Management Time and Expense'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_OL_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Misc. Other Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_OL_shareholderPartnerRel',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Shareholder and Partner Relations'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_OL_smokePlume',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Third Party Smoke Plume Effects'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_OL_total',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Other Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_PDA_addDmgs',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Additional Damage'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_PDA_adjFactor',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Secondary Damage Adjustment Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_PDA_dmgFactor',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Damage Spread Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_PDA_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Damage Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_PDA_subTotalDmgs',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Damage Subtotal'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_PDA_total',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Damage Cost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_PDA_valueAtRisk',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Value at Risk'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_PL_adjCopy',
            field=models.PositiveIntegerField(verbose_name='# of Similar Equipment'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_PL_adjFreq',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Probability Adjustment Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_PL_baseFreq',
            field=models.DecimalField(decimal_places=9, max_digits=9, verbose_name='Base Probability of Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='FM_PL_freq',
            field=models.DecimalField(decimal_places=9, max_digits=9, verbose_name='Adjusted Probability of Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_BIE_addProdDaysLost',
            field=models.PositiveIntegerField(verbose_name='Additional Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_BIE_annBIEValue',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Daily Business Interruption Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_BIE_directBILoss',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Direct Business Interruption Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_BIE_fullProdDaysLost',
            field=models.PositiveIntegerField(verbose_name='Full Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_BIE_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Business Interruption Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_BIE_totalBIE',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Business Interruption Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_BIE_totalDaysLost',
            field=models.PositiveIntegerField(verbose_name='Total Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_COP_amortizedCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Annual Amortized Capital Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_COP_annualCOP',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Annual Cost of Protection'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_COP_arealCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Equipment Capital Cost for this Area'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_COP_areasServiced',
            field=models.PositiveIntegerField(verbose_name='Areas Serviced by Equipment'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_COP_capExTotal',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Costs Subtotal'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_COP_opEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Operational Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_COP_otherCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Capital Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_COP_otherOpEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Operational Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_COP_residual',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Equipment Residual Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_COP_residualPV',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Equipment Residual Present Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_COP_totalCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Equipment Capital Cost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_OL_MEOHDisposal',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Disposal of MEOH Contaminated Foam'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_OL_customerShippingGoodwill',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Customer Goodwill and Shipping'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_OL_emergPersonnelRisk',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Risk to ERP'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_OL_mgmtTime',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Management Time and Expense'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_OL_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Misc. Other Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_OL_shareholderPartnerRel',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Shareholder and Partner Relations'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_OL_smokePlume',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Third Party Smoke Plume Effects'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_OL_total',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Other Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_PDA_addDmgs',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Additional Damage'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_PDA_adjFactor',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Secondary Damage Adjustment Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_PDA_dmgFactor',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Damage Spread Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_PDA_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Damage Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_PDA_subTotalDmgs',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Damage Subtotal'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_PDA_total',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Damage Cost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_PDA_valueAtRisk',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Value at Risk'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_PL_adjCopy',
            field=models.PositiveIntegerField(verbose_name='# of Similar Equipment'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_PL_adjFreq',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Probability Adjustment Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_PL_baseFreq',
            field=models.DecimalField(decimal_places=9, max_digits=9, verbose_name='Base Probability of Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='F_PL_freq',
            field=models.DecimalField(decimal_places=9, max_digits=9, verbose_name='Adjusted Probability of Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_BIE_addProdDaysLost',
            field=models.PositiveIntegerField(verbose_name='Additional Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_BIE_annBIEValue',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Daily Business Interruption Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_BIE_directBILoss',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Direct Business Interruption Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_BIE_fullProdDaysLost',
            field=models.PositiveIntegerField(verbose_name='Full Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_BIE_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Business Interruption Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_BIE_totalBIE',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Business Interruption Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_BIE_totalDaysLost',
            field=models.PositiveIntegerField(verbose_name='Total Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_COP_amortizedCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Annual Amortized Capital Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_COP_annualCOP',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Annual Cost of Protection'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_COP_arealCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Equipment Capital Cost for this Area'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_COP_areasServiced',
            field=models.PositiveIntegerField(verbose_name='Areas Serviced by Equipment'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_COP_capExTotal',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Costs Subtotal'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_COP_opEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Operational Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_COP_otherCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Capital Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_COP_otherOpEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Operational Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_COP_residual',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Equipment Residual Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_COP_residualPV',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Equipment Residual Present Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_COP_totalCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Equipment Capital Cost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_OL_MEOHDisposal',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Disposal of MEOH Contaminated Foam'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_OL_customerShippingGoodwill',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Customer Goodwill and Shipping'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_OL_emergPersonnelRisk',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Risk to ERP'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_OL_mgmtTime',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Management Time and Expense'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_OL_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Misc. Other Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_OL_shareholderPartnerRel',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Shareholder and Partner Relations'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_OL_smokePlume',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Third Party Smoke Plume Effects'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_OL_total',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Other Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_PDA_addDmgs',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Additional Damage'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_PDA_adjFactor',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Secondary Damage Adjustment Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_PDA_dmgFactor',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Damage Spread Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_PDA_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Damage Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_PDA_subTotalDmgs',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Damage Subtotal'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_PDA_total',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Damage Cost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_PDA_valueAtRisk',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Value at Risk'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_PL_adjCopy',
            field=models.PositiveIntegerField(verbose_name='# of Similar Equipment'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_PL_adjFreq',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Probability Adjustment Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_PL_baseFreq',
            field=models.DecimalField(decimal_places=9, max_digits=9, verbose_name='Base Probability of Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='L_PL_freq',
            field=models.DecimalField(decimal_places=9, max_digits=9, verbose_name='Adjusted Probability of Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_BIE_addProdDaysLost',
            field=models.PositiveIntegerField(verbose_name='Additional Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_BIE_annBIEValue',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Daily Business Interruption Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_BIE_directBILoss',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Direct Business Interruption Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_BIE_fullProdDaysLost',
            field=models.PositiveIntegerField(verbose_name='Full Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_BIE_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Business Interruption Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_BIE_totalBIE',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Business Interruption Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_BIE_totalDaysLost',
            field=models.PositiveIntegerField(verbose_name='Total Equivalent Production Days Lost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_COP_amortizedCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Annual Amortized Capital Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_COP_annualCOP',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Annual Cost of Protection'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_COP_arealCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Equipment Capital Cost for this Area'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_COP_areasServiced',
            field=models.PositiveIntegerField(verbose_name='Areas Serviced by Equipment'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_COP_capExTotal',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Costs Subtotal'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_COP_opEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Operational Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_COP_otherCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Capital Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_COP_otherOpEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Operational Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_COP_residual',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Equipment Residual Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_COP_residualPV',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Capital Equipment Residual Present Value'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_COP_totalCapEx',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Equipment Capital Cost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_OL_MEOHDisposal',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Disposal of MEOH Contaminated Foam'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_OL_customerShippingGoodwill',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Customer Goodwill and Shipping'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_OL_emergPersonnelRisk',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Risk to ERP'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_OL_mgmtTime',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Management Time and Expense'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_OL_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Misc. Other Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_OL_shareholderPartnerRel',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Shareholder and Partner Relations'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_OL_smokePlume',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Third Party Smoke Plume Effects'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_OL_total',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Other Losses'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_PDA_addDmgs',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Additional Damage'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_PDA_adjFactor',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Secondary Damage Adjustment Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_PDA_dmgFactor',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Damage Spread Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_PDA_other',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Other Damage Costs'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_PDA_subTotalDmgs',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Damage Subtotal'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_PDA_total',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Damage Cost'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_PDA_valueAtRisk',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Value at Risk'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_PL_adjCopy',
            field=models.PositiveIntegerField(verbose_name='# of Similar Equipment'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_PL_adjFreq',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Probability Adjustment Factor'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_PL_baseFreq',
            field=models.DecimalField(decimal_places=9, max_digits=9, verbose_name='Base Probability of Loss'),
        ),
        migrations.AlterField(
            model_name='standardassessment',
            name='M_PL_freq',
            field=models.DecimalField(decimal_places=9, max_digits=9, verbose_name='Adjusted Probability of Loss'),
        ),
    ]