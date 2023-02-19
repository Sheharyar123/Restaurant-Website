let autocomplete;

function initAutoComplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("id_address"),
    {
      types: ["geocode", "establishment"],
      componentRestrictions: { country: ["pak"] },
    }
  );
  // function to specify what should happen when the prediction is clicked
  autocomplete.addListener("place_changed", onPlaceChanged);
}

function onPlaceChanged() {
  let place = autocomplete.getPlace();

  // User did not select the prediction. Reset the input field or alert()
  if (!place.geometry) {
    document.getElementById("id_address").placeholder = "Start typing...";
  } else {
    console.log("place name=>", place.name);
  }
  // get the address components and assign them to the fields
  let geocoder = new google.maps.Geocoder();
  let address = document.getElementById("id_address").value;

  geocoder.geocode({ address: address }, function (results, status) {
    console.log("Results: ", results);
    // console.log("Status: ", status);
    if (status == google.maps.GeocoderStatus.OK) {
      let latitude = results[0].geometry.location.lat();
      let longitude = results[0].geometry.location.lng();

      $("#id_latitude").val(latitude);
      $("#id_longitude").val(longitude);
      $("#id_address").val(address);
    }

    for (let i = 0; i < place.address_components.length; i++) {
      for (let j = 0; j < place.address_components[i].types.length; j++) {
        // get country
        if (place.address_components[i].types[j] == "country") {
          $("#id_country").val(place.address_components[i].long_name);
        }
        // get state
        if (
          place.address_components[i].types[j] == "administrative_area_level_1"
        ) {
          $("#id_state").val(place.address_components[i].long_name);
        }
        // get city
        if (place.address_components[i].types[j] == "locality") {
          $("#id_city").val(place.address_components[i].long_name);
        }
        // get pincode
        if (place.address_components[i].types[j] == "postal_code") {
          $("#id_pin_code").val(place.address_components[i].long_name);
        } else {
          $("#id_pin_code").val("");
        }
      }
    }
  });
}

$(document).ready(function () {
  $(".add_to_cart").on("click", function (e) {
    e.preventDefault();
    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status == "login_required") {
          swal({
            title: response.message,
            text: "",
            icon: "info",
          }).then(function () {
            window.location = "/accounts/login";
          });
        } else if (response.status == "Failed") {
          swal({
            title: response.text,
            text: "",
            icon: "error",
          });
        } else {
          const total_cart_count = response.cart_counter["cart_count"];
          const item_qty = response.cart_quantity;
          $("#cart_counter").html(total_cart_count);
          $("#qty-" + food_id).html(item_qty);
          applyCartAmounts(
            response.cart_amount["subtotal"],
            response.cart_amount["tax"],
            response.cart_amount["grand_total"]
          );
        }
      },
    });
  });

  // Place the cart item quantity on load
  $(".item_qty").each(function () {
    var the_id = $(this).attr("id");
    var qty = $(this).attr("data-qty");
    $("#" + the_id).html(qty);
  });

  $(".decrease_cart").on("click", function (e) {
    e.preventDefault();
    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");
    cart_id = $(this).attr("data-cart-id");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        // console.log(response);
        if (response.status == "login_required") {
          swal({
            title: response.message,
            text: "",
            icon: "info",
          }).then(function () {
            window.location = "/accounts/login";
          });
        } else if (response.status == "Failed") {
          swal({
            title: response.message,
            text: "",
            icon: "error",
          });
        } else {
          const total_cart_count = response.cart_counter["cart_count"];
          const item_qty = response.cart_quantity;
          $("#cart_counter").html(total_cart_count);
          $("#qty-" + food_id).html(item_qty);
          if (window.location.pathname == "/cart/") {
            deleteItem(response.cart_quantity, cart_id);
            checkEmptyCart();
            applyCartAmounts(
              response.cart_amount["subtotal"],
              response.cart_amount["tax"],
              response.cart_amount["grand_total"]
            );
          }
        }
      },
    });
  });

  $(".delete_cart_item").on("click", function (e) {
    e.preventDefault();
    cart_id = $(this).attr("data-id");
    url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status == "Failed") {
          swal({
            title: response.message,
            text: "",
            icon: "error",
          });
        } else {
          const total_cart_count = response.cart_counter["cart_count"];
          $("#cart_counter").html(total_cart_count);
          swal({
            title: response.message,
            text: "",
            icon: "success",
          });
          deleteItem(0, cart_id);
          checkEmptyCart();
          applyCartAmounts(
            response.cart_amount["subtotal"],
            response.cart_amount["tax"],
            response.cart_amount["grand_total"]
          );
        }
      },
    });
  });
  // Function to delete cart item
  function deleteItem(cart_item_qty, cart_item_id) {
    if (cart_item_qty == 0) {
      document.querySelector(`#cart-item-${cart_item_id}`).remove();
    }
  }

  // Function to check if cart is empty and display text
  function checkEmptyCart() {
    const cart_counter = document.querySelector("#cart_counter").innerHTML;
    if (cart_counter == 0) {
      document.querySelector("#empty-cart").style.display = "block";
    }
  }

  // Function to get subtotal, tax and grand_total
  function applyCartAmounts(subtotal, tax, grand_total) {
    if (window.location.pathname == "/cart/") {
      $("#subtotal").html(subtotal);
      $("#tax").html(tax);
      $("#total").html(grand_total);
    }
  }
});
