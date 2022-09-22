let tblClient;
function getData() {
    tblClient = $('#data').DataTable({
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
            {"data": "first_name"},
            {"data": "last_name"},
            {"data": "ci"},
            {"data": "birthday"},
            {"data": "gender"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    getData();

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        // Opción 1: Para limpiar datos no guardados en los inputs al hacer click en el botón Nuevo registro
        $('form')[0].reset();
        $('#clientModal').modal('show');
    });

    // Opción 2: Para limpiar datos no guardados en los inputs al abrirse el modal
    // $('#clientModal').on('shown.bs.modal', function () {
    //     $('form')[0].reset();
    // });

    $('.btnUpdate').on('click', function () {
        getData();
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        // let parameters = $(this).serializeArray();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estás seguro que quieres realizar esta acción?', parameters, function () {
            $('#clientModal').modal('hide');
            tblClient.ajax.reload();
            // getData();
        });
    });
});