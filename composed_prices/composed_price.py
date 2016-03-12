# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo - BoM cost
#    Copyright (C) 2016 Luis Martinez Ontalba (www.tecnisagra.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _

class composed_price(models.Model):
    _name = 'composed.price'
    _order = 'parent_id,product_tmpl_id'
    
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
            else:
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
        
    _rec_name = 'product_tmpl_id'
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
