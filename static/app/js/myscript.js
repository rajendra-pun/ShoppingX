$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// for increasing, decreasing, removing product in cart
$('.plus-cart').click(function () {
    var id = $(this).attr('pid').toString();
    console.log('id clicked');
    var eml = this.parentNode.children[2];
    console.log(eml)
    
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id: id
        },
        success: function (data) {
            console.log(data)
            // show increment when we click on plus button
            eml.innerText = data.quantity;
            // showing total all amount of all products
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;
        }
    })
})

// for minus button of cart product
$('.minus-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type:'GET',
        url:'/minuscart',
        data:{
            prod_id: id
        },
        success: function(data){
            // show decrement when we click on plus button
            eml.innerText = data.quantity;
            // showing total all amount of all products
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;

        }
    })
})

// remove or delete cart
$('.remove-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml = this;

    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id: id
        },
        success: function(data) {
            console.log('delete');
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;
            // eml.parentNode.parentNode.parentNode.parentNode.remove()
            var cartrow = document.getElementById('cart-row');
            cartrow.remove();
        }
    })
})