function addToCart(id, name, price) {
  fetch("/shoping-cart", {
    method: "post",
    body: JSON.stringify({
      id,
      name,
      price,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then(function (data) {
      let { total_quantity, total_amount } = data;
      let d = document.querySelector(".header__nav__option .price");
      let b = document.querySelector(".header__nav__option span");
      d.innerText = total_amount;
      b.innerHTML = total_quantity;
    });
}

function updateCart(cart) {
  fetch(`/update-cart`, {
    method: "post",
    body: JSON.stringify({
      cart,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      let { total_quantity, total_amount } = data;
      let d = document.querySelector(".header__nav__option .price");
      let b = document.querySelector(".header__nav__option span");
      d.innerText = total_amount;
      b.innerHTML = total_quantity;
    });
}

function applyVoucher(e) {
  let code = e.target.querySelector("input");
  fetch(`/apply-voucher`, {
    method: "post",
    body: JSON.stringify({
      code: code.value,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data) {
        applyNewValue(data);
      }
    });
}

function createOrder(order) {
  fetch(`/create-reciept`, {
    method: "post",
    body: JSON.stringify({
      order: order,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data) {
        if (data.status == 1) {
          let b = document.querySelector("#btnModal");
          b.click();
          localStorage.removeItem("voucher");
        }
      }
    });
}
