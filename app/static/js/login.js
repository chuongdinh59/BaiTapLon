let container = document.getElementById("container");
let form_sign_in = document.querySelector(".form-sign-in");

toggle = () => {
  container.classList.toggle("sign-in");
  container.classList.toggle("sign-up");
};

toggleQrCode = () => {
  form_sign_in.classList.toggle("show-qr");
};

setTimeout(() => {
  container.classList.add("sign-in");
}, 200);
