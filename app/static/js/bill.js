function renderBookBill() {
  let b = localStorage.getItem("book");
  if (!b) return;
  let list = document.querySelector(".list-b-bill");
  let reciept_price = document.querySelector(".reciept_price");
  let va = JSON.parse(b);
  let html = "";
  let price = 0;
  Object.keys(va).forEach(function (key, index) {
    price += parseInt(va[key].price);
    html += `<div
    class="item mt-3 d-flex align-items-center justify-content-between"
    style="width: 100%" id = 'item-${va[key].id}'
  >
    <div class="d-flex align-items-center">
      <h6 style="font-size: 20px">${va[key].name}</h6>
    </div>
    <p class="m-0 text-danger" id='item-price' style="font-size: 20px">${va[key].price}</p>
    <div class="form-group">
      <input
        type="number"
        class="form-control"
        id="quantity-${va[key].id}"
        aria-describedby="emailHelp"
        placeholder="Số lượng"
        onblur="applyPrice(event, ${va[key].id})"
        value="1"
      />
    </div>
    <span onclick="deleteBookEm(${va[key].id})"><i class="fa-solid fa-xmark"></i></span>
  </div>`;
  });
  list.innerHTML = html;
  reciept_price.innerHTML = price;
}
renderBookBill();
