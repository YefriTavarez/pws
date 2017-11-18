// provide with the namespaces
frappe.provide("pws.ui")
frappe.provide("pws.file")

$(document).ready(function(event) {
    // hide the help menu
    $(".dropdown.dropdown-help.dropdown-mobile").hide()

    $.extend(frappe.app, {
        refresh_notifications: refresh_notifications
    })
})

var refresh_notifications = function() {
    var me = this;
    if (frappe.session_alive) {
        return frappe.call({
            method: "frappe.desk.notifications.get_notifications",
            callback: function callback(r) {
                if (r.message) {
                    $.extend(frappe.boot.notification_info, r.message);
                    $(document).trigger("notification-update");

                    me.update_notification_count_in_modules();

                    if (frappe.get_route()[0] != "messages") {
                        if (r.message.new_messages.length) {
                            frappe.utils.set_title_prefix("(" + r.message.new_messages.length + ")");
                        }
                    }
                }
            },
            freeze: false,
            type: "GET", // to fix the invalid request bug
            args: {
                // to identify requests in the server
                "user": frappe.boot.user_info[frappe.session.user].username
            }
        });
    }
}

// fix the unload bug
_f.Frm.prototype.is_new = function () {
    return this.doc && this.doc.__islocal
}

// custom get_upload_dialog
pws.ui.get_upload_dialog = function (opts) {
    var dialog = new frappe.ui.Dialog({
        title: __('Subir adjuntos'),
        no_focus: true,
        fields: [
            {
                "fieldtype": "Link",
                "fieldname": "attach_type",
                "label": "Tipo de documento a subir",
                "options": "Tipo de Adjunto",
                "onchange": function() {
                    frappe.db.get_value("Tipo de Adjunto", this.value, "abbr", function(data) {
                        if ( ! data) {
                            frappe.throw("¡No se encontro ninguna Abreviacion para dicho Tipo de Adjunto!")
                        }

                        dialog.set_value("abbr", data.abbr)

                        pws.file.abbr = data.abbr
                    })

                    $("#select_files").trigger("change")
                },
                "get_query": function() {
                    return {
                        "query": "pws.queries.attach_type_query"
                    }
                }
            },
            {
                "label": "Abreviacion",
                "fieldtype": "Data",
                "fieldname": "abbr",
                "read_only": true,
                "hidden": true,
            }
        ],
        onhide: function() {
            dialog.$wrapper.remove()
        }
    })

    var select_files = $('<div style="margin: 20px 0px">\
        <label class="btn btn-default btn-attach" for="select_files">\
            <input id="select_files" accept=\"application/pdf\" type="file">\
            Seleccionar archivo\
        </label>\
        <span id="display_name">No se ha seleccionado ningún archivo</span>\
    </div>').appendTo(dialog.body)

    $("#select_files").on("change", function() {
        var $input = $(this)
        var input = $input.get(0)

        if (input.files.length) {
            input.filedata = {
                "files_data": []
            }

            window.file_reading = true

            var abbr = dialog.get_value("abbr")
            var attach_type = dialog.get_value("attach_type")

            var filename = undefined

            if (attach_type) {
                // filename = __("{0}-{1}, {2}({3}) Cant. {4}.pdf", [
                filename = __("{0}-{1}.pdf", [
                    pws.file.abbr,
                    opts.name
                    // opts.item_name.replace("/", "-"),
                    // opts.project_name,
                    // opts.production_qty
                ])
            }

            $.each(input.files, function(key, value) {
                pws.file.setupReader(value, input, filename, attach_type)
            })

            window.file_reading = false
        }

        var display_name = input.files[0] ? 
            input.files[0].name: "No se ha seleccionado ningún archivo"

        $('#display_name').html(display_name)
    })

    // let's make it visible    
    dialog.show()

    return dialog // in case somebody needs it
};

$.extend(pws.file, {
    setupReader: function(file, input, filename, attach_type) {
        var name = file.name
        var reader = new FileReader()

        reader.onload = function(e) {
            input.filedata.files_data.push({
                "__file_attachment": 1,
                "filename": filename || name,
                "dataurl": reader.result,
                "attach_type": attach_type
            })
        }
        reader.readAsDataURL(file)
    }
})

Number.prototype.formatInteger = function(c, d, t) {
    var n = this,
        c = isNaN(c = Math.abs(c)) ? 2 : c,
        d = d == undefined ? "" : d,
        t = t == undefined ? "," : t,
        s = n < 0 ? "-" : "",
        i = String(parseInt(n = Math.abs(Number(n) || 0).toFixed(c))),
        j = (j = i.length) > 3 ? j % 3 : 0;
    return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(0).slice(2) : "");
};

frappe.form.link_formatters['Proyecto'] = function(value, doc) {
    if(doc.project_name && doc.project_name !== value) {
        return value + ': ' + doc.project_name;
    } else if(doc.customer && doc.customer !== value) {
        return value + ': ' + doc.customer;
    } else {
        return value;
    }
}
