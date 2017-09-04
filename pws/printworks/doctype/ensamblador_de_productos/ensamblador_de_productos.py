# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import pws.api

from frappe.model.document import Document
from frappe.model.naming import make_autoname as autoname
from frappe.utils import flt

class EnsambladordeProductos(Document):
    def autoname(self):
        array = pws.api.gut(
            pws.api.s_sanitize(
                self.perfilador_de_productos
            )
        )

        naming_serie = "{0}-.####".format(
            "".join(array))

        self.name = autoname(naming_serie)

    def validate(self):
        new_hash = self.make_new_hash()

        self.hash = new_hash.upper()

        self.after_validate()

    def after_validate(self):
        number_fields = [
            "cantidad_tiro_proceso",
            "cantidad_tiro_pantone",
            "cantidad_proceso_retiro",
            "cantidad_pantone_retiro"
        ]

        for field in number_fields:
            self.set(field, int(self.get(field)))

        self.create_item()

    def make_new_hash(self):
        array = ["".join(
            gut(self.get(key)))
            for key in self.get_fields() 
        if self.get(key)] 


        pre_hash = "".join(array).upper()

        pre_hash_with_textures = "{0}{1}".format(pre_hash,
            self.get_textura_names())

        new_hash = pws.api.s_sanitize(
            u"{0}".format(pre_hash_with_textures))

        # new_hash = pws.api.s_hash(pre_sanitized)

        exists = frappe.get_value("Ensamblador de Productos", {
            "hash": new_hash.upper()
        }, ["name"])

        if exists and not new_hash.upper() == self.hash:
            frappe.throw("""Ensamblador <a href='/desk#Form/Ensamblador de Productos/{0}'>{0}</a> ya existe."""
                .format(exists))

        return new_hash

    def get_textura_names(self):
        array = ""

        for textura in self.opciones_de_textura:
            array += "".join(
                gut(textura.opciones_de_textura))

        return "".join(array)

    def get_fields(self):
        return [
            "perfilador_de_productos",
            "materials",
            "cantidad_tiro_proceso",
            "cantidad_tiro_pantone",
            "cantidad_proceso_retiro",
            "cantidad_pantone_retiro",
            "dimension",
            "opciones_de_control",
            "opciones_de_empalme",
            "opciones_de_plegado",
            "opciones_de_proteccion",
            "opciones_de_utilidad",
            "opciones_de_corte",
        ]

    def create_item(self):
        # new item allocated
        item = frappe.new_doc("Item")

        # alias
        self.perfilador = self.perfilador_de_productos

        # load configuration from the control panel
        products_are_stock_items = frappe.db.get_single_value("Configuracion General", 
            "products_are_stock_items")

        # item group for the profiler
        item_group = frappe.get_value("Perfilador de Productos", 
            self.perfilador, "item_group")

        # if the item exists
        if frappe.get_value("Item", self.name):
            # let's load it and use it
            item = frappe.get_doc("Item", self.name)

        item.update({
            "item_code": self.name,
            "item_name": self.name,
            "item_group": item_group,
            "description": self.get_self_description(),
            "is_stock_item": products_are_stock_items,
            "is_purchase_item": 0,
            "is_sales_item": 1
        })

        item.save()

    def get_self_description(self):
        description = ""

        for field in self.get_fields():
            if self.get(field):
                value = get_label(self.get(field))
                
                description += "{0}, ".format(value)

        return description[:-2]

    def on_trash(self):
        frappe.delete_doc_if_exists("Item", self.name)


def gut(string):
    return [ word
        for part in string.split("-") 
        for word in part.split()
    ]

def get_label(field):
    d = {
        "cantidad_tiro_proceso": "Colres Tiro Proceso",
        "cantidad_tiro_pantone": "Colres Tiro Pantone",
        "cantidad_proceso_retiro": "Colres Retiro Proceso",
        "cantidad_pantone_retiro": "Colres Retiro Pantone"
    }

    if d.get(field):
        return "{0} {1}".format(field, d.get(field))

    return field


# 'cantidad_pantone_retiro',
# 'cantidad_proceso_retiro',
# 'cantidad_tiro_pantone',
# 'cantidad_tiro_proceso',
# 'dimension',
# 'material_calibre',
# 'material_caras',
# 'material_nombre',
# 'materials',
# 'opciones_de_control',
# 'opciones_de_corte',
# 'opciones_de_empalme',
# 'opciones_de_plegado',
# 'opciones_de_proteccion',
# 'opciones_de_textura',
# 'opciones_de_utilidad',
# 'perfilador_de_productos',
