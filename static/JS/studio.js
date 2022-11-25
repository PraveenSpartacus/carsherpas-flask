function moveRight(){
    slider = document.getElementById("slider");
    x = slider.classList;
    if(x[0] == 'img1'){
        slider.classList.remove('img1');
        slider.classList.add('img2')
    }
    else if(x[0] == 'img2'){
        slider.classList.remove('img2');
        slider.classList.add('img3')
    }
    else if(x[0] == 'img3'){
        slider.classList.remove('img3');
        slider.classList.add('img4')
    }
    else if(x[0] == 'img4'){
        slider.classList.remove('img4');
        slider.classList.add('img1')
    }
    
        
}

function moveLeft(){
    slider = document.getElementById("slider");
    x = slider.classList;
    if(x[0] == 'img2'){
        slider.classList.remove('img2');
        slider.classList.add('img1')
    }
    else if(x[0] == 'img3'){
        slider.classList.remove('img3');
        slider.classList.add('img2')
    }
    else if(x[0] == 'img4'){
        slider.classList.remove('img4');
        slider.classList.add('img3')
    }
    else if(x[0] == 'img1'){
        slider.classList.remove('img1');
        slider.classList.add('img4')
    }
    
        
}