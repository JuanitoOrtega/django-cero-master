function message_error(obj) {
    let html = '';
    if (typeof obj === 'object') {
        html = '<ul style="list-style:none;padding-inline-start: 0px;">';
        $.each(obj, function (key, value) {
            html += '<li>' + value + '</li>';
            console.log(key);
            console.log(value);
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error',
        confirmButtonText: 'Cerrar'
    });
}

function submit_with_ajax(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'modern',
        title: title,
        icon: 'fa fa-bell',
        content: content,
        columnClass: 'medium',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: false,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, // window.location.pathname
                        type: 'POST',
                        data: parameters,
                        dataType: 'json'
                    }).done(function(data) {
                        console.log(data);
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function(jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function(data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    });
}