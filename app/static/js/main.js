function toggleLightbox(mode) {
    var element = document.getElementById("lightbox");
    if (mode == "on") {
        element.style.display = "block";
    } else { 
    var messageBoxElement = element.children[1].children[0];
    messageBoxElement.innerHTML = "Performing operation...";
    element.style.display = "none";
    }
    return element;
}

function submitForm(url, formData, 
        messageBoxElement, successCallBack) {
    var xml = new XMLHttpRequest();
    xml.open("POST", url, true);
    xml.setRequestHeader("Content-type", 
            "application/x-www-form-urlencoded");
    xml.onreadystatechange = function () {
        if (xml.readyState === 4) {
            if (xml.status === 200){
                var responseText = xml.responseText;
                successCallBack(messageBoxElement,
                        responseText);
            } else {
                messageBoxElement.innerHTML = "\
                                            Snap!...looks like there \
                                            was a possible network error";
            }
        }
            //notice that this is async, so it doesn't the browser doesn't
            //wait for a response. therefore, value can not be returned to 
            //the calling function. Only passed to a function is 
            //possible.
    }
    xml.send(formData);
}

function getForm(formId) {
    var element = document.getElementById("lightbox");
    var messageBoxElement = element.children[1].children[0];
    element = toggleLightbox("on");

    form = document.getElementById(formId);

    var formData = '';
    // fetch form values
    // Doing this because form data must be serialized 
    // when using ajax for the webserver to treat it correcctly.
    for (var i = 0, d, v; i < form.length; i++) {
        d = form.elements[i];
        if (d.name && d.value) {
            v = (d.type == "checkbox" || d.type == "radio" ? (d.checked ? d.value : '') : d.value);
            if (v) formData += d.name + "=" + escape(v) + "&";
        }
    }

    function nonImageList(messageBoxElement,
            responseText) {
                var result = JSON.parse(responseText);
                messageBoxElement.innerHTML = result["message"]; }
    function imageList(messageBoxElement,
            responseText) {
                msg = "Success! Image list will "
                    + "now show in a new window." 
                    + " Please make sure your browser allows"
                    + " pop ups from this site.";
                messageBoxElement.innerHTML = msg;
                var newWindow = window.open("","Custom Images List",
                        "height=1000,width=1000",
                        "resizable,scrollbars,status");
                json = JSON.stringify(responseText, null, 4)
                newWindow.document.write(json);}

    switch(formId) {
        case "shareImageForm":
            url = '/imageshareform';
            submitForm(url, formData,
                    messageBoxElement, nonImageList);
            break;
        case "setStatusForm":
            url = '/setstatusform';
            submitForm(url, formData,
                    messageBoxElement, nonImageList);
            break;
        case "listCustomImagesForm":
            url = '/listcustomimagesform';
            submitForm(url, formData,
                    messageBoxElement, imageList);
            break;
        case "listAllImagesForm":
            url = '/imagedetailform';
            submitForm(url, formData,
                    messageBoxElement, imageList);
            break;

    }

}

function disableForms(activeForm) {
    var elements = ["shareImageContainer", 
        "setStatusContainer",
        "listAllImagesContainer",
        "imageDetailContainer",
        "listCustomImagesContainer"];
    var waitToActivate;

    elements.forEach(function (elementId) {
        var element = document.getElementById(elementId);
        if (activeForm == element.id) {
            waitToActivate = element;
        } else {
        element.style.display = "none";
        }
    });
    if (getComputedStyle(waitToActivate) !== "block" ) {
        waitToActivate.style.display = "block";
    }
}


function click(event) {
    var arg = event.target.id;
    switch(arg) {
        case "exitButton":
            toggleLightbox();
            break;
        case "shareImage":
            disableForms("shareImageContainer");
            break;
        case "setSatus":
            disableForms("setStatusContainer");
            break;
        case "listCustomImages":
            disableForms("listCustomImagesContainer");
            break;
        case "listAllImages":
            disableForms("listAllImagesContainer");
            break;
        case "imageDetail":
            disableForms("imageDetailContainer");
            break;
    }
}


window.onload = function() {
    document.addEventListener("submit", function(event) {
        event.preventDefault();
        getForm(event.srcElement.id);
    }, false);
    document.addEventListener("click", click, false); 
}

