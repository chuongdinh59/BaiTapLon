// Redirect menu

const list_menu = document.querySelectorAll(".header__menu.mobile-menu ul li");

function fillLine() {
  let g = document.querySelector(".header__menu.mobile-menu ul li.active");
  g.classList?.remove("active");
  switch (window.location.pathname) {
    case "/shop":
      list_menu[1].classList.add("active");
      break;
    case "/":
      list_menu[0].classList.add("active");
      break;
    default:
      break;
  }
}
function paramsToObject(entries) {
  const result = {};
  for (const [key, value] of entries) {
    // each 'entry' is a [key, value] tupple
    result[key] = value;
  }
  return result;
}
const pagination = document.querySelector(".product__pagination");
const nextBtn = document.querySelector(".next");
const preBtn = document.querySelector(".pre");
var search = location.search.substring(1);
JSON.parse(
  '{"' + search.replace(/&/g, '","').replace(/=/g, '":"') + '"}',
  function (key, value) {
    return key === "" ? value : decodeURIComponent(value);
  }
);
current_page =
  parseInt(
    JSON.parse(
      '{"' + search.replace(/&/g, '","').replace(/=/g, '":"') + '"}',
      function (key, value) {
        return key === "" ? value : decodeURIComponent(value);
      }
    )?.page
  ) || 1;
function renderPage(page_number = 1) {
  page_number = current_page;
  target = page_number + 2;
  pagination.innerHTML = "";
  if (current_page == 1) {
    target = target + 2;
  } else if (current_page == 2) {
    target = target + 1;
  }
  pagination.innerHTML += `<a href = ${handleChageAddress(
    current_page - 1
  )}  class="pre ${current_page == 1 ? "none-cusor" : ""}" >
    <i class="fa fa-angle-left"></i>
  </a>`;
  for (let i = page_number - 2; i <= target; i++) {
    if (i <= 0) continue;
    pagination.innerHTML += `<a href="${handleChageAddress(
      i
    )}" onclick="renderPage(${i})" class=${
      i == current_page ? "active" : ""
    }>${i}</a>`;
  }
  pagination.innerHTML += `<a href = ${handleChageAddress(
    current_page + 1
  )} class="next" href=""><i class="fa fa-angle-right"></i> </a>
`;
}
function handleChageAddress(page) {
  page = page == 0 ? 1 : page;
  return window.location.href.replace(`page=${current_page}`, `page=${page}`);
}

function renderPrice() {
  const price = document.querySelector(".shop__sidebar__price ul");
  price.innerHTML = "";
  for (let i = 0; i < 2; i++) {
    price.innerHTML += `
      <li>
        <a href=${hanleChangePrice(i)}>${
      i == 0 ? "Low to High" : "High to Low"
    } </a>
      </li>
    `;
  }
}
renderPrice();
function hanleChangePrice(sort_value) {
  if (window.location.href.includes("sort=")) {
    let search = location.search.substring(1);
    current_sort = parseInt(
      JSON.parse(
        '{"' + search.replace(/&/g, '","').replace(/=/g, '":"') + '"}',
        function (key, value) {
          return key === "" ? value : decodeURIComponent(value);
        }
      )?.sort
    );
    return window.location.href.replace(
      `sort=${current_sort}`,
      `sort=${sort_value}`
    );
  } else {
    return window.location.href + `&sort=${sort_value}`;
  }
}
fillLine();
renderPage();

function formatCurrency(__value) {
  return new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
  }).format(__value);
}

function changeUpQuantity(id) {
  const subtotal = document.querySelector("#sub_total");
  const total = document.querySelector("#total");
  const quantity = document.querySelector(`#cart_quantity_${id} input`);
  let newQuantity = parseInt(quantity.value) + 1;
  quantity.setAttribute("value", `${newQuantity}`);
  const price = document.querySelector(`#cart_price_${id}`);
  const total_price = document.querySelector(`#cart_total_price_${id}`);
  let newPrice = newQuantity * parseInt(price.innerHTML);
  subtotal.innerHTML =
    parseInt(subtotal.innerHTML) + parseInt(price.innerHTML) + " VNĐ";
  total.innerHTML = subtotal.innerHTML;
  total_price.innerHTML = newPrice;
}
function changeDownQuantity(id) {
  const subtotal = document.querySelector("#sub_total");
  const quantity = document.querySelector(`#cart_quantity_${id} input`);
  if (quantity.value == "1") return;
  let newQuantity = parseInt(quantity.value) - 1;
  quantity.setAttribute("value", `${newQuantity}`);
  const price = document.querySelector(`#cart_price_${id}`);
  const total_price = document.querySelector(`#cart_total_price_${id}`);
  let newPrice = newQuantity * parseInt(price.innerHTML);
  subtotal.innerHTML =
    parseInt(subtotal.innerHTML) - parseInt(price.innerHTML) + " VNĐ";
  total_price.innerHTML = newPrice;
}

function deleteItem(id) {
  const item = document.querySelector(`#row_cart_${id}`);
  const subtotal = document.querySelector("#sub_total");
  const quantity = document.querySelector(`#cart_quantity_${id} input`);
  let newQuantity = parseInt(quantity.value);
  const price = document.querySelector(`#cart_price_${id}`);
  let newPrice = newQuantity * parseInt(price.innerHTML);
  let total = document.querySelector("#total");
  subtotal.innerHTML = parseInt(subtotal.innerHTML) - newPrice + " VNĐ";
  total.innerHTML = subtotal.innerHTML;
  item.remove();
}

