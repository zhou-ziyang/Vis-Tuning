function addSentence(asp, sen) {
	
	console.log("add sentence");
	
	let result = document.getElementById("result");
	
    let sentence = document.createElement("sentence");
	sentence.setAttribute("class", "sentence full_width");
	result.appendChild(sentence);
	
    let aspect_box = document.createElement("aspect_box");
	aspect_box.setAttribute("class", "aspect_box left main");
	sentence.appendChild(aspect_box);
	
    let words = document.createElement("words");
	words.setAttribute("class", "words main");
	sentence.appendChild(words);
	
    let aspect = document.createElement("aspect");
	aspect.setAttribute("class", "aspect");
	if (asp == 1) {
		layer_type_content.innerHTML = "<a>👍</a>";
	} else if (asp == 0) {
		layer_type_content.innerHTML = "<a>👎</a>";
	}
	aspect_box.appendChild(aspect);
	
    let word_panel = document.createElement("word_panel");
	word_panel.setAttribute("class", "word_panel");
	words.appendChild(word_panel);
	
	let word_list = sen.split(" ")
	for (let w of word_list) {
		let word = document.createElement("word");
		word.setAttribute("class", "word");
		word.innerText = w;
		word_panel.appendChild(word);
	}
}