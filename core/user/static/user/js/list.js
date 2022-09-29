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
            {'data': 'position'},
            {'data': 'image'},
            {'data': 'full_name'},
            {'data': 'username'},
            {'data': 'email'},
            {'data': 'date_joined'},
            {'data': 'groups'},
            {'data': 'id'}
        ],
        columnDefs: [
            {
                targets: [-7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.image + '" alt="' + row.first_name + ' ' + row.last_name + '" class="img-fluid mx-auto d-block" style="width: 40px; height: 40px;" />';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let html = '';
                    $.each(data, function (key, value) {
                        html += '<span class="badge badge-success">'+ value.name +'</span> ';
                    });
                    return html;
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