function verifyAddToCart(id, name, unitPrice, isLogin = "False") {
  if (isLogin == "False") {
    return (location.href = "/login");
  }
  addToCart(id, name, unitPrice);
}

function getCartFromWeb(cart, option = {}) {
  console.log(cart);
  const list_cart_web = document.querySelectorAll(".product__cart__item");
  const id = [];
  list_cart_web.forEach((item) => id.push(item?.id.replace("cart_", "")));
  id.forEach((i) => {
    const item1 = document.querySelector(`#cart_price_${i}`);
    const item2 = document.querySelector(
      `.quantity__item#cart_quantity_${i} input`
    );
    let price = parseInt(item1.innerHTML);
    cart[`${i}`].price = price;
    let newQuantity = item2.value;
    cart[`${i}`].quantity = parseInt(newQuantity);
  });
  Object.keys(cart)
    .map((key) => {
      if (!id.includes(key)) {
        return key;
      }
    })
    .filter(function (element) {
      return element !== undefined;
    })
    .forEach((i) => delete cart[`${i}`]);
  return { ...cart, ...option };
}

function redirect(path) {
  window.location.href = window.location.origin + path;
}

function applyNewValue(voucher) {
  const total = document.querySelector(".cart__total #total");
  const subtotal = document.querySelector("#sub_total");
  const mgs_err = document.querySelector(".msg_voucher__err");
  const mgs_succ = document.querySelector(".msg_voucher__succ");
  mgs_succ.innerHTML = "";
  mgs_err.innerHTML = "";
  if (voucher.status === 1) {
    total.innerHTML =
      (parseInt(subtotal.innerHTML.replace(" VNĐ", "")) *
        (100 - voucher.rate)) /
        100 +
      " VNĐ";
    mgs_succ.innerHTML = voucher.msg;
    localStorage.setItem("voucher", JSON.stringify({ voucher: voucher }));
  } else {
    total.innerHTML = subtotal.innerHTML;
    mgs_err.innerHTML = voucher.msg;
    localStorage?.removeItem("voucher");
  }
}

function getOrderWeb(cart, user_id) {
  let address = document.querySelector(".checkout__input__add").value;
  let phone = document.querySelector("#phone").value;
  let email = document.querySelector("#email").value;
  let note = document.querySelector("#note").value;
  let voucher = JSON.parse(localStorage.getItem("voucher"));

  let obj = {
    cart,
    address,
    phone,
    email,
    note: note,
    user_id: user_id,
  };
  if (voucher) {
    obj = {
      ...obj,
      voucher_id: voucher.voucher.id,
    };
  }
  return obj;
}

function change_image(image) {
  var container = document.getElementById("main-image");

  container.src = image.src;
}
function deleteAllCookies() {
  var cookies = document.cookie.split(";");

  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i];
    var eqPos = cookie.indexOf("=");
    var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    console.log(name);
    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
  }
}
function logout() {
  localStorage.clear();
  sessionStorage.clear();
  document.cookie =
    "username=session; expires=Thu, 18 Dec 2013 12:00:00 UTC; path=/";
  redirect("/");
}

function applyCommentWeb(content, user_id, user_name) {
  console.log(content, user_id);
  let comment = document.querySelector("#comment");
  let comment_list = document.querySelector(".comment-list");
  comment.value = "";
  comment_list.innerHTML += `<div class="d-flex" style="width: 100%">
        <div class="d-flex" style="width: 80%">
          <p class="text-primary" style="width: 10%">${user_name}</p>
          <p>${content}</p>
        </div>
        <p class="text-right flex-1">Vừa xong</p>
      </div>`;
}

function saveBook(id, name, price) {
  console.log(1);
  let book = localStorage.getItem("book");
  if (!book) {
    book = {};
    book[id] = { id, name, price };
    localStorage.setItem("book", JSON.stringify(book));
  } else {
    let oldbook = JSON.parse(book);
    let newBook = {
      ...oldbook,
      [id]: { id, name, price },
    };
    localStorage.setItem("book", JSON.stringify(newBook));
  }
  renderBookBill();
}

function applyPrice(event, id) {
  let reciept_price = document.querySelector(".reciept_price");
  let b = document.querySelector(`#item-${id} #item-price`);
  reciept_price.innerHTML =
    parseInt(reciept_price.innerHTML) +
    parseInt(event.target.value) * parseInt(b.innerHTML);
}

function getOrderFromEmployee(user_id) {
  let c = localStorage.getItem("book");
  if (!c) return;
  c = JSON.parse(c);
  keys = Object.keys(c);
  keys.forEach((key) => {
    let unitItem = document.querySelector(`#item-${key} #quantity-${key}`);
    let v = parseInt(unitItem.value);
    c[key] = {
      ...c[key],
      quantity: v,
    };
  });
  console.log({
    ...c,
    user_id: user_id,
    address: "Mua trực tiếp",
    note: "không có",
    voucher: null,
  });
  return {
    cart: { ...c },
    user_id: user_id,
    address: "Mua trực tiếp",
    note: "không có",
    voucher: null,
  };
}
function deleteBookEm(id) {
  let b = localStorage.getItem("book");
  if (!b) return;
  b = JSON.parse(b);
  let reciept_price = document.querySelector(".reciept_price ");
  reciept_price.innerHTML =
    parseInt(reciept_price.innerHTML) - parseInt(b[id].price);
  delete b[id];
  localStorage.setItem("book", JSON.stringify(b));
  let c = document.querySelector(`#item-${id}`).remove();
}
