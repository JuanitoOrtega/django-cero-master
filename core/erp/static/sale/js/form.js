let tblProducts;
let tblSearchProducts;
let sale = {
    items: {
        client: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: []
    },
    get_ids: function () {
        let ids = [];
        $.each(this.items.products, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculus: function () {
        let subtotal = 0.00;
        let iva = $('input[name="iva"]').val();
        $.each(this.items.products, function (pos, dict) {
            console.log(pos);
            console.log(dict);
            dict.pos = pos;
            dict.subtotal = dict.quantity * parseFloat(dict.price);
            subtotal += dict.subtotal;
        });
        // console.log(subtotal);
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * (iva / 100);
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalculado"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
        $('.btnRemoveAll').attr('disabled', false); // Mi código
    },
    list: function () {
        this.calculus();
        // Mi código
        if (sale.items.products.length === 0) {
            $('.btnRemoveAll').attr('disabled', true);
        }
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            language: {
                url: '../../../../../static/datatables/lang/es-ES.json'
            },
            data: this.items.products,
            columns: [
                {'data': 'id'},
                {'data': 'full_name'},
                {'data': 'stock'},
                {'data': 'price'},
                {'data': 'quantity'},
                {'data': 'subtotal'}
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<button type="button" rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></button>';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (data > 10) {
                            return '<span class="badge badge-success">'+ data +'</span>';
                        }
                        return '<span class="badge badge-danger">'+ data +'</span>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="quantity" class="form-control-sm input-sm" autocomplete="off" value="' + row.quantity + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                }
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                console.log(row);
                console.log(data);
                $(row).find("input[name='quantity']").TouchSpin({
                    min: 1,
                    max: data.stock,
                    stepinterval: 1,
                });
            },
            initComplete: function (settings, json) {
                // alert('Tabla cargada');
            }
        });
        console.clear();
        console.log(this.items);
        console.log(this.get_ids());
    }
}

// Para mejorar el buscador de productos
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    if (!Number.isInteger(repo.id)) {
        return repo.text;
    }

    let container = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-md-2">' +
        '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-md-10 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.full_name + '<br>' +
        '<b>Precio:</b> <span class="badge badge-warning">$' + repo.price + '</span>' + '<br>' +
        '<b>Stock:</b> <span class="badge badge-success">' + repo.stock + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>'
    );

    return container;
}

