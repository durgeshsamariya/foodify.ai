const category = {
    0: ['Panipuri','Pani Puri'], 1: ['bhajiya','Bhajiya'], 2: ['bhindi masala','Bhindi Masala'],
    3: ['biryani','Biryani'], 4: ['boil eggs','Boil Eggs'], 5: ['burger','Burger'],
    6: ['chaas','Chaas'], 7: ['chaat','Chaat'], 8: ['chai','Chai'], 9: ['dosa','Dosa'],
    10: ['fafda','Fafda'], 11: ['franki','Franki'], 12: ['fries','Fries'],
    13: ['manchurian','Manchurian'], 14: ['milkshakes','Milkshakes'], 15: ['momos','Momos'],
    16: ['naan','Naan'], 17: ['orange_juice','Orange Juice'], 18: ['paneer tikka','Paneer Tikka'], 19: ['paratha','Paratha'],
    20: ['pav bhaji','Pav Bhaji'], 21: ['pizza','Pizza'], 22: ['poha','Poha'],
    23: ['puri-bhaji','Puri Bhaji'], 24: ['rajma','Rajma'], 25: ['samosa','Samosa'],
    26: ['sandwich','Sandwich'], 27: ['sandwich subs','Sandwich Subs'], 28: ['thepla','Thepla'], 29: ['vada pav','Vada Pav']
}



// Grab a reference to our status text element on the web page.
// Initially we print out the loaded version of TFJS.
// Check to see if TF.js is available
const tfjs_status = document.getElementById("tfjs_status");

if (tfjs_status) {
    tfjs_status.innerText = "Loaded TensorFlow.js - version:" + tf.version.tfjs;
}

//========================================================================
// Drag and drop image handling
//========================================================================

var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");

// Add event listeners
fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
    // prevent default behaviour
    e.preventDefault();
    e.stopPropagation();

    fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
    // handle file selecting
    var files = e.target.files || e.dataTransfer.files;
    fileDragHover(e);
    for (var i = 0, f; (f = files[i]); i++) {
        previewFile(f);
    }
}

//========================================================================
// Web page elements for functions to use
//========================================================================

var imagePreview = document.getElementById("image-preview");
// var imageDisplay = document.getElementById("image-display");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
var predProb = document.getElementById("pred-prob");
// var loader = document.getElementById("loader");
let tflitemodel; // This is in global scope

//========================================================================
// Main button events
//========================================================================

const initialize = async () => {
    console.log("Loading model")
    model = await tflite.loadTFLiteModel("https://raw.githubusercontent.com/durgeshsamariya/foodify.ai/main/model/model.tflite");
    tflitemodel = model;
    console.log("Loaded Successfully")
}

initialize();

function previewFile(file) {
    // show the preview of the image
    var fileName = encodeURI(file.name);

    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
        imagePreview.src = URL.createObjectURL(file);
        show(imagePreview);
        hide(uploadCaption);
        // reset
        predResult.innerHTML = "";
        // imageDisplay.classList.remove("loading");
        //displayImage(reader.result, "image-display");
    };
}

//https://www.youtube.com/watch?v=5q8BzYN4rqA 

async function predictModel() {
    // action for the submit button

    if (!imagePreview.src) {
        window.alert("Please select an image...");
        return;
    }

    tensor = tf.image.resizeBilinear(tf.browser.fromPixels(imagePreview), [75, 75])
        .toFloat()
        .expandDims()
        .div(255);

    console.log("Predicting...");
    const output = await tflitemodel.predict(tensor);
    const output_values = tf.softmax(output.arraySync()[0]);
    console.log("Arg max:");
    // console.log(output);
    console.log(output_values.arraySync());
    console.log("Output:");
    console.log(output.arraySync());
    console.log(output.arraySync()[0]); // arraySync() Returns an array to use

    predResult.innerHTML = category[output_values.argMax().arraySync()][1];
    // predProb.innerHTML = output_values.max().arraySync() * 100 + "%";

    show(predResult)
    // show(predProb)
}

function clearImage() {
    // reset selected files
    fileSelect.value = "";

    // remove image sources and hide them
    imagePreview.src = "";
//    imageDisplay.src = "";
    predResult.innerHTML = "";

    hide(imagePreview);
//    hide(imageDisplay);
//    hide(loader);
    hide(predResult);
    hide(predProb);
    show(uploadCaption);

//   imageDisplay.classList.remove("loading");
}

//========================================================================
// Helper functions
//========================================================================

function displayImage(image, id) {
    // display image on given id <img> element
    let display = document.getElementById(id);
    display.src = image;
    show(display);
}

function hide(el) {
    // hide an element
    el.classList.add("hidden");
}

function show(el) {
    // show an element
    el.classList.remove("hidden");
}

//
//
//

// Add listener to see if someone uploads an image
//fileSelect.addEventListener("change", previewFile);