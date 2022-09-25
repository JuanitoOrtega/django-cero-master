let tblProducts;

let sale = {
  items: {
    client: '',
    date_joined: '',
    subtotal: 0.00,
    iva: 0.00,
    total: 0.00,
    products: []
  },
  calculus: function () {
    let subtotal = 0.00;
    let iva = $('input[name="iva"]').val();
    $.each(this.items.products, function (pos, dict) {
      // console.log(pos);
      // console.log(dict);
      dict.pos = pos;
      dict.subtotal = dict.quantity * parseFloat(dict.price);
      subtotal += dict.subtotal;
    });
    // console.log(subtotal);
    this.items.subtotal = subtotal;
    this.items.iva = this.items.subtotal * (iva / 100);
    this.items.total = this.items.subtotal + this.items.iva;
    $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
    $('input[name="ivacalculado"]').val(this.items.iva.toFixed(2));
    $('input[name="total"]').val(this.items.total.toFixed(2));
  },
  add: function (item) {
    this.items.products.push(item);
    this.list();
    $('.btnRemoveAll').attr('disabled', false); // Mi código
  },
  list: function() {
    this.calculus();
    if (sale.items.products.length === 0) {
      $('.btnRemoveAll').attr('disabled', true);
    }
    tblProducts = $('#tblProducts').DataTable({
      responsive: true,
      autoWidth: false,
      destroy: true,
      language: {
        url: '../../../../../static/datatables/lang/es-ES.json'
      },
      data: this.items.products,
      columns: [
        {'data': 'id'},
        {'data': 'product_name'},
        {'data': 'category.name'},
        {'data': 'price'},
        {'data': 'quantity'},
        {'data': 'subtotal'}
      ],
      columnDefs: [
        {
          targets: [0],
          class: 'text-center',
          orderable: false,
          render: function(data, type, row) {
            return '<button type="button" rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></button>';
          }
        },
        {
          targets: [-3],
          class: 'text-center',
          orderable: false,
          render: function(data, type, row) {
            return '$' + parseFloat(data).toFixed(2);
          }
        },
        {
          targets: [-2],
          class: 'text-center',
          orderable: false,
          render: function(data, type, row) {
            return '<input type="text" name="quantity" class="form-control-sm input-sm" autocomplete="off" value="'+row.quantity+'">';
          }
        },
        {
          targets: [-1],
          class: 'text-center',
          orderable: false,
          render: function(data, type, row) {
            return '$' + parseFloat(data).toFixed(2);
          }
        }
      ],
      rowCallback( row, data, displayNum, displayIndex, dataIndex ) {
        // console.log(row);
        // console.log(data);
        $(row).find("input[name='quantity']").TouchSpin({
          min: 1,
          max: 1000000,
          stepinterval: 1,
        });
      },
      initComplete: function(settings, json) {
        // alert('Tabla cargada');
      }
    });
  }
}

$(function() {
  $('.select2').select2({
    theme: 'bootstrap4',
    language: 'es'
  });

  $('#id_date_joined').datetimepicker({
    locale: 'es',
    format: 'YYYY-MM-DD',
    // date: moment().format('YYYY-MM-DD'),
    minDate: moment().format('YYYY-MM-DD'),
    // maxDate: moment().format('YYYY-MM-DD')
  });

  $("input[name='iva']").TouchSpin({
    min: 0,
    max: 20,
    step: 1,
    decimals: 2,
    boostat: 5,
    maxboostedstep: 10,
    postfix: '%'
  }).on('change', function () {
    // console.clear();
    // console.log($(this).val());
    sale.calculus();
  }).val('13.00');

  // Search products
  $('input[name="search"]').autocomplete({
    source: function (request, response) {
      $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
          'action': 'search_products',
          'term': request.term
        },
        dataType: 'json'
      }).done(function(data) {
        response(data);
      }).fail(function(jqXHR, textStatus, errorThrown) {
        // alert(textStatus + ': ' + errorThrown);
      }).always(function(data) {

      });
    },
    delay: 500,
    minLength: 1,
    select: function(event, ui) {
      event.preventDefault();
      // console.log(ui.item);
      console.clear();
      ui.item.quantity = 1;
      ui.item.subtotal = 0.00;
      // console.log(sale.items);
      sale.add(ui.item);
      $(this).val('');
    }
  });

  $('.btnRemoveAll').on('click', function() {
    alert_action('Notificación', '¿Estás seguro que quieres eliminar todos los items?', function () {
      sale.items.products = [];
      sale.list();
      $('.btnRemoveAll').attr('disabled', true);
    });
  });

  // Event quantity
  $('#tblProducts tbody')
    .on('click', 'button[rel="remove"]', function () {
      let tr = tblProducts.cell($(this).closest('td, li')).index();
      alert_action('Notificación', '¿Estás seguro que quieres eliminar este item?', function () {
        sale.items.products.splice(tr.row, 1);
        sale.list();
      });
    })
    .on('change', 'input[name="quantity"]', function () {
      console.clear();
      let quantity = parseInt($(this).val());
      // console.log(quantity);
      let tr = tblProducts.cell($(this).closest('td, li')).index();
      sale.items.products[tr.row].quantity = quantity;
      sale.calculus();
      $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + sale.items.products[tr.row].subtotal.toFixed(2));
    });

  $('.btnClearSearch').on('click', function () {
    $('input[name="search"]').val('').focus();
  });

  // Event submit
  $('form').on('submit', function (e) {
    e.preventDefault();

    if(sale.items.products.length === 0){
      message_error('Debe al menos tener un item en su detalle de venta');
      return false;
    }

    sale.items.date_joined = $('input[name="date_joined"]').val();
    sale.items.client = $('select[name="client"]').val();
    let parameters = new FormData();
    parameters.append('action', $('input[name="action"]').val());
    parameters.append('sale', JSON.stringify(sale.items));
    submit_with_ajax(window.location.pathname, 'Notificación', '¿Estás seguro que quieres realizar esta acción?', parameters, function () {
        location.href = '/erp/sale/list/';
    });
  });
  sale.list();
});