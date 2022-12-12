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

function postComment(content, user_id, user_name, book_id) {
  if (!content) return;
  applyCommentWeb(content, user_id, user_name);
  fetch(`/post-comment`, {
    method: "post",
    body: JSON.stringify({
      content: content,
      user_id: user_id,
      book_id: book_id,
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

function checkCart(cart) {
  if (Object.keys(cart).length == 0) redirect("/shoping?page=1");
  fetch(`/check-cart`, {
    method: "post",
    body: JSON.stringify({
      cart: cart,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data) {
        if (Object.keys(data.isValid) > 0) {
          let btn = document.querySelector("#btnModalCart").click();
          let c = document.querySelector(".cart-isunvalid");
          c.innerHTML = "";
          Object.keys(data.isValid).forEach((item) => {
            c.innerHTML += `<p class='text-danger'>${
              data.isValid[item].name + " "
            }</p>`;
          });
          c.innerHTML += "Không còn đủ số lượng, hãy thử lại sau";
        } else redirect("/checkout");
      }
    });
}
