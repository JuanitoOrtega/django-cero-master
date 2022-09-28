$(function () {
    $('#data').DataTable({
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
            dataSrc: ''
        },
        columns: [
            {'data': 'id'},
            {'data': 'image'},
            {'data': 'username'},
            {'data': 'first_name'},
            {'data': 'last_name'},
            {'data': 'email'},
            {'data': 'date_joined'},
            {'data': 'last_login'},
            {'data': 'is_superuser'},
            {'data': 'is_staff'},
            {'data': 'id'}
        ],
        columnDefs: [
            {
                targets: [-10],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.image + '" alt="' + row.first_name + ' ' + row.last_name + '" class="img-fluid mx-auto d-block" style="width: 40px; height: 40px;" />';
                }
            },
            {
                targets: [-2,-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (data === true) {
                        return '<i class="fas fa-check-square text-success"></i>';
                    } else {
                        return '<i class="fas fa-check-square text-secondary"></i>';
                    }
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="/user/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/user/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            }
        ],
        initComplete: function (settings, json) {
            // alert('Tabla cargada');
        }
    });
});