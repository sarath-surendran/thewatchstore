$(document).ready(function () {
    
    $('.paywithRazorPay').click(function (e) { 
        e.preventDefault();

        var address_id = $("[name='delivery address']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if(address_id == "")
        {
            alert("Select an Address.");
            return false;
        }
        else
        {
            data = {
                "address_id" :  address_id,
                csrfmiddlewaretoken : token,
            }
            $.ajax({
                method: "POST",
                url: "/orders/proceed_to_pay",
                data: data,
                success: function (response) {
                    // console.log(response.first_name)
                    var options = {
                        "key": "", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Watch Store", //your business name
                        "description": "Test Transaction",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (response2){
                            alert(response2.razorpay_payment_id);
                            // alert(response.razorpay_order_id);
                            // alert(response.razorpay_signature)
                            data2 = {
                                'delivery address': address_id,
                                'payment_mode': "Paid by RazorPay",
                                'payment_id': response2.razorpay_payment_id,
                                'total_price':response.total_price,
                                csrfmiddlewaretoken : token,
                            }

                            $.ajax({
                                method: "POST",
                                url: "/orders/place_order_online",
                                data: data2,
                                success: function (response3) {
                                    var confirmation_url = '/orders/order_confirmation/';
                                    var confirmation_url_with_context = confirmation_url + '?order_number=' + response3.order_number + '&total=' + response3.total;
                                    // var confirmation_url_with_context = confirmation_url +'/'+response3.order_number +'/'+response3.total;
                                    window.location.href = confirmation_url_with_context;

                                }
                            });

                        },
                        "prefill": {
                            "name": response.first_name + "" + response.last_name, //your customer's name
                            "email": response.email,
                            "contact": response.phone
                        },
                        // "notes": {
                        //     "address": "Razorpay Corporate Office"
                        // },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    // rzp1.on('payment.failed', function (response){
                    //         alert(response.error.code);
                    //         alert(response.error.description);
                    //         alert(response.error.source);
                    //         alert(response.error.step);
                    //         alert(response.error.reason);
                    //         alert(response.error.metadata.order_id);
                    //         alert(response.error.metadata.payment_id);
                    // });
                    rzp1.open();
                }
            });
           
        }
        
        
    });
});

$(document).ready(function() {
    $('#apply-coupon-link').click(function(e) {
        e.preventDefault();
        // var couponCode = prompt('Enter coupon code:');
        // console.log('Coupon code entered:', couponCode);
        // if (couponCode) {
        //     applyCoupon(couponCode);
        // }
        // $("#coupon-box").toggle();
        $("#coupon_input").toggle();
        $("#coupon_submit").toggle();
    });

    var discount = 0
    var grand_total = 0

    $("#coupon_submit").click(function (e) { 
        e.preventDefault();
        var coupon = $("#coupon_input").val();
        var token = $("[name='csrfmiddlewaretoken']").val();
        data = {
            "coupon": coupon,
            csrfmiddlewaretoken : token,

        }
        $.ajax({
            method : "POST",
            url: "/cart/verify_coupon",
            data: data,
            success: function (response) {
                if (response.valid){
                    console.log('Success');
                    $("#apply-coupon-link").hide();
                    $("#coupon_box").hide();
                    $("#coupon_input").hide();
                    $("#coupon_submit").hide();
                    $('#invalid-coupon-message').hide()
                    $("#coupon-applied-message").show();
                    $('#discount').text(response.discount)
                    discount = response.discount
                    $('#coupon_list').show()
                    $('#total_price').text(response.grand_total);
                    grand_total = response.grand_total
                }
                else{
                    $('#invalid-coupon-message').show()
                }
                    
            },
            // error: function(jqXHR, textStatus, errorThrown) {
            //     console.log('Error:', textStatus, errorThrown);
            // },
        });
    });

    $('#remove_coupon').click(function (e) { 
        e.preventDefault();
        var token = $("[name='csrfmiddlewaretoken']").val();
        data = {
            'discount': discount,
            'grand_total': grand_total,
            csrfmiddlewaretoken : token,
        }
        $.ajax({
            method: "POST",
            url: "/cart/remove_coupon",
            data: data,
            success: function (responsea) {
                $("#apply-coupon-link").show();
                $("#coupon-applied-message").hide();
                $('#coupon_list').hide()
                $('#total_price').text(responsea.grand_total);
            }
        });
    });


});















