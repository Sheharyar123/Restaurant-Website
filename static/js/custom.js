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
  var place = autocomplete.getPlace();

  // User did not select the prediction. Reset the input field or alert()
  if (!place.geometry) {
    document.getElementById("id_address").placeholder = "Start typing...";
  } else {
    console.log("place name=>", place.name);
  }
  // get the address components and assign them to the fields
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
        }
      },
    });
  });
});
