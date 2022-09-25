let tblSales;

$(function () {
    tblSales = $('#data').DataTable({
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
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "client.first_name"},
            {"data": "client.last_name"},
            {"data": "date_joined"},
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "total"},
            {"data": "id"},
        ],
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
                    let buttons = '<button type="button" rel="details" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></button> ';
                    buttons += '<a href="/erp/sale/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
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
    });
});