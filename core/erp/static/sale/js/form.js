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
  },
  list: function() {
    this.calculus();
    $('#tblProducts').DataTable({
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
            return '<button rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></button>';
          }
        },
        {
          targets: [-3],
          class: 'text-center',
          orderable: false,
          render: function(data, type, row) {
            return '$ ' + parseFloat(data).toFixed(2);
          }
        },
        {
          targets: [-2],
          class: 'text-center',
          orderable: false,
          render: function(data, type, row) {
            return '<input type="text" name="quantity" class="form-control form-control-sm" autocomplete="off" value="'+row.quantity+'">';
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
    format: 'L',
    locale: 'es',
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
      console.log(sale.items);
      sale.add(ui.item);
      $(this).val('');
    }
  });
});