function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function redirect(url){
    window.open(url, '_blank');
}


document.getElementById('contact_btn_group').addEventListener("click", (e) => {
    redirect(buy_url);
});

document.getElementById('contact_btn_group_mob').addEventListener("click", (e) => {
    redirect(buy_url);
});



function animateCircle(){
    var circles = [...document.getElementsByClassName("moving_circles")];
    console.log(circles)

    SVGArray = document.querySelectorAll(".svg-container > svg")
    // console.log(SVG.getAttribute('width'))
    SVG = [...SVGArray].find((svg)=>getComputedStyle(svg.parentElement).getPropertyValue('display') != 'none');
    // SVG = SVGArray[1]
    WIDTH = parseInt(SVG.getAttribute('width'));
    HEIGHT = parseInt(SVG.getAttribute('height'));
    console.log(WIDTH, HEIGHT)
    circles.forEach(element => {
        element.setAttribute('cx','200');
        element.setAttribute('cy','200');
    });

    var cx = 200
    var cy = 200
    console.log(cx,cy);
    x = true
    y = true
    setInterval(() => {
        cx = getRandomInt(0,WIDTH);
        cy = getRandomInt(0,HEIGHT);

        circles.forEach(element => {
            element.setAttribute('cx',cx.toString());
            element.setAttribute('cy',cy.toString());
        });

        SVG = [...SVGArray].find((svg)=>getComputedStyle(svg.parentElement).getPropertyValue('display') != 'none');
        // SVG = SVGArray[1]
        WIDTH = parseInt(SVG.getAttribute('width'));
        HEIGHT = parseInt(SVG.getAttribute('height'));

        // if(x)
        //     cx++;
        // else
        //     cx--;
        
        // if(y)
        //     cy++;
        // else
        //     cy--;
        
        // if(cx >= 1918 || cx <= 0)
        //     x = !x
        // if(cy >= 787 || cy <= 0)
        //     y = !y
        
        console.log("inside setinterval fun",cx,cy)
    },1500);
}


animateCircle();