$(function () {
    $('.select2').select2({
        theme: 'bootstrap4',
        language: 'es'
    });

    // $('#id_date_joined').datetimepicker({
    //   locale: 'es',
    //   format: 'YYYY-MM-DD',
    //   // date: moment().format('YYYY-MM-DD'),
    //   minDate: moment().format('YYYY-MM-DD'),
    //   // maxDate: moment().format('YYYY-MM-DD')
    // });

    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 20,
        step: 1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        console.clear();
        console.log($(this).val());
        sale.calculus();
    }).val('13.00');

    // Search clients
    $('select[name="client"]').select2({
        theme: 'bootstrap4',
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_clients'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                }
            }
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1
    });

    $('.btnAddClient').on('click', function () {
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('hidden.bs.modal', function (e) {
        $('#formClient').trigger('reset');
    })

    $('#formClient').on('submit', function (e) {
        e.preventDefault();
        let parameters = new FormData(this);
        parameters.append('action', 'create_cliente');
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estás seguro que quieres registrar el nuevo cliente?', parameters, function (response) {
            console.log(response);
            let newOption = new Option(response.full_name, response.id, false, true);
            $('select[name="client"]').append(newOption).trigger('change');
            $('#myModalClient').modal('hide');
        });
    });

    // Search products

    // Search products sin usar Select2
    /* $('input[name="search"]').autocomplete({
      source: function (request, response) {
        $.ajax({
          url: window.location.pathname,
          type: 'POST',
          data: {
            'action': 'search_products',
            'term': request.term
          },
          dataType: 'json'
        }).done(function(data) {
          response(data);
        }).fail(function(jqXHR, textStatus, errorThrown) {
          // alert(textStatus + ': ' + errorThrown);
        }).always(function(data) {

        });
      },
      delay: 500,
      minLength: 1,
      select: function(event, ui) {
        event.preventDefault();
        console.log(ui.item);
        console.clear();
        ui.item.quantity = 1;
        ui.item.subtotal = 0.00;
        console.log(sale.items);
        sale.add(ui.item);
        $(this).val('');
      }
    }); */

    $('.btnRemoveAll').on('click', function () {
        alert_action('Notificación', '¿Estás seguro que quieres eliminar todos los items?', function () {
            sale.items.products = [];
            sale.list();
            $('.btnRemoveAll').attr('disabled', true);
        }, function () {

        });
    });

    // Event quantity
    $('#tblProducts tbody')
        .on('click', 'button[rel="remove"]', function () {
            let tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estás seguro que quieres eliminar este item?', function () {
                sale.items.products.splice(tr.row, 1);
                sale.list();
            }, function () {

            });
        })
        .on('change', 'input[name="quantity"]', function () {
            console.clear();
            let quantity = parseInt($(this).val());
            console.log(quantity);
            let tr = tblProducts.cell($(this).closest('td, li')).index();
            sale.items.products[tr.row].quantity = quantity;
            sale.calculus();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + sale.items.products[tr.row].subtotal.toFixed(2));
        });

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            language: {
                url: '../../../../../static/datatables/lang/es-ES.json'
            },
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(sale.get_ids()),
                    'term': $('select[name="search"]').val()
                },
                dataSrc: ""
            },
            columns: [
                {"data": "full_name"},
                {"data": "image"},
                {"data": "stock"},
                {"data": "price"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 40px; height: 40px;">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (data > 10) {
                            return '<span class="badge badge-success">'+ data +'</span>';
                        }
                        return '<span class="badge badge-danger">'+ data +'</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<button type="button" rel="add" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-plus"></i></button>';
                    }
                },
            ],
            initComplete: function (settings, json) {
    
            }
        });
        $('#myModalSearchProducts').modal('show');
    });

    // Agregar productos desde el modal
    $('#tblSearchProducts tbody').on('click', 'button[rel="add"]', function () {
        // console.clear();
        let tr = tblSearchProducts.cell($(this).closest('td, li')).index();
        let product = tblSearchProducts.row(tr.row).data();
        product.quantity = 1;
        product.subtotal = 0.00;
        sale.add(product);
        // console.log(product);
        tblSearchProducts.row($(this).parents('tr')).remove().draw();
    });

    // Event submit
    $('#formSale').on('submit', function (e) {
        e.preventDefault();

        if (sale.items.products.length === 0) {
            message_error('Debe al menos cargar un item para registrar una venta.');
            return false;
        }

        sale.items.date_joined = $('input[name="date_joined"]').val();
        sale.items.client = $('select[name="client"]').val();
        let parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('sale', JSON.stringify(sale.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estás seguro que quieres realizar esta acción?', parameters, function (response) {
            alert_action('Notificación', '¿Desea imprimir la factura?', function () {
                // location.href = '/erp/sale/invoice/pdf/'+response.id+'/';
                window.open('/erp/sale/invoice/pdf/' + response.id + '/', '_blank');
                location.href = '/erp/sale/list/';
            }, function () {
                location.href = '/erp/sale/list/';
            });
        });
    });

    // Buscador de productos usando Select2
    $('select[name="search"]').select2({
        theme: 'bootstrap4',
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_autocomplete',
                    ids: JSON.stringify(sale.get_ids())
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                }
            }
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo
    }).on('select2:select', function (e) {
        let data = e.params.data;
        if (!Number.isInteger(data.id)) {
            return false;
        }
        data.quantity = 1;
        data.subtotal = 0.00;
        sale.add(data);
        $(this).val('').trigger('change.select2');
    });

    sale.list();
});