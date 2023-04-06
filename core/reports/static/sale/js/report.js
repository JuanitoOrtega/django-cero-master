let input_daterange;

let report = {
    list: function () {
        let parameters = {
            'action': 'search',
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        }

        $('#data').DataTable({
            responsive: true,
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
            order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print', 'colvis'
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    }
}

$(function () {

    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'es',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
                applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
                cancelLabel: '<i class="fas fa-times"></i> Cancelar',
            },
        })
        .on('hide.daterangepicker', function (ev, picker) {
            report.list();
        });

    $('.drp-buttons').hide();
});