const panel = document.getElementById("layer_panel");

let layer = document.createElement("div");
layer.setAttribute("class", "layer");

let layer_type = document.createElement("div");
layer_type.setAttribute("class", "layer_type");
let layer_type_button = document.createElement("div");
layer_type_button.setAttribute("class", "layer_type_button");
layer_type.innerText = "Test";
let layer_type_content = document.createElement("div");
layer_type_content.setAttribute("class", "dropdown-content");
layer_type_content.innerHTML = "<a href=\"#\">菜鸟教程 1</a><a href=\"#\">菜鸟教程 2</a><a href=\"#\">菜鸟教程 3</a>";

layer_type.appendChild(layer_type_button);
layer_type.appendChild(layer_type_content);

layer.onclick = function () {
    layer.setAttribute("class", "layer_expand");
    layer_type.setAttribute("class", "layer_type dropdown");
    layer_type_button.setAttribute("class", "layer_type_button dropbtn");
};

let content = document.createElement("div");
content.setAttribute("class", "layer_content");

content.appendChild(layer_type);

layer.appendChild(content);

panel.appendChild(layer);

function setUpLayer(container) {
    let center = document.createElement("div");
    center.setAttribute("class", "center_box");
}