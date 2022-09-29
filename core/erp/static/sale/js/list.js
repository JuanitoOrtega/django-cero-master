let tblSales;

function format(d) {
    // `d` is the original data object for the row
    console.log(d);
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
        html += '<th scope="row">'+value.product.product_name+'</th>';
        html += '<td>'+value.product.category.name+'</td>';
        html += '<td>'+value.product.price+'</td>';
        html += '<td>'+value.quantity+'</td>';
        html += '<td>'+value.subtotal+'</td>';
        html += '</tr>';
    });
    html += '</tbody>';
    html += '</table>';
    return html;
}

$(function () {
    tblSales = $('#data').DataTable({
        // responsive: true,
        scrollX: true,
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
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            // Aplicando Child rows de datatables para ver el detalle de las ventas
            {
                className: 'dt-control',
                orderable: false,
                data: null,
                defaultContent: '',
            },
            {"data": "position"},
            {"data": "client.first_name"},
            {"data": "client.last_name"},
            {"data": "date_joined"},
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "total"},
            {"data": "id"},
        ],
        // order: [[2, 'asc']], // Ordena la lista de ventas
        columnDefs: [
            {
                targets: [-2, -3, -4],
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
                    let buttons = '<a href="/erp/sale/invoice/pdf/' + row.id + '/" target="_blank" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    buttons += '<button type="button" rel="details" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></button> ';
                    buttons += '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/sale/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody').on('click', 'button[rel="details"]', function () {
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
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_details_prod',
                    'id': data.id
                },
                dataSrc: ""
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

    }).on('click', 'td.dt-control', function () {
        let tr = $(this).closest('tr');
        let row = tblSales.row(tr);
 
        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
});