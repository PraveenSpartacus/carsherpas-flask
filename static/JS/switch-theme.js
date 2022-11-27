var isLightMode = true;

// if(localStorage.getItem('isLightMode') == 'false')
//     isLightMode = false;




function modeToggle(){
    document.body.classList.toggle('light');
    isLightMode = !isLightMode;
    localStorage.setItem('isLightMode',isLightMode);
    unshow_items(isLightMode)
    show_items(isLightMode)
}

function unshow_items(mode){
    console.log(mode,!mode?'lightmode-item':'darkmode-item')

    let mode_arr = [...document.getElementsByClassName(!mode ? 'lightmode-item':'darkmode-item')];
    console.log(mode_arr)
    mode_arr.forEach(element => {
        element.classList.add('none');
        console.log(element.classList)
    });
}

function show_items(mode){
    let mode_arr = [...document.getElementsByClassName(mode ? 'lightmode-item':'darkmode-item')];
    mode_arr.forEach(element => {
        element.classList.remove('none');
    });
}

show_items(isLightMode)
unshow_items(isLightMode)