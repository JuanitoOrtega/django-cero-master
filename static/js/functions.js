function message_error(obj) {
  // Si el error viene como objeto y no string
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
  // Si el error viene como string
  // let html = '<ul style="list-style:none;padding-inline-start: 0px;">';
  // $.each(obj, function (key, value) {
  //   html += '<li>' + value + '</li>';
  //   console.log(key);
  //   console.log(value);
  // });
  // html += '</ul>';
  Swal.fire({
    title: 'Error!',
    html: html,
    icon: 'error',
    confirmButtonText: 'Cerrar'
  });
}