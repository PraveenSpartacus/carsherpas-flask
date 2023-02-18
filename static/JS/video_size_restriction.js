var imageUplaodClass = "image_upload_input"

var uploadFields = [...document.getElementsByClassName('image_upload_input')];

uploadFields.map((uploadField)=>{
    uploadField.onchange = function() {
        if(this.files[0].size > 524288){ //max image size - 500KB
           alert("To optimize page load speed, maximum image size is set at 500KB.");
           this.value = "";
        };
    };
});

