let tblClient;
let modal_title;
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
            {"data": "gender.name"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<button rel="edit" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></button> ';
                    buttons += '<button rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></button>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    modal_title = $('.modal-title');

    getData();

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Crear nuevo cliente');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('#clientModal form')[0].reset();
        $('#clientModal').modal('show');
    });

    $('.btnUpdate').on('click', function () {
        getData();
    });

    // Para editar registros
    $('#data tbody')
        .on('click', 'button[rel="edit"]', function () {
        modal_title.find('span').html('Editar cliente');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        let tr = tblClient.cell($(this).closest('td, li')).index();
        let data = tblClient.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="first_name"]').val(data.first_name);
        $('input[name="last_name"]').val(data.last_name);
        $('input[name="ci"]').val(data.ci);
        $('input[name="birthday"]').val(data.birthday);
        $('input[name="address"]').val(data.address);
        $('select[name="gender"]').val(data.gender.id);
        $('#clientModal').modal('show');
    })
        .on('click', 'button[rel="delete"]', function () {
        let tr = tblClient.cell($(this).closest('td, li')).index();
        let data = tblClient.row(tr.row).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estás seguro que quieres eliminar este registro?', parameters, function () {
            tblClient.ajax.reload();
        });
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