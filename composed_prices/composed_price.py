# -*- coding: utf-8 -*-
# Copyright 2015 Luis M. Ontalba
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _

class composed_price(models.Model):
    _name = 'composed.price'
    _order = 'parent_id,product_tmpl_id'
    _rec_name = 'product_tmpl_id'

    brother_id = fields.Many2one('composed.price', 'Subset')
    product_tmpl_id = fields.Many2one('product.template', 'Product')
    child_ids = fields.One2many(
        'composed.price',
        'parent_id',
        'Children')
    parent_id = fields.Many2one ('composed.price', 'Parent')
    product_qty = fields.Float ('Quantity', (3,2), default = 1.00)
    standard_price = fields.Float(
        'Purchase price',
        digits = (3,2),
        compute = '_get_standard_price')
    unit_cost = fields.Float(
        'Unit cost',
        digits = (3,2),
        compute = '_get_unit_cost')
    subtotal_cost = fields.Float(
        'Subtotal cost',
        digits = (3,2),
        compute = '_get_subtotal_cost')
    composed_cost = fields.Float(
        'Composed cost',
        digits = (3,2),
        compute = '_get_composed_cost')
        
    @api.depends('standard_price')
    def _get_standard_price(self):
        for rec in self:
            if rec.brother_id.standard_price:
                rec.standard_price = rec.brother_id.standard_price
            rec.standard_price = rec.product_tmpl_id.standard_price
    
    @api.depends('unit_cost')
    def _get_unit_cost(self):
        for rec in self:
            if rec.brother_id.composed_cost != 0.00:
                rec.unit_cost = rec.brother_id.composed_cost
            elif rec.composed_cost != 0.00:
                rec.unit_cost = rec.composed_cost
            else:
                rec.unit_cost = rec.standard_price
                
    @api.depends('subtotal_cost')
    def _get_subtotal_cost(self):
        for rec in self:
            rec.subtotal_cost = rec.product_qty * rec.unit_cost
    
    @api.depends('composed_cost')
    def _get_composed_cost(self):
        for rec in self:
            rec.composed_cost = sum(line.subtotal_cost for line in rec.child_ids)
