function renderTotalPrice() {
  let voucher = localStorage.getItem("voucher")
    ? JSON.parse(localStorage.getItem("voucher"))
    : null;
  let total = document.querySelector(
    ".checkout__total__all #checkout_total span"
  );
  let sub_total = document.querySelector(
    ".checkout__total__all #checkout_subtotal span"
  );
  if (voucher) {
    voucher = voucher.voucher;
    total.innerHTML =
      ((100 - voucher.rate) *
        parseInt(sub_total.innerHTML.replace("VNĐ", ""))) /
      100;
  } else {
    total.innerHTML = sub_total.innerHTML;
  }
}
renderTotalPrice();
