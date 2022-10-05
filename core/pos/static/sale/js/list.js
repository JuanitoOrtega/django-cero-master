let tblSales;
let input_daterange;

let sale = {
    list: function (all) {
        let parameters = {
            'action': 'search',
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblSales = $('#data').DataTable({
            scrollX: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            language: {
                url: '../../../../../static/datatables/lang/es-ES.json'
            },
            ajax: {
                url: pathname,
                type: 'POST',
                data: parameters,
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                }
            },
            columns: [
                // Aplicando Child rows de datatables para ver el detalle de las ventas
                {
                    className: 'dt-control',
                    orderable: false,
                    data: null,
                    defaultContent: '',
                },
                {"data": "number"},
                {"data": "client.first_name"},
                {"data": "client.last_name"},
                {"data": "subtotal"},
                {"data": "iva"},
                {"data": "total_iva"},
                {"data": "total"},
                {"data": "id"},
            ],
            order: [[0, "desc"], [2, "desc"]],
            columnDefs: [
                {
                    targets: [-2, -3, -4, -5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="' + pathname + 'invoice/pdf/' + row.id + '/" target="_blank" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                        buttons += '<button type="button" rel="details" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></button> ';
                        buttons += '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a class="badge badge-secondary badge-pill pointer" rel="number">' + data + '</a>'
                    }
                }
            ],
            initComplete: function (settings, json) {

            }
        });
    },
    formatRowHtml: function (d) {
        let html = '<table class="table">';
        html += '<thead class="thead-dark">';
        html += '<tr>';
        html += '<th scope="col">Producto</th>';
        html += '<th scope="col">Categoría</th>';
        html += '<th scope="col">Precio</th>';
        html += '<th scope="col">Cantidad</th>';
        html += '<th scope="col">Subtotal</th>';
        html += '</tr>';
        html += '</thead>';
        html += '<tbody>';
        $.each(d.details, function (key, value) {
            html += '<tr>';
            html += '<th scope="row">' + value.product.product_name + '</th>';
            html += '<td>' + value.product.category.name + '</td>';
            html += '<td>' + value.product.price + '</td>';
            html += '<td>' + value.quantity + '</td>';
            html += '<td>' + value.subtotal + '</td>';
            html += '</tr>';
        });
        html += '</tbody>';
        html += '</table>';
        return html;
    }
}

$(function () {
    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });

    $('.drp-buttons').hide();

    $('.btnSearch').on('click', function () {
        sale.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        sale.list(true);
    });

    $('#data tbody')
        .off()
        .on('click', 'button[rel="details"]', function () {
        let tr = tblSales.cell($(this).closest('td, li')).index();
        let data = tblSales.row(tr.row).data();
        // console.log(data);

        $('#tblDetail').DataTable({
            scrollX: true,
            autoWidth: true,
            destroy: true,
            deferRender: true,
            language: {
                url: '../../../../../static/datatables/lang/es-ES.json'
            },
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_products_detail',
                    'id': data.id
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                }
            },
            // # Otra forma de acceder a los detalles de una venta
            // data: data.details,
            columns: [
                {"data": "product.product_name"},
                {"data": "product.category.name"},
                {"data": "price"},
                {"data": "quantity"},
                {"data": "subtotal"}
            ],
            columnDefs: [
                {
                    targets: [-1, -3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                }
            ],
            initComplete: function (settings, json) {

            }
        });

        $('#detailModal').modal('show');

    })
        .on('click', 'a[rel="number"]', function () {
            var tr = $(this).closest('tr');
            var row = tblSale.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(sale.formatRowHtml(row.data())).show();
                tr.addClass('shown');
            }
        });
    sale.list(false);
});