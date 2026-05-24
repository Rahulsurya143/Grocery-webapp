var productModal = $("#productModal");

function loadUnits() {
    var $uoms = $("#uoms");
    $uoms.empty().append('<option value="">--Loading units...--</option>');

    console.log('Loading UOMs from', uomListApiUrl);
    $.get(uomListApiUrl, function (response) {
        if(response && response.length > 0) {
            var options = '<option value="">--Select--</option>';
            $.each(response, function(index, uom) {
                options += '<option value="'+ uom.uom_id +'">'+ uom.uom_name +'</option>';
            });
            $uoms.empty().html(options);
        } else {
            $uoms.empty().append('<option value="">--No units available--</option>');
            console.warn('No units returned from /getUOM');
        }
    }).fail(function(xhr, status, error) {
        $uoms.empty().append('<option value="">--Failed to load units--</option>');
        console.error('Failed to load units', status, error, xhr.responseText);
    });
}

$(function () {
    // Load units immediately
    loadUnits();

    //JSON data by API call - Load products list
    $.get(productListApiUrl, function (response) {
        if(response) {
            var table = '';
            $.each(response, function(index, product) {
                table += '<tr data-id="'+ product.product_id +'" data-name="'+ product.name +'" data-unit="'+ product.uom_id +'" data-price="'+ product.price_per_unit +'">' +
                    '<td>'+ product.name +'</td>'+
                    '<td>'+ product.uom_name +'</td>'+
                    '<td>'+ product.price_per_unit +'</td>'+
                    '<td><span class="btn btn-xs btn-danger delete-product">Delete</span></td></tr>';
            });
            $("table").find('tbody').empty().html(table);
        }
    });
});

    // Save Product
    $("#saveProduct").on("click", function () {
        var data = $("#productForm").serializeArray();
        var requestPayload = {
            product_name: null,
            uom_id: null,
            price_per_unit: null
        };
        for (var i=0;i<data.length;++i) {
            var element = data[i];
            switch(element.name) {
                case 'name':
                    requestPayload.product_name = element.value.trim();
                    break;
                case 'uoms':
                    requestPayload.uom_id = element.value;
                    break;
                case 'price':
                    requestPayload.price_per_unit = element.value.trim();
                    break;
            }
        }

        if (!requestPayload.product_name) {
            alert('Please enter a product name.');
            return;
        }
        if (!requestPayload.uom_id) {
            alert('Please select a unit.');
            return;
        }
        if (!requestPayload.price_per_unit || isNaN(requestPayload.price_per_unit)) {
            alert('Please enter a valid price.');
            return;
        }

        callApi("POST", productSaveApiUrl, {
            'data': JSON.stringify(requestPayload)
        });
    });

    $(document).on("click", ".delete-product", function (){
        var tr = $(this).closest('tr');
        var data = {
            product_id : tr.data('id')
        };
        var isDelete = confirm("Are you sure to delete "+ tr.data('name') +" item?");
        if (isDelete) {
            callApi("POST", productDeleteApiUrl, data);
        }
    });

    productModal.on('hide.bs.modal', function(){
        $("#id").val('0');
        $("#name, #uoms, #price").val('');
        productModal.find('.modal-title').text('Add New Product');
    });

    productModal.on('show.bs.modal', function(){
        // Reload units when modal opens
        loadUnits();
